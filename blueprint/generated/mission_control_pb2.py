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
  serialized_pb=b'\n\x15mission_control.proto\x12\x0fmission_control\"-\n\x10HeartBeatRequest\x12\x19\n\x11request_timestamp\x18\x01 \x01(\x04\"\xce\x02\n\x0eHeartBeatReply\x12\x11\n\ttimestamp\x18\x01 \x01(\x04\x12\x19\n\x11request_timestamp\x18\x02 \x01(\x04\x12\"\n\x19number_of_servos_detected\x18\xe9\x07 \x01(\r\x12\x1c\n\x14\x63pu_temperature_degC\x18\x06 \x01(\x02\x12*\n\x05state\x18G \x01(\x0e\x32\x1b.mission_control.SystemMode\x12/\n\nmajor_mode\x18\x46 \x01(\x0e\x32\x1b.mission_control.SystemMode\x12\x17\n\x0fmission_time_ms\x18\x08 \x01(\x04\x12\x1b\n\x13zdrill_servo_moving\x18\t \x01(\x08\x12\x16\n\x0ey_servo_moving\x18\x0c \x01(\x08\x12\r\n\x05rig_y\x18\x65 \x01(\x02\x12\x12\n\nrig_zdrill\x18\x66 \x01(\x02\"W\n\x06Limits\x12\x19\n\x11request_timestamp\x18\x01 \x01(\x04\x12\x0f\n\x07\x61ir_gap\x18\x02 \x01(\x02\x12\x0e\n\x06max_z1\x18\x03 \x01(\x02\x12\x11\n\tice_depth\x18\x04 \x01(\x02\",\n\x0fGetLimitRequest\x12\x19\n\x11request_timestamp\x18\x01 \x01(\x04\"7\n\x0bMoveRequest\x12\x19\n\x11request_timestamp\x18\x01 \x01(\x04\x12\r\n\x05\x64\x65lta\x18\x02 \x01(\x02\"o\n\x0f\x43ommandResponse\x12\x11\n\ttimestamp\x18\x01 \x01(\x04\x12\x19\n\x11request_timestamp\x18\x02 \x01(\x04\x12.\n\x06status\x18\x03 \x01(\x0e\x32\x1e.mission_control.CommandReport\"1\n\x14\x45mergencyStopRequest\x12\x19\n\x11request_timestamp\x18\x01 \x01(\x04\"0\n\x13StartCommandRequest\x12\x19\n\x11request_timestamp\x18\x01 \x01(\x04\"1\n\x14GetMajorModesRequest\x12\x19\n\x11request_timestamp\x18\x01 \x01(\x04\"b\n\x0eMajorModesList\x12\x11\n\ttimestamp\x18\x01 \x01(\x04\x12\x19\n\x11request_timestamp\x18\x02 \x01(\x04\x12\r\n\x05modes\x18\x03 \x03(\x05\x12\x13\n\x0bmode_labels\x18\x04 \x03(\t\",\n\x0fHoleListRequest\x12\x19\n\x11request_timestamp\x18\x01 \x01(\x04\"\x98\x01\n\x08HoleList\x12\x11\n\ttimestamp\x18\x01 \x01(\x04\x12\x19\n\x11request_timestamp\x18\x02 \x01(\x04\x12\r\n\x05order\x18\x03 \x03(\x05\x12\x0b\n\x03x_m\x18\x04 \x03(\x02\x12\x0b\n\x03y_m\x18\x05 \x03(\x02\x12\x0f\n\x07max_z_m\x18\x06 \x03(\x02\x12\x10\n\x08water_ml\x18\x07 \x03(\x02\x12\x12\n\ndiameter_m\x18\x08 \x03(\x02*\xb6\x03\n\nSystemMode\x12\x0b\n\x07UNKNOWN\x10\x00\x12\"\n\x1eMAJOR_MODE_STARTUP_DIAGNOSTICS\x10\x64\x12\x1e\n\x19MAJOR_MODE_DRILL_BOREHOLE\x10\x90\x03\x12\x10\n\x0cSTARTUP_IDLE\x10\x65\x12!\n\x1dSTARTUP_MISSION_CLOCK_STARTED\x10\x66\x12\x15\n\x11STARTUP_HOMING_Z1\x10g\x12\x1d\n\x19STARTUP_HOME_Z1_COMPLETED\x10h\x12\x14\n\x10STARTUP_HOMING_Y\x10i\x12\x1c\n\x18STARTUP_HOME_Y_COMPLETED\x10j\x12\x0f\n\nDRILL_IDLE\x10\x91\x03\x12\x13\n\x0e\x44RILL_MOVING_Y\x10\x92\x03\x12\x1b\n\x16\x44RILL_MOVE_Y_COMPLETED\x10\x93\x03\x12\x17\n\x12\x44RILLING_HOLE_IDLE\x10\x94\x03\x12 \n\x1b\x44RILLING_HOLE_DRILLING_DOWN\x10\x95\x03\x12\x1d\n\x18\x44RILLING_HOLE_REAMING_UP\x10\x96\x03\x12\x1b\n\x16\x44RILLING_HOLE_HOMING_Y\x10\x97\x03*E\n\rCommandReport\x12\x0c\n\x08\x45XECUTED\x10\x00\x12\x11\n\rINVALID_STATE\x10\x01\x12\x13\n\x0f\x45XECUTION_ERROR\x10\x02\x32\x80\x07\n\x0eMissionControl\x12W\n\rGetMajorModes\x12%.mission_control.GetMajorModesRequest\x1a\x1f.mission_control.MajorModesList\x12O\n\tHeartBeat\x12!.mission_control.HeartBeatRequest\x1a\x1f.mission_control.HeartBeatReply\x12\x46\n\tGetLimits\x12 .mission_control.GetLimitRequest\x1a\x17.mission_control.Limits\x12\x46\n\tSetLimits\x12\x17.mission_control.Limits\x1a .mission_control.CommandResponse\x12G\n\x08GetHoles\x12 .mission_control.HoleListRequest\x1a\x19.mission_control.HoleList\x12U\n\x0bStartupNext\x12$.mission_control.StartCommandRequest\x1a .mission_control.CommandResponse\x12S\n\tSetHomeZ1\x12$.mission_control.StartCommandRequest\x1a .mission_control.CommandResponse\x12R\n\x08SetHomeY\x12$.mission_control.StartCommandRequest\x1a .mission_control.CommandResponse\x12H\n\x06Z1Move\x12\x1c.mission_control.MoveRequest\x1a .mission_control.CommandResponse\x12G\n\x05YMove\x12\x1c.mission_control.MoveRequest\x1a .mission_control.CommandResponse\x12X\n\rEmergencyStop\x12%.mission_control.EmergencyStopRequest\x1a .mission_control.CommandResponseb\x06proto3'
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
      name='MAJOR_MODE_STARTUP_DIAGNOSTICS', index=1, number=100,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MAJOR_MODE_DRILL_BOREHOLE', index=2, number=400,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STARTUP_IDLE', index=3, number=101,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STARTUP_MISSION_CLOCK_STARTED', index=4, number=102,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STARTUP_HOMING_Z1', index=5, number=103,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STARTUP_HOME_Z1_COMPLETED', index=6, number=104,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STARTUP_HOMING_Y', index=7, number=105,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STARTUP_HOME_Y_COMPLETED', index=8, number=106,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DRILL_IDLE', index=9, number=401,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DRILL_MOVING_Y', index=10, number=402,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DRILL_MOVE_Y_COMPLETED', index=11, number=403,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DRILLING_HOLE_IDLE', index=12, number=404,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DRILLING_HOLE_DRILLING_DOWN', index=13, number=405,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DRILLING_HOLE_REAMING_UP', index=14, number=406,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DRILLING_HOLE_HOMING_Y', index=15, number=407,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1185,
  serialized_end=1623,
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
  serialized_start=1625,
  serialized_end=1694,
)
_sym_db.RegisterEnumDescriptor(_COMMANDREPORT)

