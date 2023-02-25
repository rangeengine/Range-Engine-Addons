import bpy


def set_scripts_dir():

    game_file_path = bpy.data.filepath
    game_scripts_path = game_file_path.rpartition("\\")[0]

    return game_scripts_path
