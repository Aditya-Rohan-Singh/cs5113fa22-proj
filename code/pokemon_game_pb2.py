# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pokemon_game.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12pokemon_game.proto\x12\x0cpokemon_game\"8\n\x07movepos\x12\x0b\n\x03row\x18\x01 \x01(\x05\x12\x0e\n\x06\x63olumn\x18\x02 \x01(\x05\x12\x10\n\x08hostname\x18\x03 \x01(\t\"%\n\x0cmovecomplete\x12\x15\n\rmovecompleted\x18\x01 \x01(\x05\"\x18\n\x04name\x12\x10\n\x08hostname\x18\x01 \x01(\t\"\x1e\n\x08\x63heckpos\x12\x12\n\ncheckboard\x18\x01 \x03(\x05\"\x1f\n\x0ctrainer_name\x12\x0f\n\x07trainer\x18\x01 \x01(\t\"(\n\x10pokemon_captured\x12\x14\n\x0cpokemon_name\x18\x01 \x03(\t\"\x1d\n\x04path\x12\x15\n\rpath_followed\x18\x01 \x03(\x05\x32\xcb\x02\n\x0bPokemonGame\x12:\n\ncheckboard\x12\x12.pokemon_game.name\x1a\x16.pokemon_game.checkpos\"\x00\x12;\n\x04Move\x12\x15.pokemon_game.movepos\x1a\x1a.pokemon_game.movecomplete\"\x00\x12\x44\n\x0cpokemon_list\x12\x12.pokemon_game.name\x1a\x1e.pokemon_game.pokemon_captured\"\x00\x12\x37\n\x0b\x63lient_path\x12\x12.pokemon_game.name\x1a\x12.pokemon_game.path\"\x00\x12\x44\n\x0ctrainer_list\x12\x12.pokemon_game.name\x1a\x1e.pokemon_game.pokemon_captured\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'pokemon_game_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MOVEPOS._serialized_start=36
  _MOVEPOS._serialized_end=92
  _MOVECOMPLETE._serialized_start=94
  _MOVECOMPLETE._serialized_end=131
  _NAME._serialized_start=133
  _NAME._serialized_end=157
  _CHECKPOS._serialized_start=159
  _CHECKPOS._serialized_end=189
  _TRAINER_NAME._serialized_start=191
  _TRAINER_NAME._serialized_end=222
  _POKEMON_CAPTURED._serialized_start=224
  _POKEMON_CAPTURED._serialized_end=264
  _PATH._serialized_start=266
  _PATH._serialized_end=295
  _POKEMONGAME._serialized_start=298
  _POKEMONGAME._serialized_end=629
# @@protoc_insertion_point(module_scope)
