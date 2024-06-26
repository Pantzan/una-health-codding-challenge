import time
import io
from dateutil.parser import parse

import pandas as pd
from django.utils import timezone
from rest_framework import generics, serializers, status
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser
from rest_framework.response import Response

from unaapp.serializers import CreateUserGlucoseMetricsSerializer, GlucoseMetricSerializer
from unaapp.models import User, UserReport, GlucoseMetric

from asgiref.sync import sync_to_async, async_to_sync
import asyncio


class CreateUserMetrics(generics.CreateAPIView):
    serializer_class = CreateUserGlucoseMetricsSerializer
    parser_classes = [MultiPartParser]

    # borrowed from adrf in order to demonstrate async behavior in DRF which is not yet supported (or planned)
    # https://github.com/em1208/adrf/blob/main/adrf/views.py
    async def dispatch(self, request, *args, **kwargs):
        """
        `.async_dispatch()` is pretty much the same as Django's regular dispatch,
        except for awaiting the handler function and with extra hooks for startup,
        finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = await handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    async def post(self, request, *args, **kwargs):
        de_en_column_mapping = {
            'Gerät': 'device',
            'Seriennummer': 'serial_number',
            'Gerätezeitstempel': 'device_timestamp',
            'Aufzeichnungstyp': 'recording_type',
            'Glukosewert-Verlauf mg/dL': 'glucose_value_ml',
            'Glukose-Scan mg/dL': 'glucose_scan_ml',
        }

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['report_file']
        file_obj = io.BytesIO(file.read())
        report_metadata = pd.read_csv(file_obj, nrows=1).columns.tolist()[1:]
        metadata_dict = {report_metadata[i]: report_metadata[i + 1] for i in range(0, len(report_metadata), 2)}

        if not metadata_dict.keys():
            Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'The file does not contain metadata'})

        elif (
                ('Erstellt am' not in metadata_dict.keys() or not metadata_dict.get('Erstellt am'))
                or ('Erstellt von' not in metadata_dict.keys() or not metadata_dict.get('Erstellt von'))
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'The file metadata are invalid'})

        file_obj.seek(0)
        data = pd.read_csv(file_obj, skiprows=1, na_filter=False)

        if not data.shape[0]:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'There are not data in the report'})

        # drop unnecessary columns for the sake of this assignment
        data = data[data.columns.intersection(de_en_column_mapping.keys())].rename(columns=de_en_column_mapping)
        data['device_timestamp'] = data['device_timestamp'].apply(lambda x: timezone.make_aware(parse(x)))
        data = data.astype(object).replace('', -1)

        file_obj.close()
        try:
            await asyncio.create_task(self.write_to_db(metadata_dict=metadata_dict, data=data))
            print("--------- api call is finishing and returning")
            return Response(status=status.HTTP_201_CREATED)
        except ValueError as e:
            print(e)
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={'error': 'The report record already exists'}
            )

        # return Response(status.HTTP_204_NO_CONTENT)

    @sync_to_async
    def write_to_db(self, metadata_dict, data):
        s = time.perf_counter()
        try:
            user = User.objects.get(name=metadata_dict.get('Erstellt von'))
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={'error': 'The user does not exists in our records'}
            )

        if UserReport.objects.filter(
                user=user, timestamp=parse(metadata_dict.get('Erstellt am'))
        ).exists():
            # debug async connections
            pass
            # raise ValueError("UserReport exists")

        user_report_obj = UserReport.objects.create(user=user, timestamp=parse(metadata_dict.get('Erstellt am')))

        GlucoseMetric.objects.bulk_create([
            GlucoseMetric(**row, report=user_report_obj) for _, row in data.iterrows()]
        )
        t = round(time.perf_counter() - s, 2)
        print(f"************ write in db finished at: {t}")


class GetGlucoseLevelsByUser(generics.ListAPIView):
    serializer_class = GlucoseMetricSerializer

    def get_queryset(self):
        """
        We use simple filtering for simplicity. In real scenario django-filters is the right tool to handle
        sorting and filtering
        """

        user = self.request.query_params.get("user")
        sort = self.request.query_params.get("sort")
        start_level = self.request.query_params.get("start", -1)
        end_level = self.request.query_params.get("stop", -1)
        limit = self.request.query_params.get("limit")

        queryset = GlucoseMetric.objects.filter(report__user__name=user)
        if sort in ['device', 'recording_type', 'serial_number']:
            queryset = queryset.order_by(f'-{sort}')
        else:
            queryset = queryset.order_by('glucose_value_ml')

        if start_level and int(start_level) > 0:
            queryset = queryset.filter(glucose_value_ml__gte=int(start_level))

        if end_level and int(end_level) > 0 and end_level > start_level:
            queryset = queryset.filter(glucose_value_ml__lte=int(end_level))

        if limit and int(limit) > 1:
            queryset = queryset[:int(limit)]

        return queryset

    def get(self, request, *args, **kwargs):
        user_name = self.request.query_params.get("user")
        if not user_name:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={'error': 'The user name is required'}
            )
        else:
            try:
                User.objects.get(name=user_name)
            except User.DoesNotExist:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST, data={'error': 'The user does not exist in our records'}
                )
        return super().get(request)


class GetGlucoseLevelsById(generics.RetrieveAPIView):
    serializer_class = GlucoseMetricSerializer

    def get(self, request, *args, **kwargs):
        glucose_level_id = self.kwargs.get("pk")

        if glucose_level_id:
            try:
                obj = GlucoseMetric.objects.get(id=glucose_level_id)
                return Response(GlucoseMetricSerializer(obj).data)
            except GlucoseMetric.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
