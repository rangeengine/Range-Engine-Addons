# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

import bpy
import bgl
import blf
from bpy_extras import view3d_utils

import math
import mathutils
import random
from bpy.props import *
from mathutils import *

# bpy.mifthCloneTools = dict()

global drawForClonesObj
drawForClonesObj = []  # Array of Objects Names


# groups
def getGroups(scene, context):

    lst = []
    obj = context.scene.objects.active
    for group in bpy.data.groups:
        if obj is not None and obj.name in group.objects:
            lst.append((group.name, group.name, ""))

    return lst


class MFTCloneProperties(bpy.types.PropertyGroup):
    # Draw Cloned Settings
    drawClonesDirectionRotate: BoolProperty(
        name="drawClonesDirectionRotate",
        description="drawClonesDirectionRotate...",
        default=False
    )

    drawClonesRadialRotate: BoolProperty(
        name="drawClonesRadialRotate",
        description="drawClonesRadialRotate...",
        default=True
    )

    drawClonesNormalRotate: BoolProperty(
        name="drawClonesNormalRotate",
        description="drawClonesNormalRotate...",
        default=True
    )

    drawClonesOptimize: BoolProperty(
        name="drawClonesOptimize",
        description="drawClonesOptimize...",
        default=True
    )

    drawStrokeLength: FloatProperty(
        default=4,
        min=0.001,
        max=500.0
    )

    drawRandomStrokeScatter: FloatProperty(
        default=10,
        min=0.0,
        max=500.0
    )

    randNormalRotateClone: FloatProperty(
        default=0.0,
        min=0.0,
        max=180.0
    )

    randDirectionRotateClone: FloatProperty(
        default=0.0,
        min=0.0,
        max=180.0
    )

    randScaleClone: FloatProperty(
        default=0.0,
        min=0.0,
        max=0.99
    )

    drawPressure: FloatProperty(
        default=0.7,
        min=0.0,
        max=0.95
    )

    drawPressureRelativeStroke: BoolProperty(
        name="drawPressureRelativeStroke",
        description="Relative Stroke To Scale and Pressure",
        default=True
    )

    drawPressureScale: BoolProperty(
        name="drawPressureScale",
        description="Pressure for Scale",
        default=True
    )

    drawPressureScatter: BoolProperty(
        name="drawPressureScatter",
        description="Pressure for Scatter",
        default=True
    )

    drawClonesAxis: EnumProperty(
        items=(('X', 'X', ''),
               ('-X', '-X', ''),
               ('Y', 'Y', ''),
               ('-Y', '-Y', ''),
               ('Z', 'Z', ''),
               ('-Z', '-Z', '')
               ),
        default = 'Z'
    )

    # Radial Clone Settings
    radialClonesAxis: EnumProperty(
        items=(('X', 'X', ''),
               ('Y', 'Y', ''),
               ('Z', 'Z', '')
               ),
        default = 'Z'
    )

    radialClonesAxisType: EnumProperty(
        items=(('Global', 'Global', ''),
               ('Local', 'Local', '')
               ),
        default = 'Global'
    )

    # GroupInstance to Cursor
    getGroupsLst: EnumProperty(name='Get Groups',
                                description='Get Groups.',
                                items=getGroups)

def draw_line_3d(color, start, end):
    bgl.glLineWidth(5.0)
    bgl.glColor4f(*color)
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex3f(*start)
    bgl.glVertex3f(*end)
    bgl.glEnd()
    
