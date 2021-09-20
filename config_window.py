# -*- coding: utf-8 -*-

import PySimpleGUI as sg
from edit_btn_window import open_edit_window
import configure

def _create_window():

    head = [sg.Text("名称", size=(10, 1)), sg.Text("描述", size=(20, 1)), sg.Text("快捷键", size=(8, 1)), sg.Text("显示", size=(6, 1)), sg.Text("启用", size=(6, 1)), sg.Text("操作", size=(10, 1))]
    tbody = [
        [
            sg.InputText(btn.name, disabled=True, size=(10, 1)), 
            sg.InputText(btn.description, disabled=True, size=(20, 1)), 
            sg.InputText(btn.hotkey, disabled=True, size=(8, 1)), 
            sg.Checkbox("", btn.visible, disabled=True, size=(4, 1)), 
            sg.Checkbox("", btn.enable, disabled=True, size=(4, 1)),
            sg.Button("编辑", key=f"edit-{idx}"),
            sg.Button("删除", key=f"del-{idx}"),
        ]
        for idx, btn in enumerate(configure.config.buttons)
    ]
    layout = [
        [sg.Button("增加", key="add_btn")],
        [head],
        *tbody,
    ]
    window = sg.Window("配置", layout, force_toplevel=True, modal=True, icon="resources/images/txt_icon.ico")
    return window

def open_config_window():
    window = _create_window()
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        if event == "add_btn":
            window.close()
            is_ok, value = open_edit_window(configure.BtnConfig(name=""))
            if not is_ok:
                continue
            configure.config.buttons.append(value)
            configure.config.save()
            window = _create_window()
        elif event.startswith("edit-"):
            window.close()
            idx = int(event.split("-")[1])
            is_ok, value = open_edit_window(configure.config.buttons[idx])
            if not is_ok:
                continue
            configure.config.buttons[idx] = value
            configure.config.save()
            window = _create_window()
        elif event.startswith("del-"):
            window.close()
            idx = int(event.split("-")[1])
            del configure.config.buttons[idx]
            configure.config.save()
            window = _create_window()
