# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import mission_control_pb2 as mission__control__pb2


class MissionControlStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetMajorModes = channel.unary_unary(
                '/mission_control.MissionControl/GetMajorModes',
                request_serializer=mission__control__pb2.GetMajorModesRequest.SerializeToString,
                response_deserializer=mission__control__pb2.MajorModesList.FromString,
                )
        self.HeartBeat = channel.unary_unary(
                '/mission_control.MissionControl/HeartBeat',
                request_serializer=mission__control__pb2.HeartBeatRequest.SerializeToString,
                response_deserializer=mission__control__pb2.HeartBeatReply.FromString,
                )
        self.GetLimits = channel.unary_unary(
                '/mission_control.MissionControl/GetLimits',
                request_serializer=mission__control__pb2.GetLimitRequest.SerializeToString,
                response_deserializer=mission__control__pb2.Limits.FromString,
                )
        self.SetLimits = channel.unary_unary(
                '/mission_control.MissionControl/SetLimits',
                request_serializer=mission__control__pb2.Limits.SerializeToString,
                response_deserializer=mission__control__pb2.CommandResponse.FromString,
                )
        self.StartupNext = channel.unary_unary(
                '/mission_control.MissionControl/StartupNext',
                request_serializer=mission__control__pb2.StartCommandRequest.SerializeToString,
                response_deserializer=mission__control__pb2.CommandResponse.FromString,
                )
        self.SetHomeZ1 = channel.unary_unary(
                '/mission_control.MissionControl/SetHomeZ1',
                request_serializer=mission__control__pb2.StartCommandRequest.SerializeToString,
                response_deserializer=mission__control__pb2.CommandResponse.FromString,
                )
        self.SetHomeZ2 = channel.unary_unary(
                '/mission_control.MissionControl/SetHomeZ2',
                request_serializer=mission__control__pb2.StartCommandRequest.SerializeToString,
                response_deserializer=mission__control__pb2.CommandResponse.FromString,
                )
        self.SetHomeY = channel.unary_unary(
                '/mission_control.MissionControl/SetHomeY',
                request_serializer=mission__control__pb2.StartCommandRequest.SerializeToString,
                response_deserializer=mission__control__pb2.CommandResponse.FromString,
                )
        self.Z1Move = channel.unary_unary(
                '/mission_control.MissionControl/Z1Move',
                request_serializer=mission__control__pb2.MoveRequest.SerializeToString,
                response_deserializer=mission__control__pb2.CommandResponse.FromString,
                )
        self.Z2Move = channel.unary_unary(
                '/mission_control.MissionControl/Z2Move',
                request_serializer=mission__control__pb2.MoveRequest.SerializeToString,
                response_deserializer=mission__control__pb2.CommandResponse.FromString,
                )
        self.YMove = channel.unary_unary(
                '/mission_control.MissionControl/YMove',
                request_serializer=mission__control__pb2.MoveRequest.SerializeToString,
                response_deserializer=mission__control__pb2.CommandResponse.FromString,
                )
        self.StartDrillHole = channel.unary_unary(
                '/mission_control.MissionControl/StartDrillHole',
                request_serializer=mission__control__pb2.StartCommandRequest.SerializeToString,
                response_deserializer=mission__control__pb2.CommandResponse.FromString,
                )
        self.EndDrillHole = channel.unary_unary(
                '/mission_control.MissionControl/EndDrillHole',
                request_serializer=mission__control__pb2.StartCommandRequest.SerializeToString,
                response_deserializer=mission__control__pb2.CommandResponse.FromString,
                )
        self.AlignHeater = channel.unary_unary(
                '/mission_control.MissionControl/AlignHeater',
                request_serializer=mission__control__pb2.StartCommandRequest.SerializeToString,
                response_deserializer=mission__control__pb2.CommandResponse.FromString,
                )
        self.GotoMajorMode = channel.unary_unary(
                '/mission_control.MissionControl/GotoMajorMode',
                request_serializer=mission__control__pb2.GotoMajorModesRequest.SerializeToString,
                response_deserializer=mission__control__pb2.CommandResponse.FromString,
                )
        self.EmergencyStop = channel.unary_unary(
                '/mission_control.MissionControl/EmergencyStop',
                request_serializer=mission__control__pb2.EmergencyStopRequest.SerializeToString,
                response_deserializer=mission__control__pb2.CommandResponse.FromString,
                )


class MissionControlServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetMajorModes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def HeartBeat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLimits(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetLimits(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartupNext(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetHomeZ1(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetHomeZ2(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetHomeY(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Z1Move(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Z2Move(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def YMove(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartDrillHole(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EndDrillHole(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AlignHeater(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GotoMajorMode(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EmergencyStop(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MissionControlServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetMajorModes': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMajorModes,
                    request_deserializer=mission__control__pb2.GetMajorModesRequest.FromString,
                    response_serializer=mission__control__pb2.MajorModesList.SerializeToString,
            ),
            'HeartBeat': grpc.unary_unary_rpc_method_handler(
                    servicer.HeartBeat,
                    request_deserializer=mission__control__pb2.HeartBeatRequest.FromString,
                    response_serializer=mission__control__pb2.HeartBeatReply.SerializeToString,
            ),
            'GetLimits': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLimits,
                    request_deserializer=mission__control__pb2.GetLimitRequest.FromString,
                    response_serializer=mission__control__pb2.Limits.SerializeToString,
            ),
            'SetLimits': grpc.unary_unary_rpc_method_handler(
                    servicer.SetLimits,
                    request_deserializer=mission__control__pb2.Limits.FromString,
                    response_serializer=mission__control__pb2.CommandResponse.SerializeToString,
            ),
            'StartupNext': grpc.unary_unary_rpc_method_handler(
                    servicer.StartupNext,
                    request_deserializer=mission__control__pb2.StartCommandRequest.FromString,
                    response_serializer=mission__control__pb2.CommandResponse.SerializeToString,
            ),
            'SetHomeZ1': grpc.unary_unary_rpc_method_handler(
                    servicer.SetHomeZ1,
                    request_deserializer=mission__control__pb2.StartCommandRequest.FromString,
                    response_serializer=mission__control__pb2.CommandResponse.SerializeToString,
            ),
            'SetHomeZ2': grpc.unary_unary_rpc_method_handler(
                    servicer.SetHomeZ2,
                    request_deserializer=mission__control__pb2.StartCommandRequest.FromString,
                    response_serializer=mission__control__pb2.CommandResponse.SerializeToString,
            ),
            'SetHomeY': grpc.unary_unary_rpc_method_handler(
                    servicer.SetHomeY,
                    request_deserializer=mission__control__pb2.StartCommandRequest.FromString,
                    response_serializer=mission__control__pb2.CommandResponse.SerializeToString,
            ),
            'Z1Move': grpc.unary_unary_rpc_method_handler(
                    servicer.Z1Move,
                    request_deserializer=mission__control__pb2.MoveRequest.FromString,
                    response_serializer=mission__control__pb2.CommandResponse.SerializeToString,
            ),
            'Z2Move': grpc.unary_unary_rpc_method_handler(
                    servicer.Z2Move,
                    request_deserializer=mission__control__pb2.MoveRequest.FromString,
                    response_serializer=mission__control__pb2.CommandResponse.SerializeToString,
            ),
            'YMove': grpc.unary_unary_rpc_method_handler(
                    servicer.YMove,
                    request_deserializer=mission__control__pb2.MoveRequest.FromString,
                    response_serializer=mission__control__pb2.CommandResponse.SerializeToString,
            ),
            'StartDrillHole': grpc.unary_unary_rpc_method_handler(
                    servicer.StartDrillHole,
                    request_deserializer=mission__control__pb2.StartCommandRequest.FromString,
                    response_serializer=mission__control__pb2.CommandResponse.SerializeToString,
            ),
            'EndDrillHole': grpc.unary_unary_rpc_method_handler(
                    servicer.EndDrillHole,
                    request_deserializer=mission__control__pb2.StartCommandRequest.FromString,
                    response_serializer=mission__control__pb2.CommandResponse.SerializeToString,
            ),
            'AlignHeater': grpc.unary_unary_rpc_method_handler(
                    servicer.AlignHeater,
                    request_deserializer=mission__control__pb2.StartCommandRequest.FromString,
                    response_serializer=mission__control__pb2.CommandResponse.SerializeToString,
            ),
            'GotoMajorMode': grpc.unary_unary_rpc_method_handler(
                    servicer.GotoMajorMode,
                    request_deserializer=mission__control__pb2.GotoMajorModesRequest.FromString,
                    response_serializer=mission__control__pb2.CommandResponse.SerializeToString,
            ),
            'EmergencyStop': grpc.unary_unary_rpc_method_handler(
                    servicer.EmergencyStop,
                    request_deserializer=mission__control__pb2.EmergencyStopRequest.FromString,
                    response_serializer=mission__control__pb2.CommandResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mission_control.MissionControl', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MissionControl(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetMajorModes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/GetMajorModes',
            mission__control__pb2.GetMajorModesRequest.SerializeToString,
            mission__control__pb2.MajorModesList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def HeartBeat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/HeartBeat',
            mission__control__pb2.HeartBeatRequest.SerializeToString,
            mission__control__pb2.HeartBeatReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetLimits(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/GetLimits',
            mission__control__pb2.GetLimitRequest.SerializeToString,
            mission__control__pb2.Limits.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetLimits(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/SetLimits',
            mission__control__pb2.Limits.SerializeToString,
            mission__control__pb2.CommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartupNext(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/StartupNext',
            mission__control__pb2.StartCommandRequest.SerializeToString,
            mission__control__pb2.CommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetHomeZ1(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/SetHomeZ1',
            mission__control__pb2.StartCommandRequest.SerializeToString,
            mission__control__pb2.CommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetHomeZ2(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/SetHomeZ2',
            mission__control__pb2.StartCommandRequest.SerializeToString,
            mission__control__pb2.CommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetHomeY(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/SetHomeY',
            mission__control__pb2.StartCommandRequest.SerializeToString,
            mission__control__pb2.CommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Z1Move(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/Z1Move',
            mission__control__pb2.MoveRequest.SerializeToString,
            mission__control__pb2.CommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Z2Move(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/Z2Move',
            mission__control__pb2.MoveRequest.SerializeToString,
            mission__control__pb2.CommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def YMove(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/YMove',
            mission__control__pb2.MoveRequest.SerializeToString,
            mission__control__pb2.CommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartDrillHole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/StartDrillHole',
            mission__control__pb2.StartCommandRequest.SerializeToString,
            mission__control__pb2.CommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EndDrillHole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/EndDrillHole',
            mission__control__pb2.StartCommandRequest.SerializeToString,
            mission__control__pb2.CommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AlignHeater(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/AlignHeater',
            mission__control__pb2.StartCommandRequest.SerializeToString,
            mission__control__pb2.CommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GotoMajorMode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/GotoMajorMode',
            mission__control__pb2.GotoMajorModesRequest.SerializeToString,
            mission__control__pb2.CommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EmergencyStop(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mission_control.MissionControl/EmergencyStop',
            mission__control__pb2.EmergencyStopRequest.SerializeToString,
            mission__control__pb2.CommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