CommandReport = enum_type_wrapper.EnumTypeWrapper(_COMMANDREPORT)
UNKNOWN = 0
MAJOR_MODE_STARTUP_DIAGNOSTICS = 100
MAJOR_MODE_DRILL_BOREHOLE = 400
STARTUP_IDLE = 101
STARTUP_MISSION_CLOCK_STARTED = 102
STARTUP_HOMING_Z1 = 103
STARTUP_HOME_Z1_COMPLETED = 104
STARTUP_HOMING_Y = 105
STARTUP_HOME_Y_COMPLETED = 106
DRILL_IDLE = 401
DRILL_MOVING_Y = 402
DRILL_MOVE_Y_COMPLETED = 403
DRILLING_HOLE_IDLE = 404
DRILLING_HOLE_DRILLING_DOWN = 405
DRILLING_HOLE_REAMING_UP = 406
DRILLING_HOLE_HOMING_Y = 407
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
      number=1, type=4, cpp_type=4, label=1,
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
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.HeartBeatReply.request_timestamp', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='number_of_servos_detected', full_name='mission_control.HeartBeatReply.number_of_servos_detected', index=2,
      number=1001, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cpu_temperature_degC', full_name='mission_control.HeartBeatReply.cpu_temperature_degC', index=3,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='state', full_name='mission_control.HeartBeatReply.state', index=4,
      number=71, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='major_mode', full_name='mission_control.HeartBeatReply.major_mode', index=5,
      number=70, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mission_time_ms', full_name='mission_control.HeartBeatReply.mission_time_ms', index=6,
      number=8, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='zdrill_servo_moving', full_name='mission_control.HeartBeatReply.zdrill_servo_moving', index=7,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='y_servo_moving', full_name='mission_control.HeartBeatReply.y_servo_moving', index=8,
      number=12, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rig_y', full_name='mission_control.HeartBeatReply.rig_y', index=9,
      number=101, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rig_zdrill', full_name='mission_control.HeartBeatReply.rig_zdrill', index=10,
      number=102, type=2, cpp_type=6, label=1,
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
  serialized_start=90,
  serialized_end=424,
)


