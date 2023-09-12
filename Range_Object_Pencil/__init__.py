# BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# END GPL LICENSE BLOCK #####

bl_info = {
    "name": "RanGE: Object Pencil",
    "author": "Paul Geraskin, Range Engine",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "3D Viewport",
    "description": "Paints the terrain with objects",
    "warning": "Only for Range Engine 1.4+",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Game Engine Tools"}


if "bpy" in locals():
    import imp
    imp.reload(range_tools_cloning)
    imp.reload(range_tools)
    #imp.reload(mifth_vertex_paint)
else:
    from . import range_tools_cloning
    from . import range_tools
    #from . import vertex_paint

import bpy
from bpy.props import *


# registration
def menu_vertex_paint_func(self, context):
    self.layout.separator()
    self.layout.menu(mifth_vertex_paint.MFTVertexPaintMenu.bl_idname)
    
class MFTProperties(bpy.types.PropertyGroup):

        # Output Settings
        outputFolder: StringProperty(
            name="outputFolder",
            subtype="NONE",
            default="seq"
        )

        outputSubFolder: StringProperty(
            name="outputSubFolder",
            subtype="NONE",
            default="ren"
        )

        outputSequence: StringProperty(
            name="outputSequence",
            subtype="NONE",
            default="render"
        )

        outputSequenceSize: IntProperty(
            default=8,
            min=1,
            max=60
        )

        doOutputSubFolder: BoolProperty(
            name="do Output SubFolder",
            description="do Output SubFolder...",
            default=False
        )

        # Curve Animator Settings
        doUseSceneFrames: BoolProperty(
            name="do use scene frames",
            description="do use scene frames...",
            default=False
        )

        curveAniStartFrame: IntProperty(
            default=1,
            min=1,
            max=10000
        )

        curveAniEndFrame: IntProperty(
            default=100,
            min=1,
            max=10000
        )

        curveAniStepFrame: IntProperty(
            default=10,
            min=1,
            max=10000
        )

        curveAniInterpolation: FloatProperty(
            default=0.3,
            min=0.0,
            max=1.0
        )

        # MorfCreator settings
        morfCreatorNames: StringProperty(
            name="MorfNames",
            subtype="NONE",
            default=""
        )

        morfUseWorldMatrix: BoolProperty(
            name="use world matrix",
            description="use world matrix...",
            default=False
        )

        morfApplyModifiers: BoolProperty(
            name="apply modifiers to morf",
            description="apply modifiers to morf...",
            default=False
        )

classes = [
MFTProperties,
range_tools_cloning.MFTCloneProperties,
range_tools_cloning.MFTPanelCloning,
range_tools_cloning.MFTDrawClones,
range_tools_cloning.MFTPickObjToDrawClone,
range_tools_cloning.MFTCloneToSelected,
range_tools_cloning.MFTRadialClone,
range_tools_cloning.MFTGroupInstance,
range_tools_cloning.MFTGroupToMesh
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    #bpy.types.VIEW3D_MT_paint_vertex.append(menu_vertex_paint_func)
    
    bpy.types.Scene.mifthTools = PointerProperty(
        name="Range Tools Variables",
        type=MFTProperties,
        description="Range Tools Properties"
    )

    bpy.types.Scene.mifthCloneTools = PointerProperty(
        name="Range Cloning Variables",
        type=range_tools_cloning.MFTCloneProperties,
        description="Range Cloning Properties"
    )


def unregister():
    import bpy
    for cls in classes:
        bpy.utils.unregister_class(cls)

    #bpy.types.VIEW3D_MT_object_specials.remove(menu_vertex_paint_func)

    del bpy.types.Scene.mifthTools
    del bpy.types.Scene.mifthCloneTools
    # del bpy.mifthTools
    # del bpy.mifthCloneTools


if __name__ == "__main__":
    register()
