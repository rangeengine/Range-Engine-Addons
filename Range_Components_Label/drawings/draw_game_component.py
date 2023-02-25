def draw_game_component(self, context, layout):
    layout = layout.box()

    ob = context.active_object
    game = ob.game

    st = context.space_data
    scene = context.scene
    wm = context.window_manager

    component_active = wm.collection_components_active

    try:
        component = game.components[component_active]

        box = layout.box()
        row = box.row(align=True)
        row.alignment = "CENTER"

        row.operator("wm.flowmenu_python_component_reload_new",
                     text="Reload", icon="RECOVER_LAST")
        row.operator("logic.python_component_remove",
                     text="Remove", icon="X").index = component_active
        lastHeader = None

        box = box.column()
        if len(component.properties) == 0:
            message = box.column()
            message.box().label(text="No args in component!", icon="INFO")
        else:
            iconval = 1
            for prop in component.properties:
                row = box.row()
                if prop.name[:8] == "C_Header":
                    row = row.box()
                    icon = "FULLSCREEN"
                    split = prop.name.split("/")
                    if len(split) > 1:
                        icon = split[1]

                    row.label(text=prop.value, icon=icon)
                    lastHeader = row.column()
                    continue

                if prop.name == "C_Icons":
                    if type(prop.value) != type(str()):
                        pass
                    continue
                text = prop.name
                if lastHeader:
                    row = lastHeader.row()
                    text = "- {}".format(text)

                try:
                    if "C_Icons" in component.properties:
                        row.box().label(text=text, icon=icondict[iconval])
                        iconval += 1
                        col = row.column().box()
                        col.prop(prop, "value", text="")
                    else:
                        row.box().label(text=text)
                        col = row.column().box()
                        col.prop(prop, "value", text="")
                except:
                    row.box().label(text=text)
                    col = row.column().box()
                    col.prop(prop, "value", text="")
    except:
        pass
