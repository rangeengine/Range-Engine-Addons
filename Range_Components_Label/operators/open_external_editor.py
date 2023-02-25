import bpy
import os

from bpy.types import Operator
from bpy.props import EnumProperty


class FLOWMENU_OT_open_external_editor(Operator):
    bl_label = "Open External Editor"
    bl_idname = "wm.flowmenu_open_external_editor"

    editors_enum:  EnumProperty(items=[
        ("code", "VSCode", ""),
        ("subl", "Sublime", ""),
    ])

    def draw(self, context):
        layout = self.layout
        layout.props_enum(self, "editors_enum")

    def execute(self, context):
        root_file = bpy.data.filepath.rpartition("\\")[0]
        editor = self.editors_enum

        os.chdir(root_file)
        try:
            os.system(f"{editor} --add .")
            return {"FINISHED"}
        except:
            return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_props_dialog(self)
        return {"RUNNING_MODAL"}
