from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import grpc
import log_summary_pb2
import log_summary_pb2_grpc

@csrf_exempt
def summarize_logs(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

    try:
        body = json.loads(request.body)
        logs = body.get("logs", [])

        if not logs:
            return JsonResponse({"error": "Logs parameter is required"}, status=400)

        # Setup gRPC connection
        channel = grpc.insecure_channel("localhost:50051")
        stub = log_summary_pb2_grpc.LogSummaryServiceStub(channel)

        # Convert request data to gRPC format
        log_request = log_summary_pb2.LogRequest(
            logs=[
                log_summary_pb2.ActivityOccurrence(
                    datetime=log["datetime"],
                    is_completed=log["is_completed"],
                    activity=log_summary_pb2.Activity(
                        title=log["activity"]["title"],
                        activity_category=log_summary_pb2.ActivityCategory(name=log["activity"]["activity_category"]["name"])
                    )
                )
                for log in logs
            ]
        )

        # Call the gRPC service
        response = stub.SummarizeLogs(log_request)

        return JsonResponse({"summary": response.summary})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