def draw_callback_3d(operator, context):
        mifthCloneTools = bpy.context.scene.mifthCloneTools
        if (operator.rayCastCircle[0]):
            pos = operator.rayCastCircle[1] 
            normal = operator.rayCastCircle[0].normalized()
            pos += (normal * 0.1)
            bgl.glTranslatef(pos[0], pos[1], pos[2])

            # Calculates the angle of rotation with respect to the z axis
            angle = math.degrees(math.acos(normal.z))

            # RanGE: Calculates the axis of rotation as the cross product between the normal vector and the z axis
            axis = Vector((0, 0, 1)).cross(normal).normalized()
            bgl.glRotatef(angle, axis.x, axis.y, axis.z)  # Rotaciona em torno do eixo de rotação
        
        radius = int(mifthCloneTools.drawRandomStrokeScatter)
        # Draw Circle
        bgl.glLineWidth(5.0)
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
        bgl.glDisable(bgl.GL_DEPTH_TEST)
        
        bgl.glBegin(bgl.GL_LINE_LOOP)
        bgl.glColor4f(0.1, 0.1, 0.1, 0.5)
        num_segments = 36
        radius = int(mifthCloneTools.drawRandomStrokeScatter)
        for i in range(num_segments):
            angle = i * 2.0 * math.pi / num_segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            bgl.glVertex2f(x, y)
        bgl.glEnd()

        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        bgl.glColor4f(0.4, 0.4, 0.4, 0.5)
        bgl.glVertex2f(0.0, 0.0)
        inner_radius_scale = 1
        inner_radius = radius * inner_radius_scale
        for i in range(num_segments + 1):
            angle = i * 2.0 * math.pi / num_segments
            x = inner_radius * math.cos(angle)
            y = inner_radius * math.sin(angle)
            bgl.glVertex2f(x, y)
        bgl.glEnd()
        
        # 3D SPHERE #
        bgl.glEnable(bgl.GL_DEPTH_TEST)
        segments = 32 # the number of segments that will form the sphere

        # saves the current state of the transformation matrix
        bgl.glPushMatrix()
        
        # Basic Defs
        bgl.glColor4f(0.2, 0.2, 0.2, 0.5)
        center = (0, 0, 0)
        
        # Draw 3D Sphere
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        for i in range(segments//2):
            theta = i * math.pi / segments
            for j in range(segments):
                phi = j * 2 * math.pi / segments
                x = center[0] + radius * math.sin(theta) * math.cos(phi)
                y = center[1] + radius * math.sin(theta) * math.sin(phi)
                z = center[2] + radius * math.cos(theta)
                bgl.glVertex3f(x, y, z)
        bgl.glEnd()

        # restores the previous state of the transformation matrix
        bgl.glPopMatrix()
        # END 3D SPHERE #
        
        # restore opengl defaults
        bgl.glLineWidth(1)
        bgl.glDisable(bgl.GL_BLEND)
        bgl.glDisable(bgl.GL_LINE_SMOOTH)
        #bgl.glDisable(bgl.GL_DEPTH_TEST)
        
def draw_callback_2DCloneUIText(operator, context):
    # Drow Text
    # Get window dimensions
    region = context.region
    win_width = region.width
    win_height = region.height
    
    # Set font properties
    font_id = 0
    font_size = 20
    blf.size(font_id, font_size, 72)  # Font size, dpi
    
    text = "LEFTMOUSE - Draw / RIGHTMOUSE - Remove / ESC - Stop Drawing"

    # Set text position to center of screen
    text_width, text_height = blf.dimensions(font_id, text)
    pos_x = (win_width - text_width) / 2
    pos_y = (win_height - text_height)
    
    # Draw a square on the background of the text
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 0.5)
    margin_x = 10
    margin_y = 5
    quad_width = (font_size / 2.0) * (len(text) - 1.5) + margin_x * 2
    quad_height = font_size + margin_y * 2
    bgl.glRectf(pos_x - margin_x, pos_y - margin_y, pos_x + quad_width, pos_y + quad_height)
    bgl.glDisable(bgl.GL_BLEND)

    # Draw text
    bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
    blf.position(font_id, pos_x, pos_y, 0)  # Text position
    blf.draw(font_id, text)  # Text content
    
    
class MFTPanelCloning(bpy.types.Panel):
    bl_label = "Object Pencil"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_category = 'RanGE'
    # bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        mifthTools = bpy.context.scene.mifthTools
        mifthCloneTools = bpy.context.scene.mifthCloneTools

        layout.label(text="Draw Clones: {}".format(drawForClonesObj))
        layout.operator("mft.draw_clones", text="DrawClones", icon="STYLUS_PRESSURE")
        layout.operator("mft.pick_obj_to_clone_draw", text="PickObjects", icon="EYEDROPPER")
        row = layout.row()
        row.prop(mifthCloneTools, "drawClonesDirectionRotate", text='DirectionRotate')
        row.prop(mifthCloneTools, "drawClonesRadialRotate", text='RadialRotate')
        row = layout.row()
        row.prop(mifthCloneTools, "drawClonesNormalRotate", text='NormalRotate')
        row.prop(mifthCloneTools, "drawClonesOptimize", text='Optimize')

        layout.prop(mifthCloneTools, "drawStrokeLength", text='Stroke')

        layout.prop(mifthCloneTools, "drawRandomStrokeScatter", text="Radius Scatter")
        layout.prop(
            mifthCloneTools, "randNormalRotateClone", text='RandNormal')
        layout.prop(
            mifthCloneTools, "randDirectionRotateClone", text='RandDirection')
        layout.prop(mifthCloneTools, "randScaleClone", text='RandScale')

        layout.prop(mifthCloneTools, "drawPressure", text='DrawPressure')
        row = layout.row()
        row.prop(mifthCloneTools, "drawPressureRelativeStroke", text="S")
        row.prop(mifthCloneTools, "drawPressureScale", text="S")
        row.prop(mifthCloneTools, "drawPressureScatter", text="S")

        layout.prop(mifthCloneTools, "drawClonesAxis", text='Axis')
        layout.separator(factor=1)

        layout.label(text="Clone Selected:")
        layout.operator("mft.clonetoselected", text="CloneToSelected")
        layout.separator(factor=1)

        layout.label(text="Radial Clone:")
        layout.operator("mft.radialclone", text="Radial Clone")
        # layout.prop(mifthTools, "radialClonesNumber", text='')
        row = layout.row()
        row.prop(mifthCloneTools, "radialClonesAxis", text='')
        row.prop(mifthCloneTools, "radialClonesAxisType", text='')
        layout.separator(factor=1)

        layout.label(text="Position Group:")
        layout.operator("mft.group_instance_to_cursor", text="Position Group")
        layout.prop(mifthCloneTools, "getGroupsLst", text='')
        layout.separator(factor=1)

        layout.operator("mft.group_to_mesh", text="Groups To Mesh")


