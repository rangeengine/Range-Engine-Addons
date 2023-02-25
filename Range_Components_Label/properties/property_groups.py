import bpy
from bpy.types import PropertyGroup


class FLOWMENU_PG_header_enum(PropertyGroup):
    header_items: bpy.props.EnumProperty(
        name="Header Items",
        description="Enum to header menu items",
        items=[
            ("GAME", "Game Component", "Game Component Header"),
            ("OBJECT", "Object", "Object Header"),
            ("LOGIC", "Logic", "Logic Header"),
        ]
    )


class FLOWMENU_PG_expand_only_active(PropertyGroup):
    active: bpy.props.BoolProperty(name="Expand Only Active", default=False)


class FLOWMENU_PG_collection_item(PropertyGroup):
    value: bpy.props.StringProperty(name="Value", default="Item Collection")
