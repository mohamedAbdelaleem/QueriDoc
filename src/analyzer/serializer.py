from rest_framework import serializers


class AnalyzerInputSerializer(serializers.Serializer):
    query = serializers.CharField()
    document = serializers.FileField()