from bpy import ops
from bpy.types import Operator
from bpy.app import version

from ..drawings.draw_game_properties import draw_game_properties
from ..drawings.draw_game_component import draw_game_component

from ..functions.get_modules import get_modules, get_modules_in_range
from ..functions.set_scripts_dir import set_scripts_dir
from ..functions.is_somethings import is_file_saved, is_bge_version

class FLOWMENU_OT_init_addon(Operator):
    bl_label = "Components Menu"
    bl_idname = "wm.flowmenu_ot_init"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def draw(self, context):
        layout = self.layout

        wm = context.window_manager
        scene = context.scene
        obj = context.object
        game = obj.game

        header_items = wm.header_enum.header_items
        game_components = game.components

        get_properties = wm

        expand_only = get_properties.expand_only

        collection_modules = get_properties.collection_modules
        collection_modules_active = get_properties.collection_modules_active

        collection_classes = get_properties.collection_classes
        collection_classes_active = get_properties.collection_classes_active

        collection_components = get_properties.collection_components
        collection_components_active = get_properties.collection_components_active

        #collection_sensors = get_properties.collection_sensors
        #collection_sensors_active = get_properties.collection_sensors_active

        # DRAW LAYOUT ========================================

        row_title_addon = layout.box().row(align=True)
        row_title_addon.label(text="Components Menu")
        row_title_addon.operator("wm.flowmenu_reload_all_components",
                          text="Reload all scene components", icon="RECOVER_LAST")
        
        #row_info = layout.row(align=True)
        row_title_addon.label(
            text=f"{obj.name.capitalize()} is selected", icon="OBJECT_DATA")

        row_header = layout.row(align=True)
        if not is_file_saved():
            row_header.box().label(text="Save the file first to use!", icon="INFO")
            return

        #row_header.row(align=True).prop(data=wm.header_enum,
        #                                property="header_items", expand=True)

        #if header_items == "GAME":
        dict_modules = get_modules_in_range(scene)
        dict_modules.update(get_modules(set_scripts_dir()))
        

        game_row = layout.row()
        game_row.alignment = "LEFT"
        game_row.operator("wm.flowmenu_ot_create_component",
                          text="Create Component", icon="PLUS")
        game_row.operator("wm.flowmenu_open_external_editor",
                          text="Open External Editor", icon="CONSOLE")

        game_row = layout.row(align=True)

        if len(dict_modules) == 0:
            empity_msg = game_row.column()
            empity_msg.alert = True
            empity_msg.box().label(
                text="Class KX_PythonComponent not found in the game file dir! Create a root dir for game file, and create dir scripts in root.", icon="INFO")
            return

        col_modules = game_row.column(align=True)
        #col_modules.scale_x = 0.5
        col_modules.box().label(text="Modules", icon=[
            "OUTLINER", "OOPS"][version == (2, 79, 7)])

        collection_modules.clear()
        for module in dict_modules:
            item = collection_modules.add()
            item.value = module

        col_modules.template_list("FLOWMENU_UL_modules_components", "flowmenu_ul_modules_components", get_properties,
                                  "collection_modules", get_properties, "collection_modules_active", rows=10)

        col_classes = game_row.column(align=True)
        #col_classes.scale_x = 0.5
        col_classes.box().label(text="Classes", icon="FILE_BLEND")

        current_module = collection_modules[collection_modules_active].value

        for module in dict_modules:
            if current_module == module:
                item = collection_classes.clear()
                for cls in dict_modules[current_module]:
                    item = collection_classes.add()
                    item.value = cls
                col_classes.template_list("FLOWMENU_UL_classes_components", "flowmenu_ul_classes_components", get_properties,
                                          "collection_classes", get_properties, "collection_classes_active", rows=10)

        #col_components = game_row.column(align=True)
        #col_components.scale_x = 1.6
        #col_components.box().label(
        #    text=f"Object Components in {obj.name}", icon="LOGIC")

        '''if len(game_components) > 0:
            collection_components.clear()
            for component in game_components:
                item = collection_components.add()
                item.value = component.name
            col_components.template_list("FLOWMENU_UL_game_components", "flowmenu_ul_game_components", get_properties,
                                         "collection_components", get_properties, "collection_components_active", rows=10)

            col_component_select = game_row.column(align=True)
            col_component_select.scale_x = 2
            col_component_select.box().label(text="Select", icon="PINNED")

            draw_game_component(self, context, col_component_select)
        else:
            collection_components.clear()
            col_components.box().label(text="No components registered!", icon="INFO")'''

    def execute(self, context):
        ops.FLOWMENU_OT_refresh_components_list()
        return {"FINISHED"}

    def check(self, context):
        return True

    def invoke(self, context, event):
        if context.space_data.type == "VIEW_3D" or "LOGIC_EDITOR":
            width = context.window.width
            height = context.window.height

            wm = context.window_manager
            context.window.cursor_warp(int(width/2.7), int(height/1.2))

            wm.invoke_popup(self, width=int(width/2.5))
            
            context.window.cursor_warp(int(width/1.7), int(height/1.7))

            return {"RUNNING_MODAL"}
        else:
            return {"CANCELLED"}
