# -*- encoding -*-

from configure import BtnConfig
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import VerticalSeparator


def open_edit_window(default: BtnConfig):
    # actions = []
    left_layout = [
        [sg.Text("基础信息")],
        [sg.Text("名称", size=(7, 1)), sg.InputText(default.name, key="name")],
        [sg.Text("描述", size=(7, 1)), sg.InputText(default.description, key="description")],
        [sg.Text("快捷键", size=(7, 1)), sg.InputText(default.hotkey, key="hotkey")],
        [sg.Text("是否展示"), sg.Checkbox("", default=default.visible, key="visible")],
        [sg.Text("是否启用"), sg.Checkbox("", default=default.enable, key="enable")],
    ]
    default_action = default.actions or "转半角\n繁转简\n转小写\n去空格"
    action_layout = sg.Column([
        [sg.Text("动作列表")], 
        [sg.Multiline(default_action, expand_y=True, key="actions")],
        [sg.Text("直接填写需要执行的操作，每行一个，如繁转简\n多个操作之间会自动使用 ‘二次处理’ ，不必手动调用")],
    ], expand_y=True, key="action_layout")
    # right_layout = [
    #     [sg.Text("可用动作列表")],
    #     [sg.Button("繁转简", key="act-to_simp"), sg.Button("简转繁", key="act-to_trad")],
    #     [sg.Button("转半角", key="act-to_halfwidth"), sg.Button("转全角", key="act-to_fullwidth")],
    #     [sg.Button("转小写", key="act-to_lower"), sg.Button("转大写", key="act-to_upper")],
    #     [sg.Button("取拼音", key="act-to_py"), sg.Button("取首拼", key="act-to_py_head")],
    #     [sg.Button("去空格", key="act-replace_blank"), sg.Button("去换行", key="act-replace_nl")],
    # ]
    layout = [
        [
            sg.Column(left_layout, expand_y=True), 
            sg.VerticalSeparator(), 
            action_layout,
        ],
        [sg.OK("确定"), sg.Cancel("取消")]
    ]
    window = sg.Window("配置", layout, force_toplevel=True, modal=True, icon="resources/images/txt_icon.ico")
    event, values = window.read(close=True)
    if event=="确定":
        return True, BtnConfig(**values)
    else:
        return False, None
