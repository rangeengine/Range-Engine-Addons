regex_multiline = r"[ ]*?[class]+\s([\w]*)\s*?\([A-Za-z0-9_,.=:\"\' ]*(KX_PythonComponent)[A-Za-z0-9_,.:=\"\' ]*\)[\w\W]+?"

template_component = """
from bge import *
from collections import OrderedDict

class %s(types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict({
    
    })

    def start(self, args):
        # Put your initialization code here, args stores the values from the UI.
        # self.object is the owner object of this component.
        self.scene = logic.getCurrentScene() # CurrentScene(Scene)
        self.keyboard = logic.keyboard.inputs # Keyboard Inputs
        self.mouse = logic.mouse.inputs # Mouse Inputs
        

    def update(self):
        # Put your code executed every logic step here.
        # self.object is the owner object of this component.
        pass
    
"""