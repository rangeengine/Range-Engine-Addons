from bpy.types import WindowManager
from bpy.props import PointerProperty, CollectionProperty, IntProperty

from .property_groups import FLOWMENU_PG_header_enum, FLOWMENU_PG_expand_only_active, FLOWMENU_PG_collection_item


class FLOWMENU_Properties_Register():
    def pointer():
        WindowManager.header_enum = PointerProperty(
            name="Header Enum", type=FLOWMENU_PG_header_enum)

        WindowManager.expand_only = PointerProperty(
            name="Expand Only Active", type=FLOWMENU_PG_expand_only_active)

        WindowManager.collection_modules = CollectionProperty(
            type=FLOWMENU_PG_collection_item)
        WindowManager.collection_modules_active = IntProperty(
            name="Module Selected", default=0)

        WindowManager.collection_classes = CollectionProperty(
            type=FLOWMENU_PG_collection_item)
        WindowManager.collection_classes_active = IntProperty(
            name="Class Selected", default=0)

        WindowManager.collection_components = CollectionProperty(
            type=FLOWMENU_PG_collection_item)
        WindowManager.collection_components_active = IntProperty(
            name="Component Selected", default=0)

        WindowManager.collection_sensors = CollectionProperty(
            type=FLOWMENU_PG_collection_item)
        WindowManager.collection_sensors_active = IntProperty(
            name="Component Selected", default=0)

    def delete():
        del WindowManager.header_enum
        del WindowManager.expand_only

        del WindowManager.collection_modules
        del WindowManager.collection_modules_active

        del WindowManager.collection_classes
        del WindowManager.collection_classes_active

        del WindowManager.collection_components
        del WindowManager.collection_components_active

        del WindowManager.collection_sensors
        del WindowManager.collection_sensors_active
