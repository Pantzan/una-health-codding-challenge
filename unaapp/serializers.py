from rest_framework import serializers

from unaapp.models import GlucoseMetric


class GlucoseMetricSerializer(serializers.ModelSerializer):
    report = serializers.SerializerMethodField('get_report')

    class Meta:
        model = GlucoseMetric
        fields = '__all__'

    def get_report(self, obj):
        return f'{obj.report.user.name} - {obj.report.timestamp}'


class CreateUserGlucoseMetricsSerializer(serializers.Serializer):
    report_file = serializers.FileField(max_length=None, allow_empty_file=False, use_url=False)