_LIMITS = _descriptor.Descriptor(
  name='Limits',
  full_name='mission_control.Limits',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.Limits.request_timestamp', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='air_gap', full_name='mission_control.Limits.air_gap', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_z1', full_name='mission_control.Limits.max_z1', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ice_depth', full_name='mission_control.Limits.ice_depth', index=3,
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
  serialized_start=426,
  serialized_end=513,
)


_GETLIMITREQUEST = _descriptor.Descriptor(
  name='GetLimitRequest',
  full_name='mission_control.GetLimitRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.GetLimitRequest.request_timestamp', index=0,
      number=1, type=4, cpp_type=4, label=1,
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
  serialized_start=515,
  serialized_end=559,
)


_MOVEREQUEST = _descriptor.Descriptor(
  name='MoveRequest',
  full_name='mission_control.MoveRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.MoveRequest.request_timestamp', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='delta', full_name='mission_control.MoveRequest.delta', index=1,
      number=2, type=2, cpp_type=6, label=1,
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
  serialized_start=561,
  serialized_end=616,
)


_COMMANDRESPONSE = _descriptor.Descriptor(
  name='CommandResponse',
  full_name='mission_control.CommandResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='mission_control.CommandResponse.timestamp', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.CommandResponse.request_timestamp', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='mission_control.CommandResponse.status', index=2,
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
  serialized_start=618,
  serialized_end=729,
)


_EMERGENCYSTOPREQUEST = _descriptor.Descriptor(
  name='EmergencyStopRequest',
  full_name='mission_control.EmergencyStopRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.EmergencyStopRequest.request_timestamp', index=0,
      number=1, type=4, cpp_type=4, label=1,
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
  serialized_start=731,
  serialized_end=780,
)


_STARTCOMMANDREQUEST = _descriptor.Descriptor(
  name='StartCommandRequest',
  full_name='mission_control.StartCommandRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.StartCommandRequest.request_timestamp', index=0,
      number=1, type=4, cpp_type=4, label=1,
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
  serialized_start=782,
  serialized_end=830,
)


_GETMAJORMODESREQUEST = _descriptor.Descriptor(
  name='GetMajorModesRequest',
  full_name='mission_control.GetMajorModesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.GetMajorModesRequest.request_timestamp', index=0,
      number=1, type=4, cpp_type=4, label=1,
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
  serialized_start=832,
  serialized_end=881,
)


