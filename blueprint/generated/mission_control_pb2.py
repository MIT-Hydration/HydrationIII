# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mission_control.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='mission_control.proto',
  package='mission_control',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x15mission_control.proto\x12\x0fmission_control\"-\n\x10HeartBeatRequest\x12\x19\n\x11request_timestamp\x18\x01 \x01(\r\"\xaa\x01\n\x0eHeartBeatReply\x12\x11\n\ttimestamp\x18\x01 \x01(\r\x12\x19\n\x11request_timestamp\x18\x02 \x01(\r\x12\x1e\n\x16\x64rill_subsystem_online\x18\x03 \x01(\x08\x12\x1f\n\x17heater_sussystem_online\x18\x04 \x01(\x08\x12)\n\x04mode\x18\x05 \x01(\x0e\x32\x1b.mission_control.SystemMode\"6\n\x19\x44rillSensorsStatusRequest\x12\x19\n\x11request_timestamp\x18\x01 \x01(\r\"p\n\x1a\x44rillSensorsStatusResponse\x12\x11\n\ttimestamp\x18\x01 \x01(\r\x12\x19\n\x11request_timestamp\x18\x02 \x01(\r\x12\x10\n\x08\x64rill_on\x18\x03 \x01(\x08\x12\x12\n\ntachometer\x18\x04 \x01(\x02\"B\n\x13\x44rillCommandRequest\x12\x19\n\x11request_timestamp\x18\x01 \x01(\r\x12\x10\n\x08\x64rill_on\x18\x02 \x01(\x08\"t\n\x14\x44rillCommandResponse\x12\x11\n\ttimestamp\x18\x01 \x01(\r\x12\x19\n\x11request_timestamp\x18\x02 \x01(\r\x12.\n\x06status\x18\x03 \x01(\x0e\x32\x1e.mission_control.CommandReport*\\\n\nSystemMode\x12\x0b\n\x07UNKNOWN\x10\x00\x12\t\n\x05READY\x10\x01\x12\x0f\n\x0b\x43\x41LIBRATING\x10\x02\x12\n\n\x06MANUAL\x10\x03\x12\x0c\n\x08\x44RILLING\x10\x04\x12\x0b\n\x07HEATING\x10\x05*E\n\rCommandReport\x12\x0c\n\x08\x45XECUTED\x10\x00\x12\x11\n\rINVALID_STATE\x10\x01\x12\x13\n\x0f\x45XECUTION_ERROR\x10\x02\x32\xac\x02\n\x0eMissionControl\x12O\n\tHeartBeat\x12!.mission_control.HeartBeatRequest\x1a\x1f.mission_control.HeartBeatReply\x12l\n\x11\x44rillSensorStatus\x12*.mission_control.DrillSensorsStatusRequest\x1a+.mission_control.DrillSensorsStatusResponse\x12[\n\x0c\x44rillCommand\x12$.mission_control.DrillCommandRequest\x1a%.mission_control.DrillCommandResponse2\xaa\x02\n\x0c\x44rillControl\x12O\n\tHeartBeat\x12!.mission_control.HeartBeatRequest\x1a\x1f.mission_control.HeartBeatReply\x12l\n\x11\x44rillSensorStatus\x12*.mission_control.DrillSensorsStatusRequest\x1a+.mission_control.DrillSensorsStatusResponse\x12[\n\x0c\x44rillCommand\x12$.mission_control.DrillCommandRequest\x1a%.mission_control.DrillCommandResponseb\x06proto3'
)

_SYSTEMMODE = _descriptor.EnumDescriptor(
  name='SystemMode',
  full_name='mission_control.SystemMode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='READY', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CALIBRATING', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MANUAL', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DRILLING', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='HEATING', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=618,
  serialized_end=710,
)
_sym_db.RegisterEnumDescriptor(_SYSTEMMODE)

