# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: platform.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='platform.proto',
  package='platform',
  syntax='proto2',
  serialized_pb=b'\n\x0eplatform.proto\x12\x08platform\"T\n\rDocumentation\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12.\n\x0eservice_routes\x18\x02 \x03(\x0b\x32\x16.platform.ServiceRoute\"D\n\x11\x44ocumentationList\x12/\n\x0e\x64ocumentations\x18\x01 \x03(\x0b\x32\x17.platform.Documentation\"\x18\n\x05\x45rror\x12\x0f\n\x07message\x18\x01 \x01(\t\"P\n\x05\x45vent\x12\x14\n\x0corganization\x18\x04 \x01(\t\x12\x0e\n\x06method\x18\x01 \x01(\t\x12\x10\n\x08resource\x18\x02 \x01(\t\x12\x0f\n\x07payload\x18\x03 \x01(\t\"e\n\tIpAddress\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12,\n\x07version\x18\x02 \x01(\x0e\x32\x1b.platform.IpAddress.Version\"\x19\n\x07Version\x12\x06\n\x02V4\x10\x00\x12\x06\n\x02V6\x10\x01\"]\n\x07Request\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\"\n\x07routing\x18\x02 \x01(\x0b\x32\x11.platform.Routing\x12\x0f\n\x07\x63ontext\x18\x03 \x01(\x0c\x12\x0f\n\x07payload\x18\x04 \x01(\x0c\"=\n\x05Route\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\'\n\nip_address\x18\x02 \x01(\x0b\x32\x13.platform.IpAddress\"Q\n\x07Routing\x12!\n\x08route_to\x18\x01 \x03(\x0b\x32\x0f.platform.Route\x12#\n\nroute_from\x18\x02 \x03(\x0b\x32\x0f.platform.Route\"\x9e\x02\n\x0cRouterConfig\x12:\n\rprotocol_type\x18\x01 \x01(\x0e\x32#.platform.RouterConfig.ProtocolType\x12\x0c\n\x04host\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\t\x12\x36\n\x0brouter_type\x18\x04 \x01(\x0e\x32!.platform.RouterConfig.RouterType\"=\n\nRouterType\x12\x19\n\x15ROUTER_TYPE_WEBSOCKET\x10\x01\x12\x14\n\x10ROUTER_TYPE_GRPC\x10\x02\"?\n\x0cProtocolType\x12\x16\n\x12PROTOCOL_TYPE_HTTP\x10\x01\x12\x17\n\x13PROTOCOL_TYPE_HTTPS\x10\x02\"B\n\x10RouterConfigList\x12.\n\x0erouter_configs\x18\x01 \x03(\x0b\x32\x16.platform.RouterConfig\"3\n\rPossibleError\x12\r\n\x05\x65rror\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\"\xc3\x01\n\x0cServiceRoute\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12 \n\x07request\x18\x02 \x01(\x0b\x32\x0f.platform.Route\x12\"\n\tresponses\x18\x03 \x03(\x0b\x32\x0f.platform.Route\x12\x30\n\x0fpossible_errors\x18\x04 \x03(\x0b\x32\x17.platform.PossibleError\x12\x15\n\ris_deprecated\x18\x05 \x01(\x08\x12\x0f\n\x07version\x18\x06 \x01(\t'
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_IPADDRESS_VERSION = _descriptor.EnumDescriptor(
  name='Version',
  full_name='platform.IpAddress.Version',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='V4', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='V6', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=368,
  serialized_end=393,
)
_sym_db.RegisterEnumDescriptor(_IPADDRESS_VERSION)

_ROUTERCONFIG_ROUTERTYPE = _descriptor.EnumDescriptor(
  name='RouterType',
  full_name='platform.RouterConfig.RouterType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ROUTER_TYPE_WEBSOCKET', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ROUTER_TYPE_GRPC', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=797,
  serialized_end=858,
)
_sym_db.RegisterEnumDescriptor(_ROUTERCONFIG_ROUTERTYPE)

_ROUTERCONFIG_PROTOCOLTYPE = _descriptor.EnumDescriptor(
  name='ProtocolType',
  full_name='platform.RouterConfig.ProtocolType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PROTOCOL_TYPE_HTTP', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PROTOCOL_TYPE_HTTPS', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=860,
  serialized_end=923,
)
_sym_db.RegisterEnumDescriptor(_ROUTERCONFIG_PROTOCOLTYPE)