class MFTDrawClones(bpy.types.Operator):
    bl_idname = "mft.draw_clones"
    bl_label = "Draw Clones"
    bl_description = "Draw Clones with Mouse"
    bl_options = {'REGISTER', 'UNDO'}

    doPick = False
    tabletPressure = 1.0
    drawOnObjects = None  # List of objects on which will be drawn
    obj_Active_True = None  # Active object befor starting drawing
    dupliList = None  # duplilist of objects for picking stuff
    currentStrokeList = None  # this is a stroke
    allStrokesList = None  # this is all strokes

    pass_keys = ['NUMPAD_0', 'NUMPAD_1', 'NUMPAD_3', 'NUMPAD_4',
                 'NUMPAD_5', 'NUMPAD_6', 'NUMPAD_7', 'NUMPAD_8',
                 'NUMPAD_9', 'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE']
            
    def modal(self, context, event):
        mifthCloneTools = bpy.context.scene.mifthCloneTools
        #self.draw(context)
        region = context.region
        rv3d = context.region_data
        coord = event.mouse_region_x, event.mouse_region_y
        # get the ray from the viewport and mouse
        view_vector_mouse = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
        ray_origin_mouse = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
        
        ray = mft_obj_ray_cast(self.dupliList[0][0], self.dupliList[0][1], view_vector_mouse, ray_origin_mouse)
        self.rayCastCircle = ray
        
        if (self._handle_3d):
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_3d, "WINDOW")
            self._handle_3d = None

        if event.type in self.pass_keys:
            # allow navigation
            return {"PASS_THROUGH"} 
            
        elif event.type in {"ESC"}:
            finish_drawing(self, context)
            bpy.types.SpaceView3D.draw_handler_remove(self._uiTextCallback, "WINDOW")
            return {"FINISHED"}
            
        elif event.type == "MOUSEMOVE":
            if (self._handle_3d == None):
                self._handle_3d = bpy.types.SpaceView3D.draw_handler_add(draw_callback_3d, (self, context), "WINDOW", "POST_VIEW")
                
        elif event.type == "LEFTMOUSE" and event.value == "PRESS":
            self.doPick = True
            self.currentStrokeList = []

            if (self._handle_3d == None):
                self._handle_3d = bpy.types.SpaceView3D.draw_handler_add(draw_callback_3d, (self, context), 'WINDOW', 'POST_VIEW')
                
        elif event.type == "RIGHTMOUSE" and event.value == "PRESS":
            self.deleteMode = True
            
        elif event.type == "RIGHTMOUSE" and event.value == "RELEASE":
            self.deleteMode = False

        elif event.type == "LEFTMOUSE" and event.value == "RELEASE":
            self.doPick = False
            self.allStrokesList.append(self.currentStrokeList)
            
            # Do optimization
            if mifthCloneTools.drawClonesOptimize is True and self.currentStrokeList is not None:
                for point in self.currentStrokeList:
                    copy_settings_clones(point.objNew, point.objOriginal)
            self.currentStrokeList = None
            
        if self.doPick is True:
            self.tabletPressure = event.pressure
            mft_pick_and_clone(self, context, event)
            
        if (self.deleteMode):
            radius = int(mifthCloneTools.drawRandomStrokeScatter)
            #self.allStrokesList[0][0].objNew.delete()
            #print(type(self.allStrokesList[0][0].objNew))

            pencilPos = self.rayCastCircle[1]
            indices = []
            if (pencilPos != None):
                for list in self.allStrokesList:
                    listtemp = []
                    for index, obj in enumerate(list):
                        dist = (obj.objNew.location - pencilPos).length
                        # print(dist, mifthCloneTools.drawRandomStrokeScatter)
                        if (dist < mifthCloneTools.drawRandomStrokeScatter):
                            listtemp.append(index)
                    #indices.append(listtemp)

                    #print(indices, len(self.allStrokesList[0]))
                    # Delete Objects
                    #for indexList, list in enumerate(indices):
                    for index in sorted(listtemp, reverse=True):
                        indexStrokesList = self.allStrokesList.index(list)
                        if (index <= (len(self.allStrokesList[indexStrokesList]) - 1)):
                            objn = self.allStrokesList[indexStrokesList].pop(index)
                            bpy.data.objects.remove(objn.objNew)

                if (self._handle_3d == None):
                    self._handle_3d = bpy.types.SpaceView3D.draw_handler_add(draw_callback_3d, (self, context), 'WINDOW', 'POST_VIEW')
                    
                # Update Viewport
                for area in bpy.context.window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()

                
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        mifthCloneTools = bpy.context.scene.mifthCloneTools
        self.rayCastCircle = None
        self._handle_3d = None
        self._uiTextCallback = None
        self.deleteMode = False

        # global drawForClonesObj
        if len(drawForClonesObj) == 0 or len(context.selected_objects) == 0:
            self.report({'WARNING'}, "Pick Objects to Clone")
            return {'CANCELLED'}

        for obj_name in drawForClonesObj:
            if obj_name not in context.scene.objects:
                self.report({'WARNING'}, "Picked Object was Deleted!")
                return {'CANCELLED'}
                break

        if context.space_data.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)
            self._uiTextCallback = bpy.types.SpaceView3D.draw_handler_add(draw_callback_2DCloneUIText, (self, context), 'WINDOW', 'POST_PIXEL')
            prepare_drawing(self, context)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}

