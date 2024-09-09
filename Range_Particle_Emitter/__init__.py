bl_info = {
    "name": "RanGE: Particle Emitter",
    "author": "Andreas Esau, Range Engine",
    "version": (1, 0),
    "blender": (2, 7, 9),
    "api": 42494,
    "location": "Properties > Particles",
    "description": "An Easy to use Particle System for Range Engine",
    "warning": "Only for Range Engine 1.5+",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Game Engine"}

###
	
import bpy
import math
import mathutils
import os
from bpy.app.handlers import persistent
import pickle
from bpy_extras.io_utils import ExportHelper
from bpy.props import (StringProperty, 
                       IntProperty, 
                       FloatProperty, 
                       BoolProperty, 
                       EnumProperty, 
                       FloatVectorProperty)

class EasyEmitPresets(bpy.types.Panel):
    bl_label = "Particle Emitter Presets"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "particle"
    COMPAT_ENGINES = {"BLENDER_GAME"}

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        rd = context.scene.render
        return ob and ob.game and (rd.engine in cls.COMPAT_ENGINES)
    
    def draw(self, context):
        col = self.layout.column()
        row = self.layout.row()
        split = self.layout.split()
        scene = bpy.context.scene
        ob = context.object
        sce = context.scene
        
        row.label("Presets", icon="FILESEL")
        row = self.layout.row()
        
        row.template_list("UI_UL_list", "dummy", scene, "preset_list", scene, "preset_list_index", rows=2)
        
        col = row.column(align=True)
        col.operator("scene.add_preset", icon="ZOOMIN", text="")
        col.operator("scene.remove_preset", icon="ZOOMOUT", text="")  
        try:
            preset = sce.preset_list[sce.preset_list_index]
            
            row = self.layout.row()
            row.prop(preset, "name", text="Preset Name")
        except:
            ...
        row = self.layout.row()
        row.operator("scene.init_preset", text="Load Factory Presets", icon="FREEZE")
        row = self.layout.row()
        row = self.layout.row()
        row.operator("export.load_preset",text="Import Particle Presets", icon="IMPORT") 
        row = self.layout.row()    
        row.operator("export.save_preset",text="Export Particle Presets", icon="EXPORT")      
        

class EasyEmit(bpy.types.Panel):
    bl_label = "Particle Emitter"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "particle"
    COMPAT_ENGINES = {"BLENDER_GAME"}
    
    def update_values(self, context):
        bpy.ops.object.apply_values()
    
    bpy.types.Object.particlesystem = BoolProperty(default=False)
    bpy.types.Object.particle = BoolProperty(default=False)
    bpy.types.Object.frustumCulling = BoolProperty(description="Allows you to disable the Emitter automatically if not seen!",default=True, update=update_values)
    bpy.types.Object.frustumRadius = IntProperty(description="Radius for Frustum Culling", default=4, min=1, update=update_values)
    
    bpy.types.Object.localEmit = BoolProperty(default=True, description="Particle is emitted global or local", update=update_values)
    
    bpy.types.Object.emitTime = IntProperty(name="", description="Emission Time. 0 -> Emits always!", default=0, min=0, update=update_values)
    bpy.types.Object.amount = IntProperty(name="", description="Amount of Particles that are emitted in 60 Tics(1 Second)", default=10, min=1, max=180, update=update_values)
    bpy.types.Object.lifetime = IntProperty(name="", description="Particle Lifetime", default=60, min=1, update=update_values)
    bpy.types.Object.randomlifetimevalue = IntProperty(name="", description="Particle Random Lifetime", default=0, min=0, update=update_values)
    bpy.types.Object.emitteron = BoolProperty(name="", description="Turn emitter on or off", default=True, update=update_values)
    bpy.types.Object.emitterinvisible = BoolProperty(name="", description="Sets the Emitter visible or invisble in the Game", default=True, update=update_values)
    bpy.types.Object.with_cache = BoolProperty(name="", description="Enables caching for the emitter, this can save some performance but makes the emitter less accurate at high framerates", default=False, update=update_values)
    
    bpy.types.Object.cone = FloatVectorProperty(name="", description="Sperical Emission Range", default=(0.261800, 0.261800, 0.261800),precision=1, min=0, max=2*math.pi, subtype="EULER", update=update_values)
    bpy.types.Object.startscale = FloatProperty(name="", description="Particlescale on birth", default=1.0, min=0, update=update_values)
    bpy.types.Object.endscale = FloatProperty(name="", description="Particlescale on death", default=1.0, min=0, update=update_values)
    bpy.types.Object.scalefade_start = IntProperty(name="", description="Adjust the scale fading for Particle Lifetime", default=0, min=1, update=update_values)
    bpy.types.Object.scalefade_end = IntProperty(name="", description="Adjust the scale fading for Particle Lifetime", default=60, min=1, update=update_values)
    bpy.types.Object.speedfade_start = IntProperty(name="", description="Adjust the speed fading for Particle Lifetime", default=0, min=1, update=update_values)
    bpy.types.Object.speedfade_end = IntProperty(name="", description="Adjust the speed fading for Particle Lifetime", default=60, min=1, update=update_values)

    bpy.types.Object.rangeEmit = FloatVectorProperty(name="", description="Particle Emission Range", default=(0.0, 0.0, 0.0), min=0, subtype="XYZ", update=update_values)

    bpy.types.Object.startcolor = FloatVectorProperty(name="", description="Particle Start Color", default=(0.499987, 0.293760, 0.037733), min=0, max=1, step=1, precision=3, subtype="COLOR_GAMMA", size=3, update=update_values)
    bpy.types.Object.endcolor = FloatVectorProperty(name="", description="Particle End Color", default=(0.506654, 0.000000, 0.011944), min=0, max=1, step=1, precision=3, subtype="COLOR_GAMMA", size=3, update=update_values)
    bpy.types.Object.alpha = FloatProperty(name="", description="Particle Alpha Value", default=1.0, min=0, max=1, subtype="FACTOR", update=update_values)
    bpy.types.Object.colorfade_start = IntProperty(name="", description="Adjust the color fading for Particle Lifetime", default=0, min=0, update=update_values)
    bpy.types.Object.colorfade_end = IntProperty(name="", description="Adjust the color fading for Particle Lifetime", default=60, min=1, update=update_values)
    bpy.types.Object.fadein = IntProperty(name="", description="Particle Fade in time", default=10, min=0, update=update_values)
    bpy.types.Object.fadeout = IntProperty(name="", description="Particle Fade out time", default=30, min=0, update=update_values)
    
    bpy.types.Object.randomMovement = FloatProperty(name="", description="Particle Random Movement", default=0, min=0.0, max=math.pi*2, subtype="ANGLE", update=update_values)
    bpy.types.Object.startspeed = FloatProperty(name="", description="Particle Startspeed", default=0.0,min=-100,max=100, update=update_values)
    bpy.types.Object.endspeed = FloatProperty(name="", description="Particle Endspeed", default=10,min=-100,max=100, update=update_values)
    
    bpy.types.Object.particlerotation = FloatProperty(name="", description="Particle Rotation", default=0.0, min=0, max=math.pi*2, subtype="ANGLE", update=update_values)
    bpy.types.Object.halo = BoolProperty(default=True, description="Particle is Facing to the Camera", update=update_values)

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        rd = context.scene.render
        return ob and ob.game and (rd.engine in cls.COMPAT_ENGINES)
    
    def draw(self, context):
        col = self.layout.column()
        row = self.layout.row()
        split = self.layout.split()
        scene = bpy.context.scene
        ob = context.object
        sce = context.scene
        
        if bpy.context.object.particlesystem == True:
            row.label("Emitter Settings", icon="GREASEPENCIL")
            
            row = self.layout.row()
            row.prop(context.object, "emitteron", text="Emitter On")
            row.prop(context.object, "emitterinvisible", text="Emitter Invisible")
            row.prop(context.object, "with_cache", text="With Cache")
            
            row = self.layout.row()
            row.prop(context.object, "frustumCulling", text="Enable Frustum Culling")
            row.prop(context.object, "frustumRadius", text="Radius")
            
            row = self.layout.row()
            row.label("Particles Settings", icon="PREFERENCES")
            
            row = self.layout.row(align=True)
            
            if (not hasattr(scene, "particles")):
                row.label("Particles Not Found, update", icon="ERROR")
            else: row.prop(scene, "particles", text="")
            row.operator("scene.update_particle_list", icon="RECOVER_LAST", text="")
            
            row = self.layout.row()
            row.template_list("UI_UL_list", "particle_list_dummy", ob, "particle_list", ob, "particle_list_index", rows=2)
            col = row.column(align=True)
            
            col.operator("object.particle_to_list", icon="ZOOMIN", text="")
            col.operator("object.particle_from_list", icon="ZOOMOUT", text="")
            
            try:
                row = self.layout.row(align=True)
                row.label("Particle Scale:")
                row.prop(context.object.particle_list[context.object.particle_list_index], "scale", text="Scale")
            except:
                pass    
            
            row = self.layout.row()
            
            
            row.label("Emission Time:")
            row.prop(context.object, "emitTime", text="Tics")
            row = self.layout.row()
            row.label("Particle Lifetime:")
            row.prop(context.object, "lifetime", text="Tics")
            row = self.layout.row()
#            row.label("Particle Random Death:")
#            row.prop(context.object, "randomlifetimevalue", text="Tics")
#            row = self.layout.row()
            row.label("Emission Amount:")
            row.prop(context.object, "amount", text="Amount")
            
            
            row = self.layout.row()
            row.label("Spherical Emission:")
            row.column().prop(context.object, "cone", text="")
            row = self.layout.row()
            row.label("Emission Range:")
            row.column().prop(context.object, "rangeEmit", text="")
            
            row = self.layout.row()
            
            row = self.layout.row()
            row.label("Color Settings", icon="COLOR")
            
            row = self.layout.row().column(align=True)
            row = self.layout.row()
            row.label("Start Color:")
            row.prop(context.object, "startcolor", text="")
            row = self.layout.row()
            row.label("End Color:")
            row.prop(context.object, "endcolor", text="")
            row = self.layout.row()
            row.label("Alpha Value:")
            row.prop(context.object, "alpha", text="")
            row = self.layout.row(align=True)
            row.label("Color Fading:")
            row.label("")
            row.prop(context.object, "colorfade_start", text="Start")
            row.prop(context.object, "colorfade_end", text="End")
            
            row = self.layout.row(align=True)
            row.label("Fade In/Out:")
            row.label("")
            row.prop(context.object, "fadein", text="In")
            row.prop(context.object, "fadeout", text="Out")
            row = self.layout.row()
            
            
            row = self.layout.row()
            row.label("Physics Settings",icon="MOD_ARRAY")
            row = self.layout.row()
            row.label("Particle Rotation:")
            row.prop(context.object, "particlerotation", text="Rotation Speed")
            row = self.layout.row()
            row.label("Start Speed:")
            row.prop(context.object, "startspeed", text="Start Speed")
            
            row = self.layout.row()
            row.label("End Speed:")
            row.prop(context.object, "endspeed", text="End Speed")
            
            row = self.layout.row(align=True)
            row.label("Speed Fading:")
            row.label("")
            row.prop(context.object, "speedfade_start", text="Start")
            row.prop(context.object, "speedfade_end", text="End")
            row = self.layout.row()
            row.label("Random Movement:")
            row.prop(context.object, "randomMovement", text="Random Movement")
            
            
            row = self.layout.row()
            row.label("Start Size:")
            row.column().prop(context.object, "startscale", text="Start Size")
            row = self.layout.row()
            row.label("End Size:")
            row.column().prop(context.object, "endscale", text="End Size")
            row = self.layout.row(align=True)
            row.label("Size Fading:")
            row.label("")
            row.prop(context.object, "scalefade_start", text="Start")
            row.prop(context.object, "scalefade_end", text="End")
            
            row = self.layout.row()
            row = self.layout.row()
            row = self.layout.row()
            row = self.layout.row()
            
            
            row = self.layout.row()
            row.operator("object.delete_particle_system",text="Delete Particle System", icon="CANCEL")
        elif bpy.context.object.particlesystem == False and bpy.context.object.particle == False:
            row = self.layout.row()
            row.operator("scene.generate_particle_system", text="Create Particle System", icon="PARTICLES")
            
        if not "Range_Particle" in bpy.context.object.game.properties and bpy.context.object.particlesystem == False:
            row = self.layout.row()
            addButton = row.operator("object.add_to_particle_list",text="Add To Particle List", icon="PARTICLES")
            addButton.applyToCurrentOb = True
        elif "Range_Particle" in bpy.context.object.game.properties and bpy.context.object.particlesystem == False:
            row = self.layout.row()
            row.operator("object.remove_from_particle_list",text="Remove From Particle List", icon="PARTICLES")     

class delete_particle_system(bpy.types.Operator):
    bl_idname = "object.delete_particle_system" 
    bl_label = "EasyEmit - Delete System"
    bl_description = "Delete Particle System"
    
    def del_particle_logic(self,context):
        for x in range(0,len(bpy.context.object.game.properties)):
            bpy.ops.object.game_property_remove(index=0)
        bpy.ops.logic.python_component_remove(0)

        
    def execute(self, context):
        bpy.context.active_object.draw_type = "TEXTURED"
        self.del_particle_logic(context)
        bpy.context.object.particlesystem = False
        self.report({"INFO"}, "Particle System deleted!")
        return{"FINISHED"}
    


class generate_particle_system(bpy.types.Operator):
    bl_idname = "scene.generate_particle_system" 
    bl_label = "EasyEmit - Generate System"
    bl_description = "Generate New Particle System"
    
    def __init__(self):
        self.particle = False
        self.emitter_mat = False
        self.particle_parent = False
        ##############bpy.ops.object.material_slot_remove()
    
    def createMaterial(self, name):
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = (1, 1, 1)
        mat.type = "WIRE"
        bpy.context.active_object.data.materials.append(bpy.data.materials["Emitter"])
        
    def loadScript(self):
        scriptPath = bpy.utils.script_paths("addons/Range_Particle_Emitter")
        file = scriptPath[0] + "/Range_Emitter.py"
        # print(file)
        bpy.ops.text.open(filepath=file, filter_blender=False, filter_image=False, filter_movie=False, filter_python=True, filter_font=False, filter_sound=False, filter_text=True, filter_btx=False, filter_collada=False, filter_folder=True, filemode=9, internal=True)
        
    def gen_particle_logic(self,context):
        bpy.context.active_object.draw_type = "WIRE"
        try:
            bpy.ops.logic.python_component_register(component_name="Range_Emitter.Range_Emitter")
        except:
            self.loadScript()
            bpy.ops.logic.python_component_register(component_name="Range_Emitter.Range_Emitter")
        bpy.context.object.game.physics_type = "NO_COLLISION"
        
        try:
            iten = bpy.context.object.particle_list[0]
        except:
            item = bpy.context.object.particle_list.add()
            item.name = "Particle_Fire"
 
    def gen_properties(self,context):
        ### frustum Culling
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "culling"
        bpy.context.object.game.properties["culling"].type = "BOOL"
        bpy.context.object.game.properties["culling"].value = True
        
        ### frustum Culling Radius
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "cullingRadius"
        bpy.context.object.game.properties["cullingRadius"].type = "INT"
        bpy.context.object.game.properties["cullingRadius"].value = 4
        
        ### particle list
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "particleList"
        bpy.context.object.game.properties["particleList"].type = "STRING"
        bpy.context.object.game.properties["particleList"].value = "[]"
        
        ### particle list
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "particleAddMode"
        bpy.context.object.game.properties["particleAddMode"].type = "STRING"
        bpy.context.object.game.properties["particleAddMode"].value = "[]"
        
        ### particle list
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "particleScale"
        bpy.context.object.game.properties["particleScale"].type = "STRING"
        bpy.context.object.game.properties["particleScale"].value = "[]"
        
        ### particle emitter on/off
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "emitteron"
        bpy.context.object.game.properties["emitteron"].type = "BOOL"
        bpy.context.object.game.properties["emitteron"].value = True
        
        ### particle emitter cache on/off
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "with_cache"
        bpy.context.object.game.properties["with_cache"].type = "BOOL"
        bpy.context.object.game.properties["with_cache"].value = True
        
        ### particle local or global Emission
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "localEmit"
        bpy.context.object.game.properties["localEmit"].type = "BOOL"
        bpy.context.object.game.properties["localEmit"].value = True
        
        ### particle amount
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "amount"
        bpy.context.object.game.properties["amount"].type = "INT"
        bpy.context.object.game.properties["amount"].value = 1
        
        ### particle emission time
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "emitTime"
        bpy.context.object.game.properties["emitTime"].type = "INT"
        bpy.context.object.game.properties["emitTime"].value = 0
        
        ### particle lifetime
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "lifetime"
        bpy.context.object.game.properties["lifetime"].type = "INT"
        bpy.context.object.game.properties["lifetime"].value = 60
        
        ### particle random lifetime
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "randomlifetimevalue"
        bpy.context.object.game.properties["randomlifetimevalue"].type = "INT"
        bpy.context.object.game.properties["randomlifetimevalue"].value = 10
        
        ### particle range Emit
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "rangeEmitX"
        bpy.context.object.game.properties["rangeEmitX"].type = "FLOAT"
        bpy.context.object.game.properties["rangeEmitX"].value = 0.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "rangeEmitY"
        bpy.context.object.game.properties["rangeEmitY"].type = "FLOAT"
        bpy.context.object.game.properties["rangeEmitY"].value = 0.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "rangeEmitZ"
        bpy.context.object.game.properties["rangeEmitZ"].type = "FLOAT"
        bpy.context.object.game.properties["rangeEmitZ"].value = 0.0
        
        ### particle startcolor
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "start_r"
        bpy.context.object.game.properties["start_r"].type = "FLOAT"
        bpy.context.object.game.properties["start_r"].value = 1.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "start_g"
        bpy.context.object.game.properties["start_g"].type = "FLOAT"
        bpy.context.object.game.properties["start_g"].value = 0.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "start_b"
        bpy.context.object.game.properties["start_b"].type = "FLOAT"
        bpy.context.object.game.properties["start_b"].value = 0.0
        
        ### particle endcolor
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "end_r"
        bpy.context.object.game.properties["end_r"].type = "FLOAT"
        bpy.context.object.game.properties["end_r"].value = 0.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "end_g"
        bpy.context.object.game.properties["end_g"].type = "FLOAT"
        bpy.context.object.game.properties["end_g"].value = 0.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "end_b"
        bpy.context.object.game.properties["end_b"].type = "FLOAT"
        bpy.context.object.game.properties["end_b"].value = 1.0
        
        ### particle alpha
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "alpha"
        bpy.context.object.game.properties["alpha"].type = "FLOAT"
        bpy.context.object.game.properties["alpha"].value = 1.0
        
        ### particle color fade start
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "colorfade_start"
        bpy.context.object.game.properties["colorfade_start"].type = "FLOAT"
        bpy.context.object.game.properties["colorfade_start"].value = 1.0
        
        ### particle color fade end
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "colorfade_end"
        bpy.context.object.game.properties["colorfade_end"].type = "FLOAT"
        bpy.context.object.game.properties["colorfade_end"].value = 1.0
        
        ### particle startspeed
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "startspeed"
        bpy.context.object.game.properties["startspeed"].type = "FLOAT"
        bpy.context.object.game.properties["startspeed"].value = 0.0
        
        ### particle endspeed
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "endspeed"
        bpy.context.object.game.properties["endspeed"].type = "FLOAT"
        bpy.context.object.game.properties["endspeed"].value = 0.1
        
        ### particle random movemen
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "randomMovement"
        bpy.context.object.game.properties["randomMovement"].type = "FLOAT"
        bpy.context.object.game.properties["randomMovement"].value = 0.0
        
        ### particle startscale
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "startscale_x"
        bpy.context.object.game.properties["startscale_x"].type = "FLOAT"
        bpy.context.object.game.properties["startscale_x"].value = 1.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "startscale_y"
        bpy.context.object.game.properties["startscale_y"].type = "FLOAT"
        bpy.context.object.game.properties["startscale_y"].value = 1.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "startscale_z"
        bpy.context.object.game.properties["startscale_z"].type = "FLOAT"
        bpy.context.object.game.properties["startscale_z"].value = 1.0
        
        ### particle endscale
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "endscale_x"
        bpy.context.object.game.properties["endscale_x"].type = "FLOAT"
        bpy.context.object.game.properties["endscale_x"].value = 0.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "endscale_y"
        bpy.context.object.game.properties["endscale_y"].type = "FLOAT"
        bpy.context.object.game.properties["endscale_y"].value = 0.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "endscale_z"
        bpy.context.object.game.properties["endscale_z"].type = "FLOAT"
        bpy.context.object.game.properties["endscale_z"].value = 0.0
        
        ### particle randomscale
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "randomscale"
        bpy.context.object.game.properties["randomscale"].type = "FLOAT"
        bpy.context.object.game.properties["randomscale"].value = 1.0
        
        ### particle scalefade_start
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "scalefade_start"
        bpy.context.object.game.properties["scalefade_start"].type = "INT"
        bpy.context.object.game.properties["scalefade_start"].value = 1
        
        ### particle scalefade_end
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "scalefade_end"
        bpy.context.object.game.properties["scalefade_end"].type = "INT"
        bpy.context.object.game.properties["scalefade_end"].value = 1
        
        ### particle speedfade_start
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "speedfade_start"
        bpy.context.object.game.properties["speedfade_start"].type = "INT"
        bpy.context.object.game.properties["speedfade_start"].value = 1
        
        ### particle speedfade_end
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "speedfade_end"
        bpy.context.object.game.properties["speedfade_end"].type = "INT"
        bpy.context.object.game.properties["speedfade_end"].value = 1
    
        ### particle cone emission
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "coneX"
        bpy.context.object.game.properties["coneX"].type = "FLOAT"
        bpy.context.object.game.properties["coneX"].value = 0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "coneY"
        bpy.context.object.game.properties["coneY"].type = "FLOAT"
        bpy.context.object.game.properties["coneY"].value = 0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "coneZ"
        bpy.context.object.game.properties["coneZ"].type = "FLOAT"
        bpy.context.object.game.properties["coneZ"].value = 0
        
        ### particle fade in/out
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "fadein"
        bpy.context.object.game.properties["fadein"].type = "INT"
        bpy.context.object.game.properties["fadein"].value = 10
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "fadeout"
        bpy.context.object.game.properties["fadeout"].type = "INT"
        bpy.context.object.game.properties["fadeout"].value = 30
        
        ### particle rotation speed
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "rotation"
        bpy.context.object.game.properties["rotation"].type = "FLOAT"
        bpy.context.object.game.properties["rotation"].value = 0
        
        ### particle halo -> particle is facing to camera
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "halo"
        bpy.context.object.game.properties["halo"].type = "BOOL"
        bpy.context.object.game.properties["halo"].value = 1
        
        ### kill the emitter
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties["prop"].name = "kill"
        bpy.context.object.game.properties["kill"].type = "BOOL"
        bpy.context.object.game.properties["kill"].value = 0       
        
    def execute(self, context):
        active_ob = bpy.context.active_object
        self.gen_particle_logic(context)
        self.gen_properties(context)
        bpy.context.object.particlesystem = True
        
        try:
            material = bpy.context.active_object.material_slots["Emitter"]
            #print("Material found!")
        except:
            #print("Material not found!")
            for x in bpy.data.materials:
                if x.name == "Emitter":
                    self.emitter_mat = True
            if self.emitter_mat == False:
                self.createMaterial("Emitter")
            if self.emitter_mat == True:
                bpy.context.active_object.data.materials.append(bpy.data.materials["Emitter"])
        
        
        for x in bpy.context.scene.objects:
            if x.name == "ParticleParent":
                self.particle_parent = True
            if x.name == "Particle_Smooth":
                self.particle = True
        if self.particle == False:
            bpy.ops.scene.create_default_particle()
            
        if self.particle == False:
            bpy.ops.object.add(type="EMPTY", view_align=False, enter_editmode=False, location=(0, -2, 0), rotation=(0, 0, 0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
            bpy.context.active_object.name = "ParticleParent"
        
        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.scene.objects.active = active_ob
        bpy.context.scene.objects[active_ob.name].select = True
        
        
        try:
            bpy.ops.scene.apply_preset()
        except:
            pass
        bpy.ops.object.apply_values()
        
        self.report({"INFO"}, "Particle System added!")
        return{"FINISHED"}


class apply_values(bpy.types.Operator):
    bl_idname = "object.apply_values" 
    bl_label = ""
    
    def execute(self, context):
        try:
            bpy.context.object.game.properties["culling"].value = bpy.context.object.frustumCulling
            bpy.context.object.game.properties["cullingRadius"].value = bpy.context.object.frustumRadius
            
            bpy.context.object.game.properties["start_r"].value = bpy.context.object.startcolor[0]
            bpy.context.object.game.properties["start_g"].value = bpy.context.object.startcolor[1]
            bpy.context.object.game.properties["start_b"].value = bpy.context.object.startcolor[2]
            
            bpy.context.object.game.properties["end_r"].value = bpy.context.object.endcolor[0]
            bpy.context.object.game.properties["end_g"].value = bpy.context.object.endcolor[1]
            bpy.context.object.game.properties["end_b"].value = bpy.context.object.endcolor[2]
            
            bpy.context.object.game.properties["alpha"].value = bpy.context.object.alpha
    
            bpy.context.object.game.properties["colorfade_start"].value = bpy.context.object.colorfade_start
            bpy.context.object.game.properties["colorfade_end"].value = bpy.context.object.colorfade_end
            
            bpy.context.object.game.properties["emitteron"].value = bpy.context.object.emitteron
            bpy.context.object.game.properties["with_cache"].value = bpy.context.object.with_cache
            bpy.context.object.game.properties["emitTime"].value = bpy.context.object.emitTime
            bpy.context.object.game.properties["lifetime"].value = bpy.context.object.lifetime
            bpy.context.object.game.properties["randomlifetimevalue"].value = bpy.context.object.randomlifetimevalue
            bpy.context.object.game.properties["amount"].value = bpy.context.object.amount
            
            bpy.context.object.game.properties["startscale_x"].value = bpy.context.object.startscale
            bpy.context.object.game.properties["startscale_y"].value = bpy.context.object.startscale
            bpy.context.object.game.properties["startscale_z"].value = bpy.context.object.startscale
            
            bpy.context.object.game.properties["endscale_x"].value = bpy.context.object.endscale
            bpy.context.object.game.properties["endscale_y"].value = bpy.context.object.endscale
            bpy.context.object.game.properties["endscale_z"].value = bpy.context.object.endscale
            
            bpy.context.object.game.properties["rangeEmitX"].value = bpy.context.object.rangeEmit[0]
            bpy.context.object.game.properties["rangeEmitY"].value = bpy.context.object.rangeEmit[1]
            bpy.context.object.game.properties["rangeEmitZ"].value = bpy.context.object.rangeEmit[2]
            bpy.context.active_object.dimensions = bpy.context.object.rangeEmit*2 + mathutils.Vector((1,1,1))
    
            
            bpy.context.object.game.properties["scalefade_start"].value = bpy.context.object.scalefade_start
            bpy.context.object.game.properties["scalefade_end"].value = bpy.context.object.scalefade_end
            bpy.context.object.game.properties["speedfade_start"].value = bpy.context.object.speedfade_start
            bpy.context.object.game.properties["speedfade_end"].value = bpy.context.object.speedfade_end
            
            bpy.context.object.game.properties["startspeed"].value = bpy.context.object.startspeed
            bpy.context.object.game.properties["endspeed"].value = bpy.context.object.endspeed
            bpy.context.object.game.properties["randomMovement"].value = bpy.context.object.randomMovement
            
            bpy.context.object.game.properties["coneX"].value = bpy.context.object.cone[0]
            bpy.context.object.game.properties["coneY"].value = bpy.context.object.cone[1]
            bpy.context.object.game.properties["coneZ"].value = bpy.context.object.cone[2]
            
            bpy.context.object.game.properties["fadein"].value = bpy.context.object.fadein
            bpy.context.object.game.properties["fadeout"].value = bpy.context.object.fadeout
            
            bpy.context.object.hide_render = bpy.context.object.emitterinvisible
            
            bpy.context.object.game.properties["localEmit"].value = bpy.context.object.localEmit
            
            bpy.context.object.game.properties["rotation"].value = bpy.context.object.particlerotation
            bpy.context.object.game.properties["halo"].value = bpy.context.object.halo
            #bpy.context.object.particle_list[bpy.context.object.particle_list_index].name = bpy.context.scene.particles
        except:
            pass
        self.report({"INFO"}, "Changes applied!")
        
        
        for i in bpy.context.object.particle_list:
            try:
                if bpy.data.materials[i.name].game_settings.alpha_blend == "ADD":
                    i.addmode = True
                else:
                    i.addmode = False
                #print(i.name,":", i.addmode)
            except:
                self.report({"INFO"}, "No Particle found called:    " + """+i.name + """)
        
        PARTICLES=[]
        SCALE=[]
        ADDMODE=[]
        for i in range(len(bpy.context.object.particle_list)):
            PARTICLES.append(bpy.context.object.particle_list[i].name)
            SCALE.append(bpy.context.object.particle_list[i].scale)
            ADDMODE.append(bpy.context.object.particle_list[i].addmode)
            #print(SCALE)
        bpy.context.object.game.properties["particleList"].value = str(PARTICLES)
        bpy.context.object.game.properties["particleScale"].value = str(SCALE)
        bpy.context.object.game.properties["particleAddMode"].value = str(ADDMODE)
        
        return {"FINISHED"}

#### Particle Preset List
class preset_list(bpy.types.PropertyGroup):
    particles : bpy.props.StringProperty(default="")
    particlesScale : bpy.props.StringProperty(default="")
    addmode : bpy.props.StringProperty(default="")
    name : bpy.props.StringProperty(default="")
    emitTime : bpy.props.IntProperty(default=60)
    lifetime : bpy.props.IntProperty(default=0)
    randomlifetimevalue : bpy.props.IntProperty(default=0)
    amount : bpy.props.IntProperty(default=10)
    cone : bpy.props.FloatVectorProperty(name="",default=(0.261800, 0.261800, 0.261800))
    rangeEmit : bpy.props.FloatVectorProperty(name="",default=(0.0,0.0,0.0))
    startcolor : bpy.props.FloatVectorProperty(name="",default=(0.0,0.0,0.0))
    endcolor : bpy.props.FloatVectorProperty(name="",default=(0.0,0.0,0.0))
    alpha : bpy.props.FloatProperty(default=1.0)
    colorfade_start : bpy.props.IntProperty(default=0)
    colorfade_end : bpy.props.IntProperty(default=60)
    fadein : bpy.props.IntProperty(default=10)
    fadeout : bpy.props.IntProperty(default=30)
    particlerotation : bpy.props.FloatProperty(default=0.0)
    startspeed : bpy.props.FloatProperty(default=0.0)
    endspeed : bpy.props.FloatProperty(default=0.1)
    speedfade_start : bpy.props.IntProperty(default=0)
    speedfade_end : bpy.props.IntProperty(default=60)
    randomMovement : bpy.props.FloatProperty(default=0.0)
    startscale : bpy.props.FloatProperty(default=1.0)
    endscale : bpy.props.FloatProperty(default=1.0)
    scalefade_start : bpy.props.IntProperty(default=1)
    scalefade_end : bpy.props.IntProperty(default=1)

class init_presets(bpy.types.Operator):
    bl_idname = "scene.init_preset" 
    bl_label = ""
    bl_description = "Restore Buildin Presets"
    def __init__(self):
        self.fire = False  
        self.smoke = False
        self.fireball = False
        self.waterfall = False
        self.snow = False
    
    def init_presets(self,particles="'asdasdasdasdasdasd'",particlesScale="",addmode="",name="Fire",emitTime=0,lifetime=60,randomlifetimevalue=0,amount=10,cone=(0,0,0),rangeEmit=(0,0,0),startcolor=(0.499987, 0.293760, 0.037733),endcolor=(0.506654, 0.000000, 0.011944),alpha=1.0,colorfade_start=0,colorfade_end=60,fadein=10,fadeout=30,particlerotation=0,startspeed=0,endspeed=0.1,speedfade_start=0,speedfade_end=60,randomMovement=0,startscale=1.0,endscale=1.0,scalefade_start=0,scalefade_end=0):
        item = bpy.context.scene.preset_list.add()
        item.particles = particles
        item.particlesScale = particlesScale
        item.addmode = addmode
        item.name = name
        item.emitTime = emitTime
        item.lifetime = lifetime
        item.randomlifetimevalue = randomlifetimevalue
        item.amount = amount
        item.cone = cone
        item.rangeEmit = rangeEmit
        item.startcolor = startcolor
        item.endcolor = endcolor
        item.alpha = alpha
        item.colorfade_start = colorfade_start
        item.colorfade_end = colorfade_end
        item.fadein = fadein
        item.fadeout = fadeout
        item.particlerotation = particlerotation
        item.startspeed = startspeed
        item.endspeed = endspeed
        item.speedfade_start = speedfade_start
        item.speedfade_end = speedfade_end
        item.randomMovement = randomMovement
        item.startscale = startscale
        item.endscale = endscale
        item.scalefade_start = scalefade_start
        item.scalefade_end = scalefade_end 
        
    def execute(self, context):
        for item in bpy.context.scene.preset_list:
            if item.name == "Fire":
                self.fire = True
            if item.name == "Smoke":
                self.smoke = True
            if item.name == "Fireball":
                self.fireball = True
            if item.name == "Waterfall":
                self.waterfall = True
            if item.name == "Snow":
                self.snow = True
                
            print("List: ", item.name)
        
                
        if self.fire == False:
            self.init_presets(particles='"Particle_Fire",',particlesScale='"1.0",',addmode='"True"',name='Fire',emitTime=0,lifetime=60,randomlifetimevalue=0,amount=10,cone=(0,0,0),rangeEmit=(0,0,0),startcolor=(0.500000, 0.308322, 0.022600),endcolor=(0.500000, 0.026320, 0.019954),alpha=1.0,colorfade_start=0,colorfade_end=60,fadein=10,fadeout=30,particlerotation=0.001745,startspeed=0,endspeed=10,speedfade_start=1,speedfade_end=60,randomMovement=0.261800,startscale=1.0,endscale=0.8,scalefade_start=0,scalefade_end=60)
        if self.smoke == False:
            self.init_presets(particles='"Particle_Smoke",',particlesScale='"1.0",',addmode='"False"',name='Smoke',emitTime=0,lifetime=60,randomlifetimevalue=0,amount=10,cone=(0,0,0),rangeEmit=(0,0,0),startcolor=(0.5, 0.5, 0.5),endcolor=(0.5, 0.5, 0.5),alpha=1.0,colorfade_start=0,colorfade_end=60,fadein=10,fadeout=50,particlerotation=0.001745,startspeed=5,endspeed=7,speedfade_start=1,speedfade_end=60,randomMovement=0.349066,startscale=1.0,endscale=2.0,scalefade_start=20,scalefade_end=60)
        if self.fireball == False:
            self.init_presets(particles='"Particle_Fire",',particlesScale='"1.0",',addmode='"True"',name='Fireball',emitTime=0,lifetime=60,randomlifetimevalue=0,amount=10,cone=(2*math.pi,2*math.pi,2*math.pi),rangeEmit=(0,0,0),startcolor=(0.459987, 0.283649, 0.020791),endcolor=(0.193321, 0.010176, 0.007715),alpha=1.0,colorfade_start=0,colorfade_end=60,fadein=10,fadeout=50,particlerotation=0.017453,startspeed=0.0,endspeed=2,speedfade_start=1,speedfade_end=60,randomMovement=0.349066,startscale=1.0,endscale=2.0,scalefade_start=20,scalefade_end=60)
        if self.waterfall == False:
            self.init_presets(particles='"Particle_Water",',particlesScale='"1.0",',addmode='"False"',name='Waterfall',emitTime=0,lifetime=180,randomlifetimevalue=0,amount=10,cone=(0,0,0),rangeEmit=(0,1,0),startcolor=(0.534287, 0.816591, 1.000000),endcolor=(0.700371, 0.895857, 1.000000),alpha=1.0,colorfade_start=0,colorfade_end=60,fadein=40,fadeout=100,particlerotation=0.034907,startspeed=5.0,endspeed=-20,speedfade_start=1,speedfade_end=60,randomMovement=0,startscale=1.0,endscale=4.0,scalefade_start=10,scalefade_end=160)
        if self.snow == False:
            self.init_presets(particles='"Particle_Hard",',particlesScale='"0.1",',addmode='"True"',name='Snow',emitTime=0,lifetime=180,randomlifetimevalue=0,amount=7,cone=(0,0,0),rangeEmit=(10,10,0),startcolor=(0.534287, 0.816591, 1.000000),endcolor=(0.700371, 0.895857, 1.000000),alpha=1.0,colorfade_start=0,colorfade_end=60,fadein=40,fadeout=100,particlerotation=0.0,startspeed=-6,endspeed=-6,speedfade_start=1,speedfade_end=60,randomMovement=0.349066,startscale=1.0,endscale=1.0,scalefade_start=10,scalefade_end=160)
        return{'FINISHED'}

class add_preset(bpy.types.Operator):
    bl_idname = "scene.add_preset" 
    bl_label = "Add Particle Preset"        
    bl_description = "Add active Particle Settings to Preset List"
    def execute(self, context):
        item = bpy.context.scene.preset_list.add()
        for x in bpy.context.object.particle_list:
            item.particles += """ + x.name + """ +","
            item.particlesScale += """ + str(x.scale) + """ +","
            item.addmode += """ + str(x.addmode) + """ +","
        item.name = "Preset"
        item.emitTime = bpy.context.active_object.emitTime
        item.lifetime = bpy.context.active_object.lifetime
        item.randomlifetimevalue = bpy.context.active_object.randomlifetimevalue
        item.amount = bpy.context.active_object.amount
        item.cone = bpy.context.active_object.cone
        item.rangeEmit = bpy.context.active_object.rangeEmit
        item.startcolor = bpy.context.active_object.startcolor
        item.endcolor = bpy.context.active_object.endcolor
        item.alpha = bpy.context.active_object.alpha
        item.colorfade_start = bpy.context.active_object.colorfade_start
        item.colorfade_end = bpy.context.active_object.colorfade_end
        item.fadein = bpy.context.active_object.fadein
        item.fadeout = bpy.context.active_object.fadeout
        item.particlerotation = bpy.context.active_object.particlerotation
        item.startspeed = bpy.context.active_object.startspeed
        item.endspeed = bpy.context.active_object.endspeed
        item.speedfade_start = bpy.context.active_object.speedfade_start
        item.speedfade_end = bpy.context.active_object.speedfade_end
        item.randomMovement = bpy.context.active_object.randomMovement
        item.startscale = bpy.context.active_object.startscale
        item.endscale = bpy.context.active_object.endscale
        item.scalefade_start = bpy.context.active_object.scalefade_start
        item.scalefade_end = bpy.context.active_object.scalefade_end
        return{"FINISHED"}
    
class remove_preset(bpy.types.Operator):
    bl_idname = "scene.remove_preset" 
    bl_label = "Add Particle Preset" 
    bl_description = "Remove active Preset Item"       
    
    def execute(self, context):
        item = bpy.context.scene.preset_list.remove(bpy.context.scene.preset_list_index)
        return{"FINISHED"}


class apply_preset(bpy.types.Operator):
    bl_idname = "scene.apply_preset" 
    bl_label = ""
    bl_description = "Apply Preset to active Particle System"
    
    def execute(self,context):
        scene = bpy.context.scene
        particles = eval(scene.preset_list[scene.preset_list_index]["particles"])
        particlesScale = eval(scene.preset_list[scene.preset_list_index]["particlesScale"])
        addmode = eval(scene.preset_list[scene.preset_list_index]["addmode"])
        # print("addmode:", addmode)
        for i in range(len(bpy.context.object.particle_list)):
            bpy.context.object.particle_list.remove(0)
        for i in range(len(particles)):
            item = bpy.context.object.particle_list.add()
            item.name = particles[i]
            item.scale = float(particlesScale[i])
            # print(addmode[i])
            if addmode[i] == "T":
                item.addmode = True
            else:
                item.addmode = False
            
        context.object.emitTime = scene.preset_list[scene.preset_list_index]["emitTime"]
        context.object.lifetime = scene.preset_list[scene.preset_list_index]["lifetime"]
        context.object.randomlifetimevalue = scene.preset_list[scene.preset_list_index]["randomlifetimevalue"]
        context.object.amount = scene.preset_list[scene.preset_list_index]["amount"]
        context.object.cone = scene.preset_list[scene.preset_list_index]["cone"]
        context.object.rangeEmit = scene.preset_list[scene.preset_list_index]["rangeEmit"]
        context.object.startcolor = scene.preset_list[scene.preset_list_index]["startcolor"]
        context.object.endcolor = scene.preset_list[scene.preset_list_index]["endcolor"]
        context.object.alpha = scene.preset_list[scene.preset_list_index]["alpha"] 
        context.object.colorfade_start = scene.preset_list[scene.preset_list_index]["colorfade_start"]
        context.object.colorfade_end = scene.preset_list[scene.preset_list_index]["colorfade_end"]
        context.object.fadein = scene.preset_list[scene.preset_list_index]["fadein"]
        context.object.fadeout = scene.preset_list[scene.preset_list_index]["fadeout"]
        context.object.particlerotation = scene.preset_list[scene.preset_list_index]["particlerotation"]
        context.object.startspeed = scene.preset_list[scene.preset_list_index]["startspeed"]
        context.object.endspeed = scene.preset_list[scene.preset_list_index]["endspeed"]
        context.object.randomMovement = scene.preset_list[scene.preset_list_index]["randomMovement"]
        context.object.startscale = scene.preset_list[scene.preset_list_index]["startscale"]
        context.object.endscale = scene.preset_list[scene.preset_list_index]["endscale"]
        context.object.scalefade_start = scene.preset_list[scene.preset_list_index]["scalefade_start"]
        context.object.scalefade_end = scene.preset_list[scene.preset_list_index]["scalefade_end"]
        return{"FINISHED"}
    
    
    

#### Particle List
class particle_list(bpy.types.PropertyGroup):
    def update_values(self, context):
        bpy.ops.object.apply_values()
    name : bpy.props.StringProperty(default="")
    scale : bpy.props.FloatProperty(default=1.0,update=update_values)
    addmode : bpy.props.BoolProperty(default=True)
    
class particle_to_list(bpy.types.Operator):
    bl_idname = "object.particle_to_list" 
    bl_label = ""        
    
    def execute(self, context):
        
        item = bpy.context.object.particle_list.add()
        #item.name = bpy.context.scene.objects[int(bpy.context.scene.object_list[0])].name
        item.name = bpy.context.scene.particles
        item.scale = 1.0
        item.addmode = True
        #print(bpy.context.object.particle_list)
        bpy.ops.object.apply_values()
        return{"FINISHED"}
    
class particle_from_list(bpy.types.Operator):
    bl_idname = "object.particle_from_list" 
    bl_label = ""
    
    def __init__(self):
        pass
        
    
    def execute(self, context):
        bpy.ops.object.apply_values()
        item = bpy.context.object.particle_list.remove(bpy.context.object.particle_list_index)
        #print(bpy.context.object.particle_list)
        bpy.ops.object.apply_values()
        return{"FINISHED"}
    
class add_to_particle_list(bpy.types.Operator):
    bl_idname = "object.add_to_particle_list" 
    bl_label = "easyEmit - Add Particle To List"
    
    applyToCurrentOb : BoolProperty(default=False)
    
    def __init__(self):
        self.PARTICLE_NAMES = []
        self.current_ob = bpy.context.active_object
    
    def execute(self, context):
        try:
            if (self.applyToCurrentOb):
                bpy.context.active_object.data.materials[0].use_object_color = True
                scene = bpy.context.scene.name
                #self.current_ob.particle = True
                bpy.ops.object.game_property_new()
                bpy.context.object.game.properties["prop"].name = "Range_Particle"
            
            # XXX
            for x in bpy.data.scenes[scene].objects:
                bpy.data.scenes[scene].objects.active = x
                ob = bpy.context.active_object
                if "Range_Particle" in ob.game.properties:
                    name = ob.name
                    self.PARTICLE_NAMES.append((name,name,name))
                    #print(name)
            
            self.PARTICLE_NAMES.sort()
            bpy.types.Scene.particles = EnumProperty(
                                                    items = self.PARTICLE_NAMES,
                                                    name = "choose a Particle")
            bpy.data.scenes[scene].objects.active = self.current_ob
        except:
            self.report({"WARNING"}, "Particle has no Material!")
            
        return {"FINISHED"}

class remove_from_particle_list(bpy.types.Operator):
    bl_idname = "object.remove_from_particle_list" 
    bl_label = "EasyEmit - Remove Particle From List"
    
    def __init__(self):
        self.PARTICLE_NAMES = []
        self.current_ob = bpy.context.active_object
    
    def execute(self, context):
        scene = bpy.context.scene.name     
        #self.current_ob.particle = False
        bpy.ops.object.game_property_remove(0)

        # XXX
        for x in bpy.data.scenes[scene].objects:
            ob = bpy.context.active_object
            bpy.data.scenes[scene].objects.active = x
            if "Range_Particle" in ob.game.properties:
                name = ob.name
                self.PARTICLE_NAMES.append((name,name,name))
                # print(name)
        bpy.types.Scene.particles = EnumProperty(
        items = self.PARTICLE_NAMES,
        name = "choose a Particle")
        bpy.data.scenes[scene].objects.active = self.current_ob
        
        return {"FINISHED"}

class update_particle_list(bpy.types.Operator):
    bl_idname = "scene.update_particle_list" 
    bl_description = "Update particles list"
    bl_label = ""
    
    def __init__(self):
        self.PARTICLE_NAMES = []
        self.current_ob = bpy.context.active_object
    
    def execute(self, context):
        scene = bpy.context.scene.name

        for x in bpy.data.scenes[scene].objects:
            ob = bpy.context.active_object
            bpy.data.scenes[scene].objects.active = x
            if "Range_Particle" in ob.game.properties:
                name = ob.name
                self.PARTICLE_NAMES.append((name,name,name))
                #print(name)
        bpy.types.Scene.particles = EnumProperty(
        items = self.PARTICLE_NAMES,
        name = "choose a Particle")
        bpy.data.scenes[scene].objects.active = self.current_ob
        return{"FINISHED"}

class create_default_particle(bpy.types.Operator):
    bl_idname = "scene.create_default_particle"
    bl_label = ""
    
    #def loadScript(self):
    #    scriptPath = bpy.utils.script_paths("addons/easyEmit")
    #    file = scriptPath[0] + "/Range_Emitter.py"
    #    print(file)
    #    bpy.ops.text.open(filepath=file, filter_blender=False, filter_image=False, filter_movie=False, filter_python=True, filter_font=False, filter_sound=False, filter_text=True, filter_btx=False, filter_collada=False, filter_folder=True, filemode=9, internal=True)
    #
    #def createParticle(self,name,nameNew,position,type,shadeless,addmode):
    #    ...
        
    def loadPresetParticlefromFile(self, directory, name):
        bpy.ops.wm.append(filename=name,
                          directory=directory)
        
        object = bpy.context.scene.objects.get(name)
        
        
        # Set Layers
        object.layers[19] = True
        for i in range(18):
            object.layers[i] = False
        
        # bpy.ops.object.select_all(action='DESELECT')
        # object.select = True
        
        # bpy.ops.object.add_to_particle_list()
        bpy.ops.scene.update_particle_list()
    
    def execute(self, context):
        #self.createParticle("particle_smooth","Particle_Smooth",0,"Plane",True,True)
        #self.createParticle("particle_hard","Particle_Hard",2,"Plane",True,True)
        #self.createParticle("particle_scattered","Particle_Scattered",4,"Plane",True,True)
        #self.createParticle("particle_fire","Particle_Fire",6,"Plane",True,True)
        #self.createParticle("particle_star","Particle_Star",8,"Plane",True,True)
        #self.createParticle("particle_blade","Particle_Blade",10,"Plane",True,True)
        #self.createParticle("particle_smoke","Particle_Smoke",12,"Volume",False,False)
        #self.createParticle("particle_smoke","Particle_Water",12,"PlaneShaded",False,False)
        
        filepath_with_directory = bpy.utils.script_paths("addons/Range_Particle_Emitter/presets")[0] + "/particles.range/Object/"
        
        # Load Particle Objects here
        self.loadPresetParticlefromFile(filepath_with_directory, "Particle_Smooth")
        self.loadPresetParticlefromFile(filepath_with_directory, "Particle_Hard")
        self.loadPresetParticlefromFile(filepath_with_directory, "Particle_Scattered")
        self.loadPresetParticlefromFile(filepath_with_directory, "Particle_Fire")
        self.loadPresetParticlefromFile(filepath_with_directory, "Particle_Star")
        self.loadPresetParticlefromFile(filepath_with_directory, "Particle_Star_2")
        self.loadPresetParticlefromFile(filepath_with_directory, "Particle_Blade")
        self.loadPresetParticlefromFile(filepath_with_directory, "Particle_Smoke")
        self.loadPresetParticlefromFile(filepath_with_directory, "Particle_Water")
        
        # self.loadScript()
        
        return {"FINISHED"}

class save_preset(bpy.types.Operator, ExportHelper):
    bl_idname = "export.save_preset" 
    bl_label = "export Preset"
    bl_description="Save Particle Presets on Disc"
    
    # ExportHelper mixin class uses this
    filename_ext = ".eep"

    filter_glob = StringProperty(
            default="*.eep",
            options={"HIDDEN"},
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting = None
  
    def __init__(self):
        self.data = []
    
    def generate_list(self):
        presets = bpy.context.scene.preset_list
        for preset in presets:
            particleDict = dict()
            particleDict["addmode"] = preset.addmode
            particleDict["alpha"] = preset.alpha
            particleDict["amount"] = preset.amount
            particleDict["colorfade_start"] = preset.colorfade_start
            particleDict["colorfade_end"] = preset.colorfade_end
            particleDict["coneX"] = preset.cone[0]
            particleDict["coneY"] = preset.cone[1]
            particleDict["coneZ"] = preset.cone[2]
            particleDict["emitTime"] = preset.emitTime
            particleDict["endcolorR"] = preset.endcolor[0]
            particleDict["endcolorG"] = preset.endcolor[1]
            particleDict["endcolorB"] = preset.endcolor[2]
            particleDict["endscale"] = preset.endscale
            particleDict["endspeed"] = preset.endspeed
            particleDict["fadein"] = preset.fadein
            particleDict["fadeout"] = preset.fadeout
            particleDict["lifetime"] = preset.lifetime
            particleDict["name"] = preset.name
            particleDict["particlerotation"] = preset.particlerotation
            particleDict["particles"] = preset.particles
            particleDict["particlesScale"] = preset.particlesScale
            particleDict["randomMovement"] = preset.randomMovement
            particleDict["randomlifetimevalue"] = preset.randomlifetimevalue
            particleDict["rangeEmitX"] = preset.rangeEmit[0]
            particleDict["rangeEmitY"] = preset.rangeEmit[1]
            particleDict["rangeEmitZ"] = preset.rangeEmit[2]
            particleDict["scalefade_end"] = preset.scalefade_end
            particleDict["scalefade_start"] = preset.scalefade_start
            particleDict["speedfade_end"] = preset.speedfade_end
            particleDict["speedfade_start"] = preset.speedfade_start
            particleDict["startcolorR"] = preset.startcolor[0]
            particleDict["startcolorG"] = preset.startcolor[1]
            particleDict["startcolorB"] = preset.startcolor[2]
            particleDict["startscale"] = preset.startscale
            particleDict["startspeed"] = preset.startspeed
            self.data.append(particleDict)
        #print(self.data)
            
    def save_preset(self, data, filepath,use_setting):
        file = open(filepath, "wb")
        pickle.dump(data, file)
        file.close()
        return {"FINISHED"}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        self.generate_list()
         
        filepath = bpy.utils.script_paths("addons/Range_Particle_Emitter/")
        file = filepath[0] + "preset.ee"
        return self.save_preset(self.data,self.filepath, self.use_setting)
        self.report({"INFO"}, "EasyEmit Preset exported!")
        return{"FINISHED"}
    
class load_preset(bpy.types.Operator, ExportHelper):
    bl_idname = "export.load_preset" 
    bl_label = "import Preset"
    bl_description="Load Particle Presets"
    
    # ExportHelper mixin class uses this
    filename_ext = ".eep"

    filter_glob = StringProperty(
            default="*.eep",
            options={"HIDDEN"},
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting = None
    
    def __init__(self):
        self.data = []
    
    def load_preset(self,filepath):
        file = open(filepath, "rb")
        self.data = pickle.load(file)
        return {"FINISHED"}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        filepath = bpy.utils.script_paths("addons/Range_Particle_Emitter/")
        file = filepath[0] + "preset.ee"
        self.load_preset(self.filepath)
        #print(self.data[0]["startcolor"])
        
        for particleDict in self.data:
            item = bpy.context.scene.preset_list.add()
            item.addmode = particleDict["addmode"]
            item.alpha = particleDict["alpha"]
            item.amount = particleDict["amount"]
            item.colorfade_start = particleDict["colorfade_start"]
            item.colorfade_end = particleDict["colorfade_end"]
            item.cone[0] = particleDict["coneX"]
            item.cone[1] = particleDict["coneY"]
            item.cone[2] = particleDict["coneZ"]
            item.emitTime = particleDict["emitTime"]
            item.endcolor[0] = particleDict["endcolorR"]
            item.endcolor[1] = particleDict["endcolorG"]
            item.endcolor[2] = particleDict["endcolorB"]
            item.endscale = particleDict["endscale"]
            item.endspeed = particleDict["endspeed"]
            item.fadein = particleDict["fadein"]
            item.fadeout = particleDict["fadeout"]
            item.lifetime = particleDict["lifetime"]
            item.name = particleDict["name"]
            item.particlerotation = particleDict["particlerotation"]
            item.particles = particleDict["particles"]
            item.particlesScale = particleDict["particlesScale"]
            item.randomMovement = particleDict["randomMovement"]
            item.randomlifetimevalue = particleDict["randomlifetimevalue"]
            item.rangeEmit[0] = particleDict["rangeEmitX"]
            item.rangeEmit[1] = particleDict["rangeEmitY"]
            item.rangeEmit[2] = particleDict["rangeEmitZ"]
            item.scalefade_end = particleDict["scalefade_end"]
            item.scalefade_start = particleDict["scalefade_start"]
            item.speedfade_end = particleDict["speedfade_end"]
            item.speedfade_start = particleDict["speedfade_start"]
            item.startcolor[0] = particleDict["startcolorR"]
            item.startcolor[1] = particleDict["startcolorG"]
            item.startcolor[2] = particleDict["startcolorB"]
            item.startscale = particleDict["startscale"]
            item.startspeed = particleDict["startspeed"]
        self.report({"INFO"}, "easyEmit Preset imported!")
        
        return{"FINISHED"}


classes = (
    EasyEmitPresets,
    EasyEmit,
    apply_preset,
    init_presets,
    preset_list,
    add_preset,
    remove_preset,
    generate_particle_system,
    delete_particle_system,
    apply_values,
    particle_list,
    particle_to_list,
    particle_from_list,
    create_default_particle,
    add_to_particle_list,
    remove_from_particle_list,
    update_particle_list,
    save_preset,
    load_preset,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Object.particle_list = bpy.props.CollectionProperty(type=particle_list)
    bpy.types.Object.particle_list_index = bpy.props.IntProperty()
    
    bpy.types.Scene.preset_list = bpy.props.CollectionProperty(type=preset_list)
    bpy.types.Scene.preset_list_index = bpy.props.IntProperty()
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
if __name__ == "__main__":
    register()
