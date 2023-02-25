import bpy
from bpy.types import Operator

class FLOWMENU_OT_python_component_reload_new(Operator):
    bl_label = "Python Component Reload New"
    bl_idname = "wm.flowmenu_python_component_reload_new"

    def execute(self, context):
        wm = context.window_manager
        game = context.object.game

        component_active = wm.collection_components_active

        get_component = f"{game.components[component_active].module}.{game.components[component_active].name}"

        bpy.ops.logic.python_component_remove(index=component_active)
        bpy.ops.logic.python_component_register(component_name=get_component)

        return {"FINISHED"}
        
class FLOWMENU_OT_reload_all_components(Operator):
    bl_label = "Reloads the components of all the objects in the Scene."
    bl_idname = "wm.flowmenu_reload_all_components"
    
    def execute(self, context):
        act = bpy.context.scene.objects.active

        for obj in bpy.context.scene.objects:
            flag = obj.select
            
            obj.select = True
            bpy.context.scene.objects.active = obj
            
            for i, comp in enumerate(obj.game.components):
                bpy.ops.logic.python_component_reload(index = i)
                
            obj.select = flag
            
        bpy.context.scene.objects.active = act
        self.report({"INFO"}, "All Scene Components Reloaded!")
        
        return {"FINISHED"}
        
# in .Range Files # obj.name = FileName
class FLOWMENU_OT_refresh_components_list(bpy.types.Operator):
    bl_label = "Refresh the Component List"
    bl_idname = "wm.flowmenu_components_refresh"
    
    def execute(self, context):
        scene = context.scene
        
        dict_modules = {"In .Range File"}
        
        for obj in bpy.data.texts:
            if obj.name[-3:] == ".py":
                strTxt = obj.as_string() # File Container
                if "bge.types.KX_PythonComponent" in strTxt:
                    for line in strTxt.split("\n"):
                        if "bge.types.KX_PythonComponent" in line:
                            nm = line.replace("class", "").replace(" ","").split("(")[0]
                            
                            dict_modules["In .Range File"].update({
                                nm: nm
                            })
                            #item = scene.component_list.add()
                            #item.name = obj.name[-3:]+obj.name[:-3]+"."+nm
                            
        scene.component_list = dict_modules
                
        return {"FINISHED"}