class MFTPickObjToDrawClone(bpy.types.Operator):
    bl_idname = "mft.pick_obj_to_clone_draw"
    bl_label = "Pick"
    bl_description = "Pick To Clone"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mifthCloneTools = context.scene.mifthCloneTools

        if len(context.selected_objects) > 0:
            # global drawForClonesObj
            drawForClonesObj.clear()
            for obj in context.selected_objects:
                drawForClonesObj.append(obj.name)

        return {'FINISHED'}


class MTFDCPoint:
    def __init__(self, objNew, objOriginal, hitPoint, hitNormal):
        self.objNew, self.objOriginal, self.hitPoint, self.hitNormal = objNew, objOriginal, hitPoint, hitNormal


# Just prepare some stuff
def prepare_drawing(self, context):
    self.drawOnObjects = context.selected_objects
    for obj in self.drawOnObjects:
        obj.select = False
    self.obj_Active_True = context.scene.objects.active

    self.dupliList = mft_selected_objects_and_duplis(self, context)
    self.allStrokesList = []

# Just clear some stuff at the end
def finish_drawing(self, context):
    for obj in self.drawOnObjects:
        obj.select = True
    context.scene.objects.active = self.obj_Active_True
    self.drawOnObjects = None
    self.dupliList = None

    if self.allStrokesList is not None:
        for stroke in self.allStrokesList:
            if stroke is not None:
                stroke.clear()
        self.allStrokesList.clear()
    self.allStrokesList = None

    if self.currentStrokeList is not None:
        self.currentStrokeList.clear()
    self.currentStrokeList = None


def mft_selected_objects_and_duplis(self, context):
    """Loop over (object, matrix) pairs (mesh only)"""

    listObjMatrix = []
    for obj in self.drawOnObjects:
        if obj.type == 'MESH':
            listObjMatrix.append((obj, obj.matrix_world.copy()))

        if obj.dupli_type != 'NONE':
            obj.dupli_list_create(context.scene)
            for dob in obj.dupli_list:
                obj_dupli = dob.object
                if obj_dupli.type == 'MESH':
                    listObjMatrix.append((obj_dupli, dob.matrix.copy()))

        obj.dupli_list_clear()

    return listObjMatrix


def copy_settings_clones(newObj, oldObj):
    # Copy Groups
    for thisGroup in bpy.data.groups:
        if oldObj.name in thisGroup.objects:
            thisGroup.objects.link(newObj)

    # Copy Modifiers
    for old_modifier in oldObj.modifiers.values():
            new_modifier = newObj.modifiers.new(name=old_modifier.name,
                                                type=old_modifier.type)

    # copy duplis
    if oldObj.dupli_group is not None:
        newObj.dupli_type = oldObj.dupli_type
        newObj.dupli_group = oldObj.dupli_group

    # copy custom settings of the old object
    for prop in oldObj.keys():
        newObj[prop] = oldObj[prop]


