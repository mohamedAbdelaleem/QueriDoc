import pdfplumber
import boto3
import json
from django.core.files.uploadedfile import InMemoryUploadedFile


class AnalyzerService:

    def __init__(self):
        self.bedrock_runtime = boto3.client("bedrock-runtime")

    def extract_document_text(self, document: InMemoryUploadedFile) -> str:
        full_text = ""
        print("Begin")
        document.seek(0)
        with pdfplumber.open(document) as doc:
            for page in doc.pages:
                full_text += page.extract_text() or ''  # Avoid NoneType errors
                full_text += "\n"
        
        print("End")
        return full_text

    def answer_query(self, document_txt: str, query: str) -> str:
        
        prompt = f"""You are a helpful assistant.
                    You must answer the following question using the information provided in the document below.
                    The answer may not directly be in the document, use the information in the document to provide a helpful answer.
                    If the document does not contain any of the information required to answer the question, respond with:
                    'The document does not contain the answer.'

                    Question: {query}

                    Document: {document_txt}
                    """

        
        prompt_config = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "temperature": 0.5,
            "top_k": 250,
            "top_p": 0.99,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                    ],
                }
            ],
        }


        body = json.dumps(prompt_config)

        modelId = "anthropic.claude-3-haiku-20240307-v1:0"
        accept = "application/json"
        contentType = "application/json"

        response = self.bedrock_runtime.invoke_model(
            body=body, modelId=modelId, accept=accept, contentType=contentType
        )
        response_body = json.loads(response.get("body").read())

        results = response_body.get("content")[0].get("text")
        return results
