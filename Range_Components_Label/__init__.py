import bpy

from .properties.property_groups import FLOWMENU_PG_header_enum, FLOWMENU_PG_expand_only_active, FLOWMENU_PG_collection_item
from .properties.property_register import FLOWMENU_Properties_Register
from .ui_lists.modules_components import FLOWMENU_UL_modules_components
from .ui_lists.classes_components import FLOWMENU_UL_classes_components
from .ui_lists.game_components import FLOWMENU_UL_game_components
from .ui_lists.sensors import FLOWMENU_UL_sensors

from .operators.create_component import FLOWMENU_OT_create_component
from .operators.register_component import FLOWMENU_OT_register_component
from .operators.component_reload_new import FLOWMENU_OT_python_component_reload_new
from .operators.component_reload_new import FLOWMENU_OT_reload_all_components
from .operators.open_logic_editor import FLOWMENU_OT_open_logic_editor
from .operators.open_external_editor import FLOWMENU_OT_open_external_editor
from .operators.init_addon import FLOWMENU_OT_init_addon

bl_info = {
    "name": "RanGE Components Label",
    "author": "x~p (Misael Sousa), Range Engine",
    "description": "Easy flow menu to using a Python Component.",
    "blender": (2, 79, 7),
    "version": (1, 2, 0),
    "location": "Properties > Game",
    "wiki_url": "https://github.com/misael-s/flow-menu-components",
    "warning": "Only for Range Engine 1.4+",
    "tracker_url": "",
    "category": "Game Engine"
}

classes = [
    FLOWMENU_PG_header_enum,
    FLOWMENU_PG_expand_only_active,
    FLOWMENU_PG_collection_item,
    FLOWMENU_UL_modules_components,
    FLOWMENU_UL_classes_components,
    FLOWMENU_UL_game_components,
    FLOWMENU_UL_sensors,
    FLOWMENU_OT_create_component,
    FLOWMENU_OT_register_component,
    FLOWMENU_OT_python_component_reload_new,
    FLOWMENU_OT_reload_all_components,
    FLOWMENU_OT_open_logic_editor,
    FLOWMENU_OT_open_external_editor,
    FLOWMENU_OT_init_addon,
]

properties = [
    FLOWMENU_Properties_Register,
]

addon_keymaps = []


def register():

    # Classes
    for cls in classes:
        bpy.utils.register_class(cls)

    # Properties
    for prt in properties:
        prt.pointer()
    # Other
    '''wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            FLOWMENU_OT_init_addon.bl_idname, type="Q", value="PRESS", alt=True)
        addon_keymaps.append((km, kmi))

        km = kc.keymaps.new(name="Logic Editor", space_type="LOGIC_EDITOR")
        kmi = km.keymap_items.new(
            FLOWMENU_OT_init_addon.bl_idname, type="Q", value="PRESS", alt=True)
        addon_keymaps.append((km, kmi))'''


def unregister():

    # Classes
    for cls in classes:
        bpy.utils.unregister_class(cls)

    # Properties
    for prt in properties:
        prt.delete()

    # Other
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


#if __name__ == "__main__":
#    register()