def get_obj_axis(obj, axis):
    ax = 0
    if axis == 'Y' or axis == '-Y':
        ax = 1
    if axis == 'Z' or axis == '-Z':
        ax = 2

    obj_matrix = obj.matrix_world
    axis_tuple = (
        obj_matrix[0][ax], obj_matrix[1][ax], obj_matrix[2][ax])
    axisResult = Vector(axis_tuple).normalized()

    if axis == '-X' or axis == '-Y' or axis == '-Z':
        axisResult.negate()

    return axisResult

###################################################################################################################
def mft_obj_ray_cast(obj, matrix, view_vector, ray_origin, ray_max=10000.0):
        """Wrapper for ray casting that moves the ray into object space"""

        # get the ray relative to the object
        matrix_inv = matrix.inverted()
        ray_target = ray_origin + (view_vector * ray_max)

        ray_origin_obj = matrix_inv * ray_origin
        ray_target_obj = matrix_inv * ray_target
        ray_direction_obj = ray_target_obj - ray_origin_obj

        # cast the ray
        hit_result, hit, normal, face_index = obj.ray_cast(ray_origin_obj, ray_direction_obj, ray_max)
        
        if hit_result:
            hit_world = matrix * hit

            length_squared = (hit_world - ray_origin).length_squared

            if face_index != -1:
                #normal_world = (matrix.to_quaternion() * normal).normalized()

                normal_world = (matrix.to_quaternion() * normal).to_4d()
                normal_world.w = 0
                normal_world = (matrix.to_quaternion() * (matrix_inv * normal_world).to_3d()).normalized()

                return normal_world, hit_world, length_squared

        return None, None, None


