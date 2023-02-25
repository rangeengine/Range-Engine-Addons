from bpy.types import UIList


class FLOWMENU_UL_sensors(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        self.use_filter_show = False

        collection = data.collection_sensors
        collection_active = active_data.collection_sensors_active

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            name = layout.column(align=True)
            name.label(text=f"{item.value}")

        elif self.layout_type in {'GRID'}:
            name = layout.row(align=True)
            name.label(text=f"{item.value}")
