from bpy.types import UIList


class FLOWMENU_UL_modules_components(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        self.use_filter_show = False
        
        '''
        script = item.name.split(".")[0]+".py"
        print(item.name)
        classNm = item.name.split(".")[1]
        
        #layout.label(text=item.name, translate=False, icon="GAME")
        layout.label(text=classNm, translate=False, icon="GAME")
        layout.label(text=script, translate=False, icon="TEXT")
        '''

        collection = data.collection_modules
        collection_active = active_data.collection_modules_active

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            name = layout.row(align=True)
            name.label(text=f"{item.value}")

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)