def mft_pick_and_clone(self, context, event, ray_max=10000.0):
    """Run this function on left mouse, execute the ray cast"""
    # get the context arguments
    scene = context.scene
    region = context.region
    rv3d = context.region_data
    coord = event.mouse_region_x, event.mouse_region_y

    # cast rays and find the closest object
    best_length_squared = ray_max * ray_max
    best_obj, best_obj_nor, best_obj_pos = None, None, None
    best_obj_rand, best_obj_nor_rand, best_obj_pos_rand = None, None, None
    best_obj_hit = None

    mifthCloneTools = bpy.context.scene.mifthCloneTools
    thePressure = max(1.0 - mifthCloneTools.drawPressure,
                      self.tabletPressure)  # The pressure of a pen!

    for obj, matrix in self.dupliList:
        # get the ray from the viewport and mouse
        view_vector_mouse = view3d_utils.region_2d_to_vector_3d(
            region, rv3d, coord)
        ray_origin_mouse = view3d_utils.region_2d_to_origin_3d(
            region, rv3d, coord)

        # Do RayCast! t1,t2,t3,t4 - temp values
        t1, t2, t3 = mft_obj_ray_cast(
            obj, matrix, view_vector_mouse, ray_origin_mouse)
        if t1 is not None and t3 < best_length_squared:
            best_obj = obj
            best_obj_nor, best_obj_pos, best_length_squared = t1, t2, t3
            best_obj_hit = t2

        # Check for stroke length
        if best_obj is not None:
            previousHit = None
            if len(self.currentStrokeList) > 0:
                previousHit = self.currentStrokeList[-1]  # get Last Element

            # Check for stroke
            strokeLength = mifthCloneTools.drawStrokeLength
            if mifthCloneTools.drawPressureScale is True and mifthCloneTools.drawPressureRelativeStroke is True and self.tabletPressure < 1.0 and mifthCloneTools.drawPressure > 0.0:
                strokeLength *= thePressure
            if previousHit is not None and (best_obj_pos - previousHit.hitPoint).length < strokeLength:
                best_obj = None  # Don't do cloning

    # random scatter things
    if mifthCloneTools.drawRandomStrokeScatter > 0.0 and best_obj is not None and t1 is not None:
        # Random Vec
        randX = random.uniform(
            -1.0, 1.0) * mifthCloneTools.drawRandomStrokeScatter  # 3.0 is random addition
        randY = random.uniform(
            -1.0, 1.0) * mifthCloneTools.drawRandomStrokeScatter  # 3.0 is random addition
        randZ = random.uniform(
            -1.0, 1.0) * mifthCloneTools.drawRandomStrokeScatter

        if mifthCloneTools.drawPressureScatter is True and self.tabletPressure < 1.0 and mifthCloneTools.drawPressure > 0.0:
            randX *= thePressure
            randY *= thePressure
            randZ *= thePressure

        randVect = Vector((randX, randY, randZ))

        for obj, matrix in self.dupliList:
            ray_origin_rand = best_obj_pos + randVect
            ray_origin_rand_2d = view3d_utils.location_3d_to_region_2d(
                region, rv3d, ray_origin_rand)
                
            # RanGE: Fix Crash mifthTools
            if (ray_origin_rand_2d == None):
                continue
                
            view_vector_rand = view3d_utils.region_2d_to_vector_3d(
                region, rv3d, (ray_origin_rand_2d.x, ray_origin_rand_2d.y))

            t1, t2, t3 = mft_obj_ray_cast(
                obj, matrix, view_vector_rand, ray_origin_rand)
            # 3.0 is random addition
            if t1 is not None and (t2 - best_obj_hit).length <= mifthCloneTools.drawRandomStrokeScatter * 3.0:
                best_obj_nor, best_obj_pos = t1, t2

    # now we have the object under the mouse cursor,
    if best_obj is not None:
        objToClone = bpy.data.objects.get(random.choice(drawForClonesObj))
        best_obj_nor = best_obj_nor.normalized()

        # clone object
        newDup = bpy.data.objects.new(objToClone.name, objToClone.data)

        # copy draw type
        newDup.draw_type = objToClone.draw_type
        newDup.show_wire = objToClone.show_wire

        # copy transformation
        newDup.matrix_world = objToClone.matrix_world
        newDup.location = best_obj_pos
        newDup.scale = objToClone.scale
        newDup.rotation_euler = objToClone.rotation_euler
        # bpy.ops.object.rotation_clear()

        context.scene.objects.link(newDup)
        newDup.select = True
        context.scene.objects.active = newDup

        # Rotation To Normal
        if mifthCloneTools.drawClonesNormalRotate is True:
            # rotate To Normal
            newDupZAxis = get_obj_axis(newDup, 'Z')
            angleRotate = newDupZAxis.angle(best_obj_nor)
            rotateAxis = newDupZAxis.cross(best_obj_nor).normalized()

            bpy.ops.transform.rotate(value=angleRotate, axis=(
                (rotateAxis.x, rotateAxis.y, rotateAxis.z)), proportional='DISABLED')

        # Change Axis
        if mifthCloneTools.drawClonesAxis == 'Y':
            bpy.ops.transform.rotate(value=math.radians(
                90), axis=get_obj_axis(newDup, 'X'), proportional='DISABLED')
        elif mifthCloneTools.drawClonesAxis == '-Y':
            bpy.ops.transform.rotate(value=math.radians(
                -90), axis=get_obj_axis(newDup, 'X'), proportional='DISABLED')
            bpy.ops.transform.rotate(value=math.radians(
                180), axis=get_obj_axis(newDup, 'Y'), proportional='DISABLED')
        elif mifthCloneTools.drawClonesAxis == '-Z':
            bpy.ops.transform.rotate(
                value=math.radians(180), axis=get_obj_axis(newDup, 'X'), proportional='DISABLED')
        elif mifthCloneTools.drawClonesAxis == 'X':
            bpy.ops.transform.rotate(
                value=math.radians(-90), axis=get_obj_axis(newDup, 'Y'), proportional='DISABLED')
        elif mifthCloneTools.drawClonesAxis == '-X':
            bpy.ops.transform.rotate(value=math.radians(
                90), axis=get_obj_axis(newDup, 'Y'), proportional='DISABLED')

        # Other rotate
        if mifthCloneTools.drawClonesRadialRotate is True or mifthCloneTools.drawClonesDirectionRotate is True:

            # Ratate to Direction
            newDirRotLookAtt = None
            if mifthCloneTools.drawClonesDirectionRotate is True:
                previousHit = None
                if len(self.currentStrokeList) > 0:
                    previousHit = self.currentStrokeList[
                        -1]  # get Last Element
                else:
                    if len(self.allStrokesList) > 0:
                        previousHit = self.allStrokesList[-1][
                            -1]  # get Last Element of previous Stroke

                if previousHit is not None:
                    newDirRotLookAtt = (
                        best_obj_hit - previousHit.hitPoint).normalized()
            else:
                newDirRotLookAtt = Vector((0.0, 0.0, 1.0))

            # Get the axis to rotate
            if newDirRotLookAtt is not None:
                tempYCross = best_obj_nor.cross(newDirRotLookAtt).normalized()
                if tempYCross != Vector((0.0, 0.0, 0.0)):
                    tempYCross.negate()
                    radialVec = best_obj_nor.cross(tempYCross).normalized()

                    axisPickTemp = 'Y'
                    if mifthCloneTools.drawClonesAxis == 'Y':
                        axisPickTemp = 'Z'
                    if mifthCloneTools.drawClonesAxis == '-Y':
                        axisPickTemp = 'Z'
                    if mifthCloneTools.drawClonesAxis == '-Z':
                        axisPickTemp = 'Y'
                    if mifthCloneTools.drawClonesAxis == 'X':
                        axisPickTemp = 'Z'
                    if mifthCloneTools.drawClonesAxis == '-X':
                        axisPickTemp = 'Z'

                    tempY = get_obj_axis(newDup, axisPickTemp)
                    xyAngleRotate = Vector(radialVec).angle(tempY)

                    if tempYCross.angle(tempY) > math.radians(90.0):
                        xyAngleRotate = -xyAngleRotate

                    bpy.ops.transform.rotate(
                        value=xyAngleRotate, axis=best_obj_nor, proportional='DISABLED')

                # newDupMatrix2 = newDup.matrix_world
                # newDupZAxisTuple2 = (
                    # newDupMatrix2[0][2], newDupMatrix2[1][2], newDupMatrix2[2][2])
                # newDupZAxis2 = (
                    # Vector(newDupZAxisTuple2)).normalized()
                # newDirRotVec2 = (newDirRotLookAtt.cross(best_obj_nor)).normalized().cross(
                    # best_obj_nor).normalized()
                # newDirRotAngle = newDirRotVec2.angle(newDupZAxis2)
                # fixDirRotAngle = newDirRotLookAtt.cross(
                    # best_obj_nor).angle(newDupZAxis2)
                # if fixDirRotAngle < math.radians(90.0):
                    # newDirRotAngle = - \
                        # newDirRotAngle  # As we do it in negative axis
                # Main rotation
                # bpy.ops.transform.rotate(value=newDirRotAngle, axis=(
                    #(best_obj_nor.x, best_obj_nor.y, best_obj_nor.z)), proportional='DISABLED')
        # set PreviousClone position
        # self.prevClonePos = best_obj_hit
        # Random rotation along Picked Normal
        if mifthCloneTools.randNormalRotateClone > 0.0:
            randNorAngle = random.uniform(
                math.radians(-mifthCloneTools.randNormalRotateClone), math.radians(mifthCloneTools.randNormalRotateClone))
            randNorAxis = (best_obj_nor.x, best_obj_nor.y, best_obj_nor.z)
            if mifthCloneTools.drawClonesRadialRotate is False and mifthCloneTools.drawClonesNormalRotate is False:
                randNorAxis = (0.0, 0.0, 1.0)
            bpy.ops.transform.rotate(
                value=randNorAngle, axis=(randNorAxis), proportional='DISABLED')

        # Random rotation along Picked Normal
        if mifthCloneTools.randDirectionRotateClone > 0.0:
            randDirX, randDirY, randDirZ = random.uniform(
                0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)
            randDirVec = (
                Vector((randDirX, randDirY, randDirZ))).normalized()
            randDirAngle = random.uniform(
                math.radians(-mifthCloneTools.randDirectionRotateClone), math.radians(mifthCloneTools.randDirectionRotateClone))
            bpy.ops.transform.rotate(
                value=randDirAngle, axis=(randDirVec), proportional='DISABLED')

        # change Size
        if mifthCloneTools.drawPressure > 0.0 or mifthCloneTools.randScaleClone > 0.0:
            newSize = newDup.scale
            if self.tabletPressure < 1.0 and mifthCloneTools.drawPressure > 0.0 and mifthCloneTools.drawPressureScale is True:
                newSize *= thePressure

            if mifthCloneTools.randScaleClone > 0.0:
                randScaleClone = 1.0 - \
                    (random.uniform(0.0, 0.99) *
                     mifthCloneTools.randScaleClone)
                newSize *= randScaleClone

        # Add this point with all its stuff
        self.currentStrokeList.append(
            MTFDCPoint(newDup, objToClone, best_obj_hit, best_obj_nor))

        # do optimization for a stroke or not
        if mifthCloneTools.drawClonesOptimize is False:
            copy_settings_clones(newDup, objToClone)

        newDup.select = False  # Clear Selection
