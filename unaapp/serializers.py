from rest_framework import serializers

from unaapp.models import GlucoseMetric


class GlucoseMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlucoseMetric


class CreateUserGlucoseMetricsSerializer(serializers.Serializer):
    report_file = serializers.FileField(max_length=None, allow_empty_file=False, use_url=False)
