# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import va.va_pb2 as va__pb2

GRPC_GENERATED_VERSION = '1.71.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in va_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class VoiceAssistantServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ProcessAudio = channel.unary_unary(
                '/va.VoiceAssistantService/ProcessAudio',
                request_serializer=va__pb2.AudioRequest.SerializeToString,
                response_deserializer=va__pb2.AudioResponse.FromString,
                _registered_method=True)
        self.HealthCheck = channel.unary_unary(
                '/va.VoiceAssistantService/HealthCheck',
                request_serializer=va__pb2.HealthCheckRequest.SerializeToString,
                response_deserializer=va__pb2.HealthCheckResponse.FromString,
                _registered_method=True)


class VoiceAssistantServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ProcessAudio(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def HealthCheck(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VoiceAssistantServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ProcessAudio': grpc.unary_unary_rpc_method_handler(
                    servicer.ProcessAudio,
                    request_deserializer=va__pb2.AudioRequest.FromString,
                    response_serializer=va__pb2.AudioResponse.SerializeToString,
            ),
            'HealthCheck': grpc.unary_unary_rpc_method_handler(
                    servicer.HealthCheck,
                    request_deserializer=va__pb2.HealthCheckRequest.FromString,
                    response_serializer=va__pb2.HealthCheckResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'va.VoiceAssistantService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('va.VoiceAssistantService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class VoiceAssistantService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ProcessAudio(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/va.VoiceAssistantService/ProcessAudio',
            va__pb2.AudioRequest.SerializeToString,
            va__pb2.AudioResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def HealthCheck(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/va.VoiceAssistantService/HealthCheck',
            va__pb2.HealthCheckRequest.SerializeToString,
            va__pb2.HealthCheckResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