###############################################################################################################################

class MFTCloneToSelected(bpy.types.Operator):
    bl_idname = "mft.clonetoselected"
    bl_label = "Clone To Selected"
    bl_description = "Clone To Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if len(bpy.context.selected_objects) > 1:
            objToClone = bpy.context.scene.objects.active
            objectsToClone = []

            for obj in bpy.context.selected_objects:
                if obj != objToClone:
                    objectsToClone.append(obj.name)

            for name in objectsToClone:
                obj = context.scene.objects[name]
                bpy.ops.object.select_all(action='DESELECT')
                objToClone.select = True

                bpy.ops.object.duplicate(linked=True, mode='DUMMY')
                newDup = bpy.context.selected_objects[0]
                # print(newDup)
                newDup.location = obj.location
                newDup.rotation_euler = obj.rotation_euler
                newDup.scale = obj.scale

            bpy.ops.object.select_all(action='DESELECT')
            for name in objectsToClone:
                context.scene.objects[name].select = True
            bpy.ops.object.delete(use_global=False)

            objectsToClone = None
        else:
            self.report({'INFO'}, "Need more Objects!")

        return {'FINISHED'}


class MFTRadialClone(bpy.types.Operator):
    bl_idname = "mft.radialclone"
    bl_label = "Radial Clone"
    bl_description = "Radial Clone"
    bl_options = {'REGISTER', 'UNDO'}

    create_last_clone: BoolProperty(
        name="Create Last Clone",
        description="create last clone...",
        default=False
    )

    radialClonesAngle: FloatProperty(
        default=360.0,
        min=-360.0,
        max=360.0
    )
    clonez: IntProperty(
        default=8,
        min=2,
        max=300
    )

    def execute(self, context):

        if len(bpy.context.selected_objects) > 0:
            activeObj = bpy.context.scene.objects.active
            selObjects = bpy.context.selected_objects
            mifthCloneTools = bpy.context.scene.mifthCloneTools
            # self.clonez = mifthCloneTools.radialClonesNumber

            activeObjMatrix = activeObj.matrix_world

            clones_count = self.clonez
            if self.create_last_clone is False:
                clones_count = self.clonez - 1

            for i in range(clones_count):
                bpy.ops.object.duplicate(linked=True, mode='DUMMY')
                # newObj = bpy.context.selected_objects[0]
                # print(newObj)
                # for obj in bpy.context.selected_objects:
                theAxis = None

                if mifthCloneTools.radialClonesAxis == 'X':
                    if mifthCloneTools.radialClonesAxisType == 'Local':
                        theAxis = (
                            activeObjMatrix[0][0], activeObjMatrix[1][0], activeObjMatrix[2][0])
                    else:
                        theAxis = (1, 0, 0)

                elif mifthCloneTools.radialClonesAxis == 'Y':
                    if mifthCloneTools.radialClonesAxisType == 'Local':
                        theAxis = (
                            activeObjMatrix[0][1], activeObjMatrix[1][1], activeObjMatrix[2][1])
                    else:
                        theAxis = (0, 1, 0)

                elif mifthCloneTools.radialClonesAxis == 'Z':
                    if mifthCloneTools.radialClonesAxisType == 'Local':
                        theAxis = (
                            activeObjMatrix[0][2], activeObjMatrix[1][2], activeObjMatrix[2][2])
                    else:
                        theAxis = (0, 0, 1)

                rotateValue = (
                    math.radians(self.radialClonesAngle) / float(self.clonez))
                bpy.ops.transform.rotate(value=rotateValue, axis=theAxis)

            bpy.ops.object.select_all(action='DESELECT')

            for obj in selObjects:
                obj.select = True
            selObjects = None
            bpy.context.scene.objects.active = activeObj
        else:
            self.report({'INFO'}, "Select Objects!")

        return {'FINISHED'}


