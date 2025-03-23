import grpc
from concurrent import futures
import log_summary_pb2
import log_summary_pb2_grpc
import json
from vertexai.generative_models import GenerativeModel
from vertexai import init
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "default-project-id")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")

class LogSummaryServiceServicer(log_summary_pb2_grpc.LogSummaryServiceServicer):
    def __init__(self):
        init(project=PROJECT_ID, location=LOCATION)
        self.model = GenerativeModel("gemini-2.0-flash-001")

    def SummarizeLogs(self, request, context):
        logs = [
            {
                "activity_category": log.activity.activity_category.name,
                "activity_title": log.activity.title,
                "datetime": log.datetime,
                "is_completed": log.is_completed,
            }
            for log in request.logs
        ]

        summary = self.get_summary_from_vertex_ai(logs)
        return log_summary_pb2.LogResponse(summary=summary)

    def get_summary_from_vertex_ai(self, logs):
        """ Send logs to Vertex AI's Gemini 2.0 Flash and get summary. """
        response = self.model.generate_content(
            "Berikut ini adalah log aktivitas seorang pasien demensia selama satu minggu. "
            "Rangkum log berikut menjadi satu paragraf yang mudah dibaca:\n"
            + json.dumps(logs, indent=2),
            generation_config={"temperature": 0.2, "max_output_tokens": 256}
        )
        return response.text.strip()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    log_summary_pb2_grpc.add_LogSummaryServiceServicer_to_server(LogSummaryServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()