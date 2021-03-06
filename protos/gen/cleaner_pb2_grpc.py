# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import cleaner_pb2 as cleaner__pb2
from . import extractor_pb2 as extractor__pb2


class CleanServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.clean = channel.unary_unary(
                '/CleanService/clean',
                request_serializer=extractor__pb2.ExtractInfo.SerializeToString,
                response_deserializer=cleaner__pb2.CleanInfo.FromString,
                )


class CleanServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def clean(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CleanServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'clean': grpc.unary_unary_rpc_method_handler(
                    servicer.clean,
                    request_deserializer=extractor__pb2.ExtractInfo.FromString,
                    response_serializer=cleaner__pb2.CleanInfo.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'CleanService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CleanService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def clean(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CleanService/clean',
            extractor__pb2.ExtractInfo.SerializeToString,
            cleaner__pb2.CleanInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
