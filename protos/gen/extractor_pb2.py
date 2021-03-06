# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: extractor.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import downloader_pb2 as downloader__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='extractor.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0f\x65xtractor.proto\x1a\x10\x64ownloader.proto\"\x8d\x01\n\x0b\x45xtractInfo\x12\x10\n\x08\x62\x61tch_no\x18\x01 \x01(\t\x12\x0b\n\x03\x61pi\x18\x02 \x01(\t\x12\x11\n\tex_status\x18\x03 \x01(\t\x12\x15\n\rex_error_code\x18\x04 \x01(\t\x12\x10\n\x08topic_id\x18\x05 \x01(\x05\x12\r\n\x05links\x18\x06 \x01(\t\x12\x14\n\x0c\x65xtract_data\x18\x07 \x01(\t27\n\x0e\x45xtractService\x12%\n\x07\x65xtract\x12\x0c.DownloadRsp\x1a\x0c.ExtractInfob\x06proto3'
  ,
  dependencies=[downloader__pb2.DESCRIPTOR,])




_EXTRACTINFO = _descriptor.Descriptor(
  name='ExtractInfo',
  full_name='ExtractInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='batch_no', full_name='ExtractInfo.batch_no', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='api', full_name='ExtractInfo.api', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ex_status', full_name='ExtractInfo.ex_status', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ex_error_code', full_name='ExtractInfo.ex_error_code', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='topic_id', full_name='ExtractInfo.topic_id', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='links', full_name='ExtractInfo.links', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extract_data', full_name='ExtractInfo.extract_data', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=38,
  serialized_end=179,
)

DESCRIPTOR.message_types_by_name['ExtractInfo'] = _EXTRACTINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ExtractInfo = _reflection.GeneratedProtocolMessageType('ExtractInfo', (_message.Message,), {
  'DESCRIPTOR' : _EXTRACTINFO,
  '__module__' : 'extractor_pb2'
  # @@protoc_insertion_point(class_scope:ExtractInfo)
  })
_sym_db.RegisterMessage(ExtractInfo)



_EXTRACTSERVICE = _descriptor.ServiceDescriptor(
  name='ExtractService',
  full_name='ExtractService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=181,
  serialized_end=236,
  methods=[
  _descriptor.MethodDescriptor(
    name='extract',
    full_name='ExtractService.extract',
    index=0,
    containing_service=None,
    input_type=downloader__pb2._DOWNLOADRSP,
    output_type=_EXTRACTINFO,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_EXTRACTSERVICE)

DESCRIPTOR.services_by_name['ExtractService'] = _EXTRACTSERVICE

# @@protoc_insertion_point(module_scope)
