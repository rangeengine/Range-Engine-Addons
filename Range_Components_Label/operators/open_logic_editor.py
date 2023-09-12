import bpy
from bpy.types import Operator


class FLOWMENU_OT_open_logic_editor(Operator):
    bl_label = "Open Logic Editor"
    bl_idname = "wm.flowmenu_open_logic_editor"

    def execute(self, context):

        if context.area.type == "VIEW_3D":
            context.area.type = "LOGIC_EDITOR"
            bpy.ops.screen.screen_full_area()
            return {"FINISHED"}

        elif context.area.type == "LOGIC_EDITOR":
            context.area.type = "VIEW_3D"
            if context.window.screen.show_fullscreen:
                bpy.ops.screen.screen_full_area()
                return {"FINISHED"}

        return {"FINISHED"}
