import os
from re import findall

from bpy.types import Operator
from bpy.props import StringProperty

from ..functions.get_modules import get_modules
from ..functions.set_scripts_dir import set_scripts_dir

from ..var_globals import template_component


class FLOWMENU_OT_create_component(Operator):
    bl_label = "Create Component"
    bl_idname = "wm.flowmenu_ot_create_component"

    new_module: StringProperty(default="")
    new_class: StringProperty(default="")

    check_to_create: False

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def check(self, context):
        return True

    def draw(self, context):
        dict_modules = get_modules(set_scripts_dir())

        layout = self.layout.column()

        if len(dict_modules) > 0:
            collection_modules = context.window_manager.collection_modules
            collection_modules_active = context.window_manager.collection_modules_active

            current_module = collection_modules[collection_modules_active].value

            layout.box().label(
                text=f"{current_module.capitalize()} is selected", icon="INFO")
            layout.separator()
            layout.separator()
            layout.separator()

        layout.prop(self, "new_module", text="Module")
        layout.prop(self, "new_class", text="Class")

        regex_get_errors = r"^\d.?|\W"
        if findall(regex_get_errors, self.new_module) or findall(regex_get_errors, self.new_class):
            layout.alignment = "RIGHT"
            layout.label(text="Non caracteres not accept")
            self.check_to_create = False
        else:
            self.check_to_create = True

    def execute(self, context):
        game_file_path = set_scripts_dir()
        dict_modules = get_modules(game_file_path)

        if self.check_to_create:

            os.chdir(game_file_path)

            if os.path.exists("scripts"):
                try:
                    if len(dict_modules) > 0:
                        collection_modules = context.window_manager.collection_modules
                        collection_modules_active = context.window_manager.collection_modules_active

                        for root, dirs, files in os.walk(game_file_path):
                            if root.split("\\")[-1] == collection_modules[collection_modules_active].value:
                                os.chdir(root)
                                if self.new_module != "" and not os.path.exists(self.new_module):
                                    if self.new_class != "":
                                        os.mkdir(self.new_module)
                                        with open(os.path.join(f"{root}\\{self.new_module}", f"{self.new_class}.py"), 'w') as fp:
                                            fp.write(template_component %
                                                     self.new_class.capitalize())
                                        fp.close()
                                if self.new_module == "" and self.new_class != "" and not os.path.exists(f"{self.new_class}.py"):
                                    with open(os.path.join(root, f"{self.new_class}.py"), 'w') as fp:
                                        fp.write(template_component %
                                                 self.new_class.capitalize())
                                        fp.close()
                    self.new_module = ""
                    self.new_class = ""
                    return {"FINISHED"}
                except:
                    self.new_module = ""
                    self.new_class = ""
                    return {"FINISHED"}

            else:
                self.new_module = ""
                self.new_class = ""
                os.mkdir("scripts")
                return {"FINISHED"}

        self.new_module = ""
        self.new_class = ""

        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_props_dialog(self)
        return {"RUNNING_MODAL"}