_MAJORMODESLIST = _descriptor.Descriptor(
  name='MajorModesList',
  full_name='mission_control.MajorModesList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='mission_control.MajorModesList.timestamp', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.MajorModesList.request_timestamp', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='modes', full_name='mission_control.MajorModesList.modes', index=2,
      number=3, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mode_labels', full_name='mission_control.MajorModesList.mode_labels', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=883,
  serialized_end=981,
)


_HOLELISTREQUEST = _descriptor.Descriptor(
  name='HoleListRequest',
  full_name='mission_control.HoleListRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.HoleListRequest.request_timestamp', index=0,
      number=1, type=4, cpp_type=4, label=1,
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
  serialized_start=983,
  serialized_end=1027,
)


_HOLELIST = _descriptor.Descriptor(
  name='HoleList',
  full_name='mission_control.HoleList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='mission_control.HoleList.timestamp', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='mission_control.HoleList.request_timestamp', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='order', full_name='mission_control.HoleList.order', index=2,
      number=3, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='x_m', full_name='mission_control.HoleList.x_m', index=3,
      number=4, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='y_m', full_name='mission_control.HoleList.y_m', index=4,
      number=5, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_z_m', full_name='mission_control.HoleList.max_z_m', index=5,
      number=6, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='water_ml', full_name='mission_control.HoleList.water_ml', index=6,
      number=7, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='diameter_m', full_name='mission_control.HoleList.diameter_m', index=7,
      number=8, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=1030,
  serialized_end=1182,
)

_HEARTBEATREPLY.fields_by_name['state'].enum_type = _SYSTEMMODE
_HEARTBEATREPLY.fields_by_name['major_mode'].enum_type = _SYSTEMMODE
_COMMANDRESPONSE.fields_by_name['status'].enum_type = _COMMANDREPORT
DESCRIPTOR.message_types_by_name['HeartBeatRequest'] = _HEARTBEATREQUEST
DESCRIPTOR.message_types_by_name['HeartBeatReply'] = _HEARTBEATREPLY
DESCRIPTOR.message_types_by_name['Limits'] = _LIMITS
DESCRIPTOR.message_types_by_name['GetLimitRequest'] = _GETLIMITREQUEST
DESCRIPTOR.message_types_by_name['MoveRequest'] = _MOVEREQUEST
DESCRIPTOR.message_types_by_name['CommandResponse'] = _COMMANDRESPONSE
DESCRIPTOR.message_types_by_name['EmergencyStopRequest'] = _EMERGENCYSTOPREQUEST
DESCRIPTOR.message_types_by_name['StartCommandRequest'] = _STARTCOMMANDREQUEST
DESCRIPTOR.message_types_by_name['GetMajorModesRequest'] = _GETMAJORMODESREQUEST
DESCRIPTOR.message_types_by_name['MajorModesList'] = _MAJORMODESLIST
DESCRIPTOR.message_types_by_name['HoleListRequest'] = _HOLELISTREQUEST
DESCRIPTOR.message_types_by_name['HoleList'] = _HOLELIST
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

Limits = _reflection.GeneratedProtocolMessageType('Limits', (_message.Message,), {
  'DESCRIPTOR' : _LIMITS,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.Limits)
  })
_sym_db.RegisterMessage(Limits)

GetLimitRequest = _reflection.GeneratedProtocolMessageType('GetLimitRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETLIMITREQUEST,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.GetLimitRequest)
  })
_sym_db.RegisterMessage(GetLimitRequest)

MoveRequest = _reflection.GeneratedProtocolMessageType('MoveRequest', (_message.Message,), {
  'DESCRIPTOR' : _MOVEREQUEST,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.MoveRequest)
  })
_sym_db.RegisterMessage(MoveRequest)

CommandResponse = _reflection.GeneratedProtocolMessageType('CommandResponse', (_message.Message,), {
  'DESCRIPTOR' : _COMMANDRESPONSE,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.CommandResponse)
  })
_sym_db.RegisterMessage(CommandResponse)