SystemMode = enum_type_wrapper.EnumTypeWrapper(_SYSTEMMODE)
_COMMANDREPORT = _descriptor.EnumDescriptor(
  name='CommandReport',
  full_name='mission_control.CommandReport',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='EXECUTED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_STATE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EXECUTION_ERROR', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=712,
  serialized_end=781,
)
_sym_db.RegisterEnumDescriptor(_COMMANDREPORT)

CommandReport = enum_type_wrapper.EnumTypeWrapper(_COMMANDREPORT)
UNKNOWN = 0
READY = 1
CALIBRATING = 2
MANUAL = 3
DRILLING = 4
HEATING = 5
EXECUTED = 0
INVALID_STATE = 1
EXECUTION_ERROR = 2



_HEARTBEATREQUEST = _descriptor.Descriptor(
  name='HeartBeatRequest',
  full_name='mission_control.HeartBeatRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.HeartBeatRequest.request_timestamp', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=42,
  serialized_end=87,
)


_HEARTBEATREPLY = _descriptor.Descriptor(
  name='HeartBeatReply',
  full_name='mission_control.HeartBeatReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='mission_control.HeartBeatReply.timestamp', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.HeartBeatReply.request_timestamp', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='drill_subsystem_online', full_name='mission_control.HeartBeatReply.drill_subsystem_online', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='heater_sussystem_online', full_name='mission_control.HeartBeatReply.heater_sussystem_online', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mode', full_name='mission_control.HeartBeatReply.mode', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=90,
  serialized_end=260,
)


_DRILLSENSORSSTATUSREQUEST = _descriptor.Descriptor(
  name='DrillSensorsStatusRequest',
  full_name='mission_control.DrillSensorsStatusRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.DrillSensorsStatusRequest.request_timestamp', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=262,
  serialized_end=316,
)


_DRILLSENSORSSTATUSRESPONSE = _descriptor.Descriptor(
  name='DrillSensorsStatusResponse',
  full_name='mission_control.DrillSensorsStatusResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='mission_control.DrillSensorsStatusResponse.timestamp', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.DrillSensorsStatusResponse.request_timestamp', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='drill_on', full_name='mission_control.DrillSensorsStatusResponse.drill_on', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tachometer', full_name='mission_control.DrillSensorsStatusResponse.tachometer', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=318,
  serialized_end=430,
)


_DRILLCOMMANDREQUEST = _descriptor.Descriptor(
  name='DrillCommandRequest',
  full_name='mission_control.DrillCommandRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.DrillCommandRequest.request_timestamp', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='drill_on', full_name='mission_control.DrillCommandRequest.drill_on', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=432,
  serialized_end=498,
)


_DRILLCOMMANDRESPONSE = _descriptor.Descriptor(
  name='DrillCommandResponse',
  full_name='mission_control.DrillCommandResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='mission_control.DrillCommandResponse.timestamp', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.DrillCommandResponse.request_timestamp', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='mission_control.DrillCommandResponse.status', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=500,
  serialized_end=616,
)

_HEARTBEATREPLY.fields_by_name['mode'].enum_type = _SYSTEMMODE
_DRILLCOMMANDRESPONSE.fields_by_name['status'].enum_type = _COMMANDREPORT
DESCRIPTOR.message_types_by_name['HeartBeatRequest'] = _HEARTBEATREQUEST
DESCRIPTOR.message_types_by_name['HeartBeatReply'] = _HEARTBEATREPLY
DESCRIPTOR.message_types_by_name['DrillSensorsStatusRequest'] = _DRILLSENSORSSTATUSREQUEST
DESCRIPTOR.message_types_by_name['DrillSensorsStatusResponse'] = _DRILLSENSORSSTATUSRESPONSE
DESCRIPTOR.message_types_by_name['DrillCommandRequest'] = _DRILLCOMMANDREQUEST
DESCRIPTOR.message_types_by_name['DrillCommandResponse'] = _DRILLCOMMANDRESPONSE
DESCRIPTOR.enum_types_by_name['SystemMode'] = _SYSTEMMODE
DESCRIPTOR.enum_types_by_name['CommandReport'] = _COMMANDREPORT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HeartBeatRequest = _reflection.GeneratedProtocolMessageType('HeartBeatRequest', (_message.Message,), {
  'DESCRIPTOR' : _HEARTBEATREQUEST,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.HeartBeatRequest)
  })
