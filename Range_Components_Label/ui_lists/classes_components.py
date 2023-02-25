from bpy.types import UIList


class FLOWMENU_UL_classes_components(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        self.use_filter_show = False

        collection = data.collection_classes
        collection_active = active_data.collection_classes_active

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            name = layout.row(align=True)
            name.label(text=item.value)
            button = layout.row(align=True)

            if collection_active >= len(collection):
                active_data.collection_classes_active = 0

            try:
                if item.value == collection[collection_active].value:
                    button.operator("wm.flowmenu_ot_register_component",
                                    text="Register", icon="FILE_SCRIPT")

            except:
                pass

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)
