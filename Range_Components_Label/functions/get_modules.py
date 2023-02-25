import os
from re import findall
from ..var_globals import regex_multiline
import bpy

def get_modules(scripts_path):
    dict_modules = {}
    for root, dirs, files in os.walk(top=f"{scripts_path}\\scripts"):
        root_split = root.split("\\")[-1]

        if root_split != "__pycache__":
            module = root_split
            if module not in dict_modules and module != scripts_path.split("\\")[-1]:
                dict_modules[module] = {}

            for file in files:
                path_file = os.path.join(root, file)

                with open(path_file) as open_file:

                    if str(object=file).endswith((".py")):
                        content = open_file.read()
                        all_classes = findall(
                            pattern=regex_multiline, string=content)

                        for cls in all_classes:
                            name_class = cls[0]

                            path_class = path_file.replace(scripts_path, "").replace(
                                "\\", ".").replace(".py", "").replace(".", "", 1)
                            path_class = f"{path_class}.{name_class}"
                            dict_modules[module].update({
                                name_class: path_class
                            })
                    open_file.close

    return dict_modules

# in .Range Files # obj.name = FileName
def get_modules_in_range(scene):
    dict_modules = {"In .Range File" : {}}
    
    for obj in bpy.data.texts:
        if obj.name[-3:] == ".py":
            strTxt = obj.as_string() # File Container
            if "types.KX_PythonComponent" in strTxt:
                for line in strTxt.split("\n"):
                    if "types.KX_PythonComponent" in line:
                        nm = line.replace("class", "").replace(" ","").split("(")[0]
                        
                        dict_modules["In .Range File"].update({
                            nm: obj.name[:-3] + "." + nm
                        })
                        
    return dict_modules
