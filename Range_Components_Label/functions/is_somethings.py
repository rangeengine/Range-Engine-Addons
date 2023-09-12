import bpy


def is_file_saved():
    return bpy.data.is_saved


def is_bge_version():
    if bpy.app.version == (2, 79, 7):
        return True