EmergencyStopRequest = _reflection.GeneratedProtocolMessageType('EmergencyStopRequest', (_message.Message,), {
  'DESCRIPTOR' : _EMERGENCYSTOPREQUEST,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.EmergencyStopRequest)
  })
_sym_db.RegisterMessage(EmergencyStopRequest)

StartCommandRequest = _reflection.GeneratedProtocolMessageType('StartCommandRequest', (_message.Message,), {
  'DESCRIPTOR' : _STARTCOMMANDREQUEST,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.StartCommandRequest)
  })
_sym_db.RegisterMessage(StartCommandRequest)

GetMajorModesRequest = _reflection.GeneratedProtocolMessageType('GetMajorModesRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETMAJORMODESREQUEST,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.GetMajorModesRequest)
  })
_sym_db.RegisterMessage(GetMajorModesRequest)

MajorModesList = _reflection.GeneratedProtocolMessageType('MajorModesList', (_message.Message,), {
  'DESCRIPTOR' : _MAJORMODESLIST,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.MajorModesList)
  })
_sym_db.RegisterMessage(MajorModesList)

HoleListRequest = _reflection.GeneratedProtocolMessageType('HoleListRequest', (_message.Message,), {
  'DESCRIPTOR' : _HOLELISTREQUEST,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.HoleListRequest)
  })
_sym_db.RegisterMessage(HoleListRequest)

HoleList = _reflection.GeneratedProtocolMessageType('HoleList', (_message.Message,), {
  'DESCRIPTOR' : _HOLELIST,
  '__module__' : 'mission_control_pb2'
  # @@protoc_insertion_point(class_scope:mission_control.HoleList)
  })
_sym_db.RegisterMessage(HoleList)



_MISSIONCONTROL = _descriptor.ServiceDescriptor(
  name='MissionControl',
  full_name='mission_control.MissionControl',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1697,
  serialized_end=2593,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetMajorModes',
    full_name='mission_control.MissionControl.GetMajorModes',
    index=0,
    containing_service=None,
    input_type=_GETMAJORMODESREQUEST,
    output_type=_MAJORMODESLIST,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='HeartBeat',
    full_name='mission_control.MissionControl.HeartBeat',
    index=1,
    containing_service=None,
    input_type=_HEARTBEATREQUEST,
    output_type=_HEARTBEATREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetLimits',
    full_name='mission_control.MissionControl.GetLimits',
    index=2,
    containing_service=None,
    input_type=_GETLIMITREQUEST,
    output_type=_LIMITS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SetLimits',
    full_name='mission_control.MissionControl.SetLimits',
    index=3,
    containing_service=None,
    input_type=_LIMITS,
    output_type=_COMMANDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetHoles',
    full_name='mission_control.MissionControl.GetHoles',
    index=4,
    containing_service=None,
    input_type=_HOLELISTREQUEST,
    output_type=_HOLELIST,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='StartupNext',
    full_name='mission_control.MissionControl.StartupNext',
    index=5,
    containing_service=None,
    input_type=_STARTCOMMANDREQUEST,
    output_type=_COMMANDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SetHomeZ1',
    full_name='mission_control.MissionControl.SetHomeZ1',
    index=6,
    containing_service=None,
    input_type=_STARTCOMMANDREQUEST,
    output_type=_COMMANDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SetHomeY',
    full_name='mission_control.MissionControl.SetHomeY',
    index=7,
    containing_service=None,
    input_type=_STARTCOMMANDREQUEST,
    output_type=_COMMANDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Z1Move',
    full_name='mission_control.MissionControl.Z1Move',
    index=8,
    containing_service=None,
    input_type=_MOVEREQUEST,
    output_type=_COMMANDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='YMove',
    full_name='mission_control.MissionControl.YMove',
    index=9,
    containing_service=None,
    input_type=_MOVEREQUEST,
    output_type=_COMMANDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='EmergencyStop',
    full_name='mission_control.MissionControl.EmergencyStop',
    index=10,
    containing_service=None,
    input_type=_EMERGENCYSTOPREQUEST,
    output_type=_COMMANDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_MISSIONCONTROL)

DESCRIPTOR.services_by_name['MissionControl'] = _MISSIONCONTROL

# @@protoc_insertion_point(module_scope)
