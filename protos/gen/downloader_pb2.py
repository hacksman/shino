# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: downloader.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='downloader.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x10\x64ownloader.proto\"\xcc\x03\n\x0b\x44ownloadReq\x12\x10\n\x08\x62\x61tch_no\x18\x01 \x01(\t\x12\x0b\n\x03\x61pi\x18\x02 \x01(\t\x12\x0b\n\x03url\x18\x03 \x01(\t\x12\x10\n\x06method\x18\x04 \x01(\tH\x00\x12\x17\n\rdownload_type\x18\x05 \x01(\tH\x01\x12\x15\n\x0bretry_times\x18\x06 \x01(\x05H\x02\x12\x12\n\x08time_out\x18\x07 \x01(\x05H\x03\x12\x31\n\x0bhttp_header\x18\x08 \x03(\x0b\x32\x1c.DownloadReq.HttpHeaderEntry\x12-\n\tpost_data\x18\t \x03(\x0b\x32\x1a.DownloadReq.PostDataEntry\x12\x13\n\tuse_proxy\x18\n \x01(\x05H\x04\x1a\x31\n\x0fHttpHeaderEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a/\n\rPostDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x0f\n\rone_of_methodB\x16\n\x14one_of_download_typeB\x14\n\x12one_of_retry_timesB\x11\n\x0fone_of_time_outB\x0e\n\x0cone_of_proxy\"\xd9\x01\n\x0b\x44ownloadRsp\x12\x10\n\x08\x62\x61tch_no\x18\x01 \x01(\t\x12\x0b\n\x03\x61pi\x18\x02 \x01(\t\x12\x0b\n\x03url\x18\x03 \x01(\t\x12\x1c\n\x06status\x18\x04 \x01(\x0e\x32\x0c.CrawlStatus\x12\x11\n\thttp_code\x18\x05 \x01(\x05\x12\x15\n\rdownload_time\x18\x06 \x01(\t\x12\x0f\n\x07\x65lapsed\x18\x07 \x01(\x02\x12\x14\n\x0c\x63ontent_type\x18\x08 \x01(\t\x12\x0f\n\x07\x63ontent\x18\t \x01(\t\x12\x1e\n\x08req_info\x18\n \x01(\x0b\x32\x0c.DownloadReq*0\n\x0b\x43rawlStatus\x12\x11\n\rCRAWL_SUCCESS\x10\x00\x12\x0e\n\nCRAWL_FAIL\x10\x01\x32\x39\n\x0f\x44ownloadService\x12&\n\x08\x64ownload\x12\x0c.DownloadReq\x1a\x0c.DownloadRspb\x06proto3'
)

_CRAWLSTATUS = _descriptor.EnumDescriptor(
  name='CrawlStatus',
  full_name='CrawlStatus',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CRAWL_SUCCESS', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CRAWL_FAIL', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=703,
  serialized_end=751,
)
_sym_db.RegisterEnumDescriptor(_CRAWLSTATUS)

CrawlStatus = enum_type_wrapper.EnumTypeWrapper(_CRAWLSTATUS)
CRAWL_SUCCESS = 0
CRAWL_FAIL = 1



_DOWNLOADREQ_HTTPHEADERENTRY = _descriptor.Descriptor(
  name='HttpHeaderEntry',
  full_name='DownloadReq.HttpHeaderEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='DownloadReq.HttpHeaderEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='DownloadReq.HttpHeaderEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=285,
  serialized_end=334,
)

_DOWNLOADREQ_POSTDATAENTRY = _descriptor.Descriptor(
  name='PostDataEntry',
  full_name='DownloadReq.PostDataEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='DownloadReq.PostDataEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='DownloadReq.PostDataEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=336,
  serialized_end=383,
)

_DOWNLOADREQ = _descriptor.Descriptor(
  name='DownloadReq',
  full_name='DownloadReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='batch_no', full_name='DownloadReq.batch_no', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='api', full_name='DownloadReq.api', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='DownloadReq.url', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='method', full_name='DownloadReq.method', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='download_type', full_name='DownloadReq.download_type', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='retry_times', full_name='DownloadReq.retry_times', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='time_out', full_name='DownloadReq.time_out', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='http_header', full_name='DownloadReq.http_header', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='post_data', full_name='DownloadReq.post_data', index=8,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='use_proxy', full_name='DownloadReq.use_proxy', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_DOWNLOADREQ_HTTPHEADERENTRY, _DOWNLOADREQ_POSTDATAENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='one_of_method', full_name='DownloadReq.one_of_method',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='one_of_download_type', full_name='DownloadReq.one_of_download_type',
      index=1, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='one_of_retry_times', full_name='DownloadReq.one_of_retry_times',
      index=2, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='one_of_time_out', full_name='DownloadReq.one_of_time_out',
      index=3, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='one_of_proxy', full_name='DownloadReq.one_of_proxy',
      index=4, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=21,
  serialized_end=481,
)


