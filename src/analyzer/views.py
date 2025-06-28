from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .serializer import AnalyzerInputSerializer
from .service import AnalyzerService



class AnalyzerView(APIView):

    parser_classes = [MultiPartParser]

    def post(self, request):

        serializer = AnalyzerInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = AnalyzerService()
        document_txt = service.extract_document_text(serializer.validated_data["document"])

        answer = service.answer_query(document_txt, serializer.validated_data["query"])
        return Response(data={"answer": answer})

