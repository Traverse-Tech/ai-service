# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: va.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'va.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x08va.proto\x12\x02va\"6\n\x0c\x41udioRequest\x12\x12\n\naudio_data\x18\x01 \x01(\x0c\x12\x12\n\nsession_id\x18\x02 \x01(\t\"n\n\rAudioResponse\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x18\n\x10transcribed_text\x18\x02 \x01(\t\x12\x13\n\x0b\x61i_response\x18\x03 \x01(\t\x12\x1a\n\x12\x61udio_response_url\x18\x04 \x01(\t\"\x14\n\x12HealthCheckRequest\"&\n\x13HealthCheckResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2\x8c\x01\n\x15VoiceAssistantService\x12\x33\n\x0cProcessAudio\x12\x10.va.AudioRequest\x1a\x11.va.AudioResponse\x12>\n\x0bHealthCheck\x12\x16.va.HealthCheckRequest\x1a\x17.va.HealthCheckResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'va_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_AUDIOREQUEST']._serialized_start=16
  _globals['_AUDIOREQUEST']._serialized_end=70
  _globals['_AUDIORESPONSE']._serialized_start=72
  _globals['_AUDIORESPONSE']._serialized_end=182
  _globals['_HEALTHCHECKREQUEST']._serialized_start=184
  _globals['_HEALTHCHECKREQUEST']._serialized_end=204
  _globals['_HEALTHCHECKRESPONSE']._serialized_start=206
  _globals['_HEALTHCHECKRESPONSE']._serialized_end=244
  _globals['_VOICEASSISTANTSERVICE']._serialized_start=247
  _globals['_VOICEASSISTANTSERVICE']._serialized_end=387
# @@protoc_insertion_point(module_scope)