_DOWNLOADRSP = _descriptor.Descriptor(
  name='DownloadRsp',
  full_name='DownloadRsp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='batch_no', full_name='DownloadRsp.batch_no', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='api', full_name='DownloadRsp.api', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='DownloadRsp.url', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='DownloadRsp.status', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='http_code', full_name='DownloadRsp.http_code', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='download_time', full_name='DownloadRsp.download_time', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='elapsed', full_name='DownloadRsp.elapsed', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='content_type', full_name='DownloadRsp.content_type', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='content', full_name='DownloadRsp.content', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='req_info', full_name='DownloadRsp.req_info', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=484,
  serialized_end=701,
)

_DOWNLOADREQ_HTTPHEADERENTRY.containing_type = _DOWNLOADREQ
_DOWNLOADREQ_POSTDATAENTRY.containing_type = _DOWNLOADREQ
_DOWNLOADREQ.fields_by_name['http_header'].message_type = _DOWNLOADREQ_HTTPHEADERENTRY
_DOWNLOADREQ.fields_by_name['post_data'].message_type = _DOWNLOADREQ_POSTDATAENTRY
_DOWNLOADREQ.oneofs_by_name['one_of_method'].fields.append(
  _DOWNLOADREQ.fields_by_name['method'])
_DOWNLOADREQ.fields_by_name['method'].containing_oneof = _DOWNLOADREQ.oneofs_by_name['one_of_method']
_DOWNLOADREQ.oneofs_by_name['one_of_download_type'].fields.append(
  _DOWNLOADREQ.fields_by_name['download_type'])
_DOWNLOADREQ.fields_by_name['download_type'].containing_oneof = _DOWNLOADREQ.oneofs_by_name['one_of_download_type']
_DOWNLOADREQ.oneofs_by_name['one_of_retry_times'].fields.append(
  _DOWNLOADREQ.fields_by_name['retry_times'])
_DOWNLOADREQ.fields_by_name['retry_times'].containing_oneof = _DOWNLOADREQ.oneofs_by_name['one_of_retry_times']
_DOWNLOADREQ.oneofs_by_name['one_of_time_out'].fields.append(
  _DOWNLOADREQ.fields_by_name['time_out'])
_DOWNLOADREQ.fields_by_name['time_out'].containing_oneof = _DOWNLOADREQ.oneofs_by_name['one_of_time_out']
_DOWNLOADREQ.oneofs_by_name['one_of_proxy'].fields.append(
  _DOWNLOADREQ.fields_by_name['use_proxy'])
_DOWNLOADREQ.fields_by_name['use_proxy'].containing_oneof = _DOWNLOADREQ.oneofs_by_name['one_of_proxy']
_DOWNLOADRSP.fields_by_name['status'].enum_type = _CRAWLSTATUS
_DOWNLOADRSP.fields_by_name['req_info'].message_type = _DOWNLOADREQ
DESCRIPTOR.message_types_by_name['DownloadReq'] = _DOWNLOADREQ
DESCRIPTOR.message_types_by_name['DownloadRsp'] = _DOWNLOADRSP
DESCRIPTOR.enum_types_by_name['CrawlStatus'] = _CRAWLSTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DownloadReq = _reflection.GeneratedProtocolMessageType('DownloadReq', (_message.Message,), {

  'HttpHeaderEntry' : _reflection.GeneratedProtocolMessageType('HttpHeaderEntry', (_message.Message,), {
    'DESCRIPTOR' : _DOWNLOADREQ_HTTPHEADERENTRY,
    '__module__' : 'downloader_pb2'
    # @@protoc_insertion_point(class_scope:DownloadReq.HttpHeaderEntry)
    })
  ,

  'PostDataEntry' : _reflection.GeneratedProtocolMessageType('PostDataEntry', (_message.Message,), {
    'DESCRIPTOR' : _DOWNLOADREQ_POSTDATAENTRY,
    '__module__' : 'downloader_pb2'
    # @@protoc_insertion_point(class_scope:DownloadReq.PostDataEntry)
    })
  ,
  'DESCRIPTOR' : _DOWNLOADREQ,
  '__module__' : 'downloader_pb2'
  # @@protoc_insertion_point(class_scope:DownloadReq)
  })
_sym_db.RegisterMessage(DownloadReq)
_sym_db.RegisterMessage(DownloadReq.HttpHeaderEntry)
_sym_db.RegisterMessage(DownloadReq.PostDataEntry)

DownloadRsp = _reflection.GeneratedProtocolMessageType('DownloadRsp', (_message.Message,), {
  'DESCRIPTOR' : _DOWNLOADRSP,
  '__module__' : 'downloader_pb2'
  # @@protoc_insertion_point(class_scope:DownloadRsp)
  })
_sym_db.RegisterMessage(DownloadRsp)


_DOWNLOADREQ_HTTPHEADERENTRY._options = None
_DOWNLOADREQ_POSTDATAENTRY._options = None

_DOWNLOADSERVICE = _descriptor.ServiceDescriptor(
  name='DownloadService',
  full_name='DownloadService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=753,
  serialized_end=810,
  methods=[
  _descriptor.MethodDescriptor(
    name='download',
    full_name='DownloadService.download',
    index=0,
    containing_service=None,
    input_type=_DOWNLOADREQ,
    output_type=_DOWNLOADRSP,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_DOWNLOADSERVICE)

DESCRIPTOR.services_by_name['DownloadService'] = _DOWNLOADSERVICE

# @@protoc_insertion_point(module_scope)
