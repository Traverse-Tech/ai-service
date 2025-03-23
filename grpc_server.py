import grpc
from concurrent import futures
from va import va_pb2_grpc
from summarizer import log_summary_pb2_grpc
from summarizer.services import LogSummaryServiceServicer
from va.services import VoiceAssistantServicer

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    va_pb2_grpc.add_VoiceAssistantServiceServicer_to_server(VoiceAssistantServicer(), server)
    log_summary_pb2_grpc.add_LogSummaryServiceServicer_to_server(LogSummaryServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()