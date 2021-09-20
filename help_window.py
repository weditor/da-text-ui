# -*- coding: utf-8 -*-
import PySimpleGUI as sg


def open_help_window():
    text = """
程序介绍: 数据部文本处理程序
源码: https://github.com/weditor/da-text-ui

说明:
1. 优化生僻字显示为 □ 的问题
2. (一定程度上)优化拼音多音字问题, 
   比如 "了解了" => "liao jie le"
3. (一定程度上)优化简繁转换对应错误的问题, 
   比如 "想著一本著作" => "想着一本著作"

如果使用过程中遇到问题或者有改进意见，请联系 aochujie 。
欢迎邮件或vanish轰炸。
    """
    help_wd = sg.Window("关于", layout=[[sg.Text(text)]], keep_on_top=True, modal=True, icon="resources/images/txt_icon.ico")
    event, value = help_wd.read(close=True)
    help_wd.close()
    