class MFTGroupInstance(bpy.types.Operator):
    bl_idname = "mft.group_instance_to_cursor"
    bl_label = "Set GroupInstance to Cursor"
    bl_description = "Set GroupInstance to Cursor..."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = bpy.context.scene
        mifthCloneTools = scene.mifthCloneTools

        obj_group = bpy.data.groups.get(mifthCloneTools.getGroupsLst)
        if obj_group is not None:
            obj_group.dupli_offset[
                0] = bpy.context.space_data.cursor_location[0]
            obj_group.dupli_offset[
                1] = bpy.context.space_data.cursor_location[1]
            obj_group.dupli_offset[
                2] = bpy.context.space_data.cursor_location[2]

        return {'FINISHED'}


class MFTGroupToMesh(bpy.types.Operator):
    bl_idname = "mft.group_to_mesh"
    bl_label = "Convert Group Instance to Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.duplicates_make_real()
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, texture=False, animation=False)
        
        objs = context.selected_objects
        objs_names = [i.name for i in objs]

        for name in objs_names:
            obj = context.scene.objects[name]

            if obj.type == 'EMPTY':
                bpy.data.objects.remove(bpy.data.objects[name], True)

            elif obj.type == 'MESH':
                if obj.scale[0] < 0 or obj.scale[1] < 0 or obj.scale[2] < 0:
                    for face in obj.data.polygons:
                        face.select = True

                    context.scene.objects.active = obj
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bpy.ops.mesh.flip_normals()
                    bpy.ops.object.mode_set(mode = 'OBJECT')

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)


        return {'FINISHED'}
