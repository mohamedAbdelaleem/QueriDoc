import fitz 
import boto3
import json
from django.core.files.uploadedfile import InMemoryUploadedFile


class AnalyzerService:

    def __init__(self):
        self.bedrock_runtime = boto3.client("bedrock-runtime")

    def extract_document_text(self, document: InMemoryUploadedFile) -> str:
        full_text = ""

        document.seek(0)
        with fitz.open(stream=document.read(), filetype="pdf") as doc:
            for page in doc:
                full_text += page.get_text() + "\n"
        
        return full_text

    def answer_query(self, document_txt: str, query: str) -> str:
        prompt = f"""Human: You are a helpful assistant.

                    Answer the question below using the provided document as your primary source. If the document contains a clear answer, use it.

                    If the document does not contain a direct answer but the topic is mentioned or discussed, you may use your general knowledge to answer the question — but you should still ground your response in the context of the document when possible.

                    If the topic is completely unrelated to the document, respond with:
                    "The document does not contain the answer."

                    Document:
                    {document_txt}

                    Question: {query}

                    Assistant:"""
        
        response = self.bedrock_runtime.invoke_model(
            modelId="anthropic.claude-v2:1",
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 700,
                "temperature": 0.5,
                "top_k": 250,
                "top_p": 1,
                "stop_sequences": ["\n\nHuman:"]
            }),
            contentType="application/json",
            accept="application/json"
        )

        
        response_body = json.loads(response['body'].read())
        print(response_body)
        summary = response_body['completion']
        return summary
