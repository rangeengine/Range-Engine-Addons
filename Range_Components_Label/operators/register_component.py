import bpy
from bpy.types import Operator

from ..functions.get_modules import get_modules, get_modules_in_range
from ..functions.set_scripts_dir import set_scripts_dir


class FLOWMENU_OT_register_component(Operator):
    bl_label = "Register Component"
    bl_idname = "wm.flowmenu_ot_register_component"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        scene = context.scene
    
        dict_modules = get_modules_in_range(scene)
        dict_modules.update(get_modules(set_scripts_dir()))

        obj = context.object
        game = obj.game
        wm = context.window_manager

        get_properties = wm

        collection_modules = get_properties.collection_modules
        collection_modules_active = get_properties.collection_modules_active

        collection_classes = get_properties.collection_classes
        collection_classes_active = get_properties.collection_classes_active

        module_select = collection_modules[collection_modules_active].value
        class_select = collection_classes[collection_classes_active].value
        
        #if (module_select != "In .Range File"):
        print(dict_modules[module_select][class_select])
        register_component = dict_modules[module_select][class_select]
        #else: register_component = dict_modules["In .Range File"][class_select]

        list_name_components = []
        for component in game.components:
            list_name_components.append(f"{component.module}.{component.name}")

        if register_component not in list_name_components:
            bpy.ops.logic.python_component_register(
                component_name=register_component)
            self.report({"INFO"}, "Component '"+ str(register_component).split(".")[1] +"' added!")
            return {"FINISHED"}
        
        self.report({"INFO"}, "Component '"+ str(register_component).split(".")[1] +"' is already added.")
        return {"FINISHED"}
