from bpy.app import version


def draw_game_properties(self, context, layout):
    layout = layout.column(align=True)

    ob = context.active_object
    game = ob.game
    is_font = (ob.type == 'FONT')

    if is_font:
        prop_index, prop_indexR = game.properties.find(
            "Text"), game.properties.find("Text-Res")

        if prop_index != -1:
            layout.operator("object.game_property_remove",
                            text="Remove Text Game Property", icon='X').index = prop_index
            row = layout.row()
            sub = row.row()
            sub.enabled = 0
            prop = game.properties[prop_index]
            sub.prop(prop, "name", text="", icon="FONT_DATA")
            row.prop(prop, "type", text="")
            row.label("See Text Object")

            if prop_indexR != -1:
                sub = row.row(align=True)
                sub.operator("object.game_property_remove",
                             text="", icon='X').index = prop_indexR
                row = layout.row()
                sub = row.row()
                sub.enabled = 0
                prop = game.properties[prop_indexR]
                sub.prop(prop, "name", text="", icon="FONT_DATA")
                row.prop(prop, "value", text="Resolution")
                row.label("Text Resolution(0-50)")
            else:
                sub = row.row(align=True)
                propsR = sub.operator(
                    "object.game_property_new", text="", icon=[
                        "ADD", "ZOOMIN"][version == (2, 79, 7)],)
                propsR.name = "Text-Res"
                propsR.type = 'FLOAT'
        else:
            props = layout.operator(
                "object.game_property_new", text="Add Text Game Property", icon=[
                    "ADD", "ZOOMIN"][version == (2, 79, 7)])
            props.name = "Text"
            props.type = 'STRING'

    props = layout.operator("object.game_property_new",
                            text="Add Game Property", icon=[
                                "ADD", "ZOOMIN"][version == (2, 79, 7)])
    props.name = ""

    for i, prop in enumerate(game.properties):
        if is_font and i == prop_index or is_font and i == prop_indexR:
            continue

        box = layout.box()
        row = box.row()
        row.prop(prop, "name", text="")
        row.prop(prop, "type", text="")
        row.prop(prop, "value", text="")
        row.prop(prop, "show_debug", text="", toggle=True, icon='INFO')
        sub = row.row(align=True)
        props = sub.operator("object.game_property_move",
                             text="", icon='TRIA_UP')
        props.index = i
        props.direction = 'UP'
        props = sub.operator("object.game_property_move",
                             text="", icon='TRIA_DOWN')
        props.index = i
        props.direction = 'DOWN'
        row.operator("object.game_property_remove", text="",
                     icon='X', emboss=False).index = i