_sym_db.RegisterMessage(HeartBeatRequest)

HeartBeatReply = _reflection.GeneratedProtocolMessageType('HeartBeatReply', (_message.Message,), {
  'DESCRIPTOR' : _HEARTBEATREPLY,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.HeartBeatReply)
  })
_sym_db.RegisterMessage(HeartBeatReply)

DrillSensorsStatusRequest = _reflection.GeneratedProtocolMessageType('DrillSensorsStatusRequest', (_message.Message,), {
  'DESCRIPTOR' : _DRILLSENSORSSTATUSREQUEST,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.DrillSensorsStatusRequest)
  })
_sym_db.RegisterMessage(DrillSensorsStatusRequest)

DrillSensorsStatusResponse = _reflection.GeneratedProtocolMessageType('DrillSensorsStatusResponse', (_message.Message,), {
  'DESCRIPTOR' : _DRILLSENSORSSTATUSRESPONSE,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.DrillSensorsStatusResponse)
  })
_sym_db.RegisterMessage(DrillSensorsStatusResponse)

DrillCommandRequest = _reflection.GeneratedProtocolMessageType('DrillCommandRequest', (_message.Message,), {
  'DESCRIPTOR' : _DRILLCOMMANDREQUEST,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.DrillCommandRequest)
  })
_sym_db.RegisterMessage(DrillCommandRequest)

DrillCommandResponse = _reflection.GeneratedProtocolMessageType('DrillCommandResponse', (_message.Message,), {
  'DESCRIPTOR' : _DRILLCOMMANDRESPONSE,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.DrillCommandResponse)
  })
_sym_db.RegisterMessage(DrillCommandResponse)



_MISSIONCONTROL = _descriptor.ServiceDescriptor(
  name='MissionControl',
  full_name='mission_control.MissionControl',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=784,
  serialized_end=1084,
  methods=[
  _descriptor.MethodDescriptor(
    name='HeartBeat',
    full_name='mission_control.MissionControl.HeartBeat',
    index=0,
    containing_service=None,
    input_type=_HEARTBEATREQUEST,
    output_type=_HEARTBEATREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DrillSensorStatus',
    full_name='mission_control.MissionControl.DrillSensorStatus',
    index=1,
    containing_service=None,
    input_type=_DRILLSENSORSSTATUSREQUEST,
    output_type=_DRILLSENSORSSTATUSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DrillCommand',
    full_name='mission_control.MissionControl.DrillCommand',
    index=2,
    containing_service=None,
    input_type=_DRILLCOMMANDREQUEST,
    output_type=_DRILLCOMMANDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_MISSIONCONTROL)

DESCRIPTOR.services_by_name['MissionControl'] = _MISSIONCONTROL


_DRILLCONTROL = _descriptor.ServiceDescriptor(
  name='DrillControl',
  full_name='mission_control.DrillControl',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1087,
  serialized_end=1385,
  methods=[
  _descriptor.MethodDescriptor(
    name='HeartBeat',
    full_name='mission_control.DrillControl.HeartBeat',
    index=0,
    containing_service=None,
    input_type=_HEARTBEATREQUEST,
    output_type=_HEARTBEATREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DrillSensorStatus',
    full_name='mission_control.DrillControl.DrillSensorStatus',
    index=1,
    containing_service=None,
    input_type=_DRILLSENSORSSTATUSREQUEST,
    output_type=_DRILLSENSORSSTATUSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DrillCommand',
    full_name='mission_control.DrillControl.DrillCommand',
    index=2,
    containing_service=None,
    input_type=_DRILLCOMMANDREQUEST,
    output_type=_DRILLCOMMANDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_DRILLCONTROL)

DESCRIPTOR.services_by_name['DrillControl'] = _DRILLCONTROL

# @@protoc_insertion_point(module_scope)