_DOCUMENTATION = _descriptor.Descriptor(
  name='Documentation',
  full_name='platform.Documentation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='description', full_name='platform.Documentation.description', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='service_routes', full_name='platform.Documentation.service_routes', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=112,
)


_DOCUMENTATIONLIST = _descriptor.Descriptor(
  name='DocumentationList',
  full_name='platform.DocumentationList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='documentations', full_name='platform.DocumentationList.documentations', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=114,
  serialized_end=182,
)


_ERROR = _descriptor.Descriptor(
  name='Error',
  full_name='platform.Error',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='platform.Error.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=184,
  serialized_end=208,
)


_EVENT = _descriptor.Descriptor(
  name='Event',
  full_name='platform.Event',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='organization', full_name='platform.Event.organization', index=0,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='method', full_name='platform.Event.method', index=1,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='resource', full_name='platform.Event.resource', index=2,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payload', full_name='platform.Event.payload', index=3,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=210,
  serialized_end=290,
)


_IPADDRESS = _descriptor.Descriptor(
  name='IpAddress',
  full_name='platform.IpAddress',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='address', full_name='platform.IpAddress.address', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='platform.IpAddress.version', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _IPADDRESS_VERSION,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=292,
  serialized_end=393,
)


_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='platform.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uuid', full_name='platform.Request.uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='routing', full_name='platform.Request.routing', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='context', full_name='platform.Request.context', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payload', full_name='platform.Request.payload', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=395,
  serialized_end=488,
)


_ROUTE = _descriptor.Descriptor(
  name='Route',
  full_name='platform.Route',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uri', full_name='platform.Route.uri', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ip_address', full_name='platform.Route.ip_address', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=490,
  serialized_end=551,
)


_ROUTING = _descriptor.Descriptor(
  name='Routing',
  full_name='platform.Routing',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='route_to', full_name='platform.Routing.route_to', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='route_from', full_name='platform.Routing.route_from', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=553,
  serialized_end=634,
)


_ROUTERCONFIG = _descriptor.Descriptor(
  name='RouterConfig',
  full_name='platform.RouterConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='protocol_type', full_name='platform.RouterConfig.protocol_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='host', full_name='platform.RouterConfig.host', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='port', full_name='platform.RouterConfig.port', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='router_type', full_name='platform.RouterConfig.router_type', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ROUTERCONFIG_ROUTERTYPE,
    _ROUTERCONFIG_PROTOCOLTYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=637,
  serialized_end=923,
)


_ROUTERCONFIGLIST = _descriptor.Descriptor(
  name='RouterConfigList',
  full_name='platform.RouterConfigList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='router_configs', full_name='platform.RouterConfigList.router_configs', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=925,
  serialized_end=991,
)


_POSSIBLEERROR = _descriptor.Descriptor(
  name='PossibleError',
  full_name='platform.PossibleError',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='platform.PossibleError.error', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='platform.PossibleError.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=993,
  serialized_end=1044,
)


_SERVICEROUTE = _descriptor.Descriptor(
  name='ServiceRoute',
  full_name='platform.ServiceRoute',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='description', full_name='platform.ServiceRoute.description', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='request', full_name='platform.ServiceRoute.request', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='responses', full_name='platform.ServiceRoute.responses', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='possible_errors', full_name='platform.ServiceRoute.possible_errors', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_deprecated', full_name='platform.ServiceRoute.is_deprecated', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='platform.ServiceRoute.version', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1047,
  serialized_end=1242,
)

