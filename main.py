# -*- encoding: utf-8 -*-

from config_window import open_config_window
from help_window import open_help_window
from typing import Callable, NamedTuple
import PySimpleGUI as sg
import string_action
import configure


sg.set_options(font="幼圆 15")
# sg.theme('DarkAmber')   # Add a touch of color
# sg.theme('DefaultNoMoreNagging')   # Add a touch of color

sg.theme('GrayGrayGray')   # Add a touch of color
# All the stuff inside your window.


def _chunk(_iter, n):
    rets = []
    for item in _iter:
        rets.append(item)
        if len(rets) >= n:
            yield rets
            rets = []
    if rets:
        yield rets
        rets = []


class TxtActInfo(NamedTuple):
    key: str
    label: str
    func: Callable[[str], str]


text_act_infos = [
    TxtActInfo("to_simp", "繁转简", string_action.to_simplify),
    TxtActInfo("to_trad", "简转繁", string_action.to_traditional),
    TxtActInfo("to_lower", "转小写", string_action.to_lower),
    TxtActInfo("to_upper", "转大写", string_action.to_upper),
    TxtActInfo("to_py", "取拼音", string_action.to_pinyin),
    TxtActInfo("to_py_head", "取首拼", string_action.to_pinyin_head),
    TxtActInfo("replace_blank", "去空格", string_action.replace_blank),
    TxtActInfo("replace_nl", "去换行", string_action.replace_nl),
    TxtActInfo("to_halfwidth", "转半角", string_action.str_q2b),
    TxtActInfo("to_fullwidth", "转全角", string_action.str_b2q),
]


class MainWindow:
    inputText: sg.Multiline
    outputText: sg.Multiline
    def __init__(self) -> None:
        self._btn_size = (10, 2)
        self._wd_events = [
            ["to_becontinued", self._to_becontinued],
            ["clear_text", self._clear_text],
            ["_help_wnd", open_help_window],
            *[[info.key, self.process_text(info.func)] for info in text_act_infos]
        ]

    def _gen_btn(self, label: str, size=None):
        btn_size = size or self._btn_size
        info = [_info for _info in text_act_infos if _info.label == label][0]
        return sg.Button(info.label, size=btn_size, key=info.key)
    
    def _create_window(self):
        # 測試: 想著要出一本著作
        self.inputText = sg.Multiline(size=(80, 13), expand_x=True)
        self.outputText = sg.Multiline(size=(80, 13), expand_x=True, disabled=True)

        btn_size = self._btn_size
        left_layout = [
            [self.inputText],
            [self.outputText],
        ]
        right_layout = [
            [sg.Button("二次处理", size=(btn_size[0]*2+2, btn_size[1]), key="to_becontinued",) ],
            [self._gen_btn("繁转简"), self._gen_btn("简转繁"),],
            [self._gen_btn("转半角"), self._gen_btn("转全角"),],
            [self._gen_btn("转小写"), self._gen_btn("转大写"),],
            [self._gen_btn("取拼音"), self._gen_btn("取首拼"),],
            [self._gen_btn("去空格"), self._gen_btn("去换行"),],
            [sg.Button("十转10", size=(btn_size[0]*2+2, btn_size[1]), key="ten_to_10", disabled=True), ],
            [sg.Button("去重", size=btn_size, key="to_uniq", disabled=True), sg.Button("取名称", size=btn_size, key="get_name", disabled=True), ],
            [sg.Button("帮助?", size=btn_size, key="_help_wnd")],
        ]

        head_btns = [
            sg.Button("取代码", disabled=True, size=btn_size, key="get_code"), 
            sg.Button("排版", disabled=True, size=btn_size, key="restructure"),
            sg.Button("清空", size=btn_size, key="clear_text"),
            sg.Button("替换", disabled=True, size=btn_size, key="restructure"),
        ]
        custom_btns = [
            sg.Button(btn.name, size=btn_size, key=f"custom-{idx}", tooltip=f"{btn.name}\n{btn.description}") 
            for idx, btn in enumerate(configure.config.buttons)
            if btn.visible and btn.enable
        ]

        custom_btns_layout = [
            *_chunk(custom_btns+[sg.Button("配置", button_color="#54b4eb", size=btn_size, key="_conf_wnd")], 8),
        ]
        layout = [
            [sg.Column([head_btns], expand_x=True)],
            [sg.Column(left_layout, expand_x=True, justification="left"), sg.VerticalSeparator(), sg.Column(right_layout, expand_y=True, justification="right")],
            [sg.Column(custom_btns_layout, expand_x=True)],
        ]
        window = sg.Window('文本处理程序', layout, resizable=True, icon="resources/images/txt_icon.ico", finalize=True)
        window.bind
        return window

    def process_text(self, func: Callable[[str], str]):
        def _inner_func():
            text = self.inputText.get()
            self.outputText.update(func(text))
        return _inner_func

    def _to_becontinued(self, ):
        text = self.outputText.get()
        self.inputText.update(text)
        self.outputText.update("")

    def _clear_text(self, ):
        self.outputText.update("")
        self.inputText.update("")

    def find_event(self, ev: str):
        for item in self._wd_events:
            if item[0] == ev:
                return item
        return None

    def run(self):
        # Create the Window
        window = self._create_window()
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            item = self.find_event(event)
            if item:
                _, func = item
                func()
                continue
            if event.startswith("custom-"):
                idx = int(event.split("-")[1])
                text = self.inputText.get()
                actions = list(filter(None, map(str.strip, configure.config.buttons[idx].actions.split("\n"))))
                # print(actions)
                for _act_name in actions:
                    # print('exec', _act_name)
                    info = [_info for _info in text_act_infos if _info.label == _act_name][0]
                    text = info.func(text)
                self.outputText.update(text)
                continue
            if event == "_conf_wnd":
                open_config_window()
                window.close()
                # sg.clean
                del window
                window = self._create_window()
                continue
            print('You entered ', event, values[0])

        window.close()

"""
想著要出一本著作
HELLO WORLD ｅｒａｓｄｇｄａｇ
"""
MainWindow().run()
