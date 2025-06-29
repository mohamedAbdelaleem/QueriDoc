from rest_framework import serializers


class AnalyzerInputSerializer(serializers.Serializer):
    query = serializers.CharField()
    document = serializers.FileField()
    def validate_document(self, file):
        if file.content_type != 'application/pdf':
            raise serializers.ValidationError("Only PDF files are allowed.")
        
        if not file.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("The file must have a .pdf extension.")
        
        return file