_DOCUMENTATION.fields_by_name['service_routes'].message_type = _SERVICEROUTE
_DOCUMENTATIONLIST.fields_by_name['documentations'].message_type = _DOCUMENTATION
_IPADDRESS.fields_by_name['version'].enum_type = _IPADDRESS_VERSION
_IPADDRESS_VERSION.containing_type = _IPADDRESS
_REQUEST.fields_by_name['routing'].message_type = _ROUTING
_ROUTE.fields_by_name['ip_address'].message_type = _IPADDRESS
_ROUTING.fields_by_name['route_to'].message_type = _ROUTE
_ROUTING.fields_by_name['route_from'].message_type = _ROUTE
_ROUTERCONFIG.fields_by_name['protocol_type'].enum_type = _ROUTERCONFIG_PROTOCOLTYPE
_ROUTERCONFIG.fields_by_name['router_type'].enum_type = _ROUTERCONFIG_ROUTERTYPE
_ROUTERCONFIG_ROUTERTYPE.containing_type = _ROUTERCONFIG
_ROUTERCONFIG_PROTOCOLTYPE.containing_type = _ROUTERCONFIG
_ROUTERCONFIGLIST.fields_by_name['router_configs'].message_type = _ROUTERCONFIG
_SERVICEROUTE.fields_by_name['request'].message_type = _ROUTE
_SERVICEROUTE.fields_by_name['responses'].message_type = _ROUTE
_SERVICEROUTE.fields_by_name['possible_errors'].message_type = _POSSIBLEERROR
DESCRIPTOR.message_types_by_name['Documentation'] = _DOCUMENTATION
DESCRIPTOR.message_types_by_name['DocumentationList'] = _DOCUMENTATIONLIST
DESCRIPTOR.message_types_by_name['Error'] = _ERROR
DESCRIPTOR.message_types_by_name['Event'] = _EVENT
DESCRIPTOR.message_types_by_name['IpAddress'] = _IPADDRESS
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Route'] = _ROUTE
DESCRIPTOR.message_types_by_name['Routing'] = _ROUTING
DESCRIPTOR.message_types_by_name['RouterConfig'] = _ROUTERCONFIG
DESCRIPTOR.message_types_by_name['RouterConfigList'] = _ROUTERCONFIGLIST
DESCRIPTOR.message_types_by_name['PossibleError'] = _POSSIBLEERROR
DESCRIPTOR.message_types_by_name['ServiceRoute'] = _SERVICEROUTE

Documentation = _reflection.GeneratedProtocolMessageType('Documentation', (_message.Message,), dict(
  DESCRIPTOR = _DOCUMENTATION,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:platform.Documentation)
  ))
_sym_db.RegisterMessage(Documentation)

DocumentationList = _reflection.GeneratedProtocolMessageType('DocumentationList', (_message.Message,), dict(
  DESCRIPTOR = _DOCUMENTATIONLIST,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:platform.DocumentationList)
  ))
_sym_db.RegisterMessage(DocumentationList)

Error = _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), dict(
  DESCRIPTOR = _ERROR,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:platform.Error)
  ))
_sym_db.RegisterMessage(Error)

Event = _reflection.GeneratedProtocolMessageType('Event', (_message.Message,), dict(
  DESCRIPTOR = _EVENT,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:platform.Event)
  ))
_sym_db.RegisterMessage(Event)

IpAddress = _reflection.GeneratedProtocolMessageType('IpAddress', (_message.Message,), dict(
  DESCRIPTOR = _IPADDRESS,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:platform.IpAddress)
  ))
_sym_db.RegisterMessage(IpAddress)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:platform.Request)
  ))
_sym_db.RegisterMessage(Request)

Route = _reflection.GeneratedProtocolMessageType('Route', (_message.Message,), dict(
  DESCRIPTOR = _ROUTE,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:platform.Route)
  ))
_sym_db.RegisterMessage(Route)

Routing = _reflection.GeneratedProtocolMessageType('Routing', (_message.Message,), dict(
  DESCRIPTOR = _ROUTING,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:platform.Routing)
  ))
_sym_db.RegisterMessage(Routing)

RouterConfig = _reflection.GeneratedProtocolMessageType('RouterConfig', (_message.Message,), dict(
  DESCRIPTOR = _ROUTERCONFIG,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:platform.RouterConfig)
  ))
_sym_db.RegisterMessage(RouterConfig)

RouterConfigList = _reflection.GeneratedProtocolMessageType('RouterConfigList', (_message.Message,), dict(
  DESCRIPTOR = _ROUTERCONFIGLIST,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:platform.RouterConfigList)
  ))
_sym_db.RegisterMessage(RouterConfigList)

PossibleError = _reflection.GeneratedProtocolMessageType('PossibleError', (_message.Message,), dict(
  DESCRIPTOR = _POSSIBLEERROR,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:platform.PossibleError)
  ))
_sym_db.RegisterMessage(PossibleError)

ServiceRoute = _reflection.GeneratedProtocolMessageType('ServiceRoute', (_message.Message,), dict(
  DESCRIPTOR = _SERVICEROUTE,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:platform.ServiceRoute)
  ))
_sym_db.RegisterMessage(ServiceRoute)


# @@protoc_insertion_point(module_scope)
