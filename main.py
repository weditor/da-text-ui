# -*- encoding: utf-8 -*-

from typing import Callable
import PySimpleGUI as sg
import string_action

# sg.theme('DarkAmber')   # Add a touch of color
# sg.theme('DefaultNoMoreNagging')   # Add a touch of color
sg.theme('GrayGrayGray')   # Add a touch of color
# All the stuff inside your window.

# 測試: 想著要出一本著作
inputText = sg.Multiline(size=(100, 15), expand_x=True)
outputText = sg.Multiline(size=(100, 15), expand_x=True, disabled=True)
btn_size = (10, 2)
left_layout = [
    [inputText],
    [outputText],
]
right_layout = [
    # [sg.Button("二次处理", size=(btn_size[0]*2+2, btn_size[1]), key="to_becontinued", font="楷体 16"), ],
    [sg.Button("二次处理", size=(btn_size[0]*2+2, btn_size[1]), key="to_becontinued",) ],
    [sg.Button("繁转简", size=btn_size, key="to_simp"), sg.Button("简转繁", size=btn_size, key="to_trad"),],
    [sg.Button("转半角", size=btn_size, key="to_halfwidth"), sg.Button("转全角", size=btn_size, key="to_fullwidth"),],
    [sg.Button("转小写", size=btn_size, key="to_lower"), sg.Button("转大写", size=btn_size, key="to_upper"),],
    [sg.Button("取拼音", size=btn_size, key="to_py"), sg.Button("取首拼", size=btn_size, key="to_py_head"),],
    [sg.Button("去空格", size=btn_size, key="replace_blank"), sg.Button("去换行", size=btn_size, key="replace_nl"),],
    [sg.Button("十转10", size=(btn_size[0]*2+2, btn_size[1]), key="ten_to_10", disabled=True), ],
    [sg.Button("去重", size=btn_size, key="to_uniq", disabled=True), sg.Button("取名称", size=btn_size, key="get_name", disabled=True), ],
    [sg.Button("帮助?", size=btn_size, key="_help"), ],
]

head_btns = [
    sg.Button("取代码", disabled=True, size=btn_size, key="get_code"), 
    sg.Button("排版", disabled=True, size=btn_size, key="restructure"),
    sg.Button("清空", size=btn_size, key="clear_text"),
    sg.Button("替换", disabled=True, size=btn_size, key="restructure"),
]
layout = [
    [sg.Column([head_btns], expand_x=True)],
    [sg.Column(left_layout, expand_x=True, expand_y=True), sg.VerticalSeparator(), sg.Column(right_layout, expand_y=True)]
]

def process_text(func: Callable[[str], str]):
    def _inner_func():
        text = inputText.get()
        outputText.update(func(text))
    return _inner_func

def _to_becontinued():
    text = outputText.get()
    inputText.update(text)

def _clear_text():
    outputText.update("")
    inputText.update("")

def _help():
    text = """
程序介绍: 数据部文本处理程序
源码: (待补充)

说明:
1. 优化生僻字显示为 □ 的问题
2. (一定程度上)优化拼音多音字问题, 比如 "了解了" => "liao jie le"
3. 优化简繁转换对应错误的问题, 比如 "想著一本著作" => "想着一本著作"

如果使用过程中遇到问题或者有改进意见，请联系 aochujie@myhexin.com 。
欢迎邮件或vanish轰炸。

    """
    help_wd = sg.Window("关于", layout=[[sg.Text(text)]], keep_on_top=True, modal=True)
    event, value = help_wd.read(close=True)
    help_wd.close()
    # sg.popup("fuck")


wd_events = [
    ["to_becontinued", _to_becontinued],
    ["clear_text", _clear_text],
    ["to_simp", process_text(string_action.to_simplify)],
    ["to_trad", process_text(string_action.to_traditional)],
    ["to_upper", process_text(string_action.to_upper)],
    ["to_lower", process_text(string_action.to_lower)],
    ["to_py", process_text(string_action.to_pinyin)],
    ["to_py_head", process_text(string_action.to_pinyin_head)],
    ["replace_blank", process_text(string_action.replace_blank)],
    ["replace_nl", process_text(string_action.replace_nl)],
    ["to_halfwidth", process_text(string_action.str_q2b)],
    ["to_fullwidth", process_text(string_action.str_b2q)],
    ["_help", _help],
]

def find_event(ev: str):
    for item in wd_events:
        if item[0] == ev:
            return item
    return None

window = sg.Window('文本处理程序', layout, resizable=True)
def main():
    # Create the Window
    
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        item = find_event(event)
        if not item:
            print('You entered ', event, values[0])
            continue
        _, func = item
        func()

    window.close()

main()
