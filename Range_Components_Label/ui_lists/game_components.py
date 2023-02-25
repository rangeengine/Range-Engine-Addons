from bpy.types import UIList


class FLOWMENU_UL_game_components(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        self.use_filter_show = False

        collection = data.collection_components
        collection_active = active_data.collection_components_active

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            name = layout.row(align=True)
            name.label(text=f"{item.value}")

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)
