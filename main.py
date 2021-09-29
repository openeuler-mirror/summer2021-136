from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import fileIdentify
import generatePdf
import init


# 创建一个简单的GUI
class boxLayoutExample(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=50, padding=50)  # 创建Layout
        label1 = Label(text='Please fill the path of each RPM into the text box to separate by newline',
                       font_size='20sp',
                       markup=True)
        layout.add_widget(label1)
        textinput = TextInput(text='path', font_size=20)
        layout.add_widget(textinput)
        buttons = ['identify', 'compare']  # 设置按键的标签
        button = Button(text=buttons[0], size_hint=(.5, .5),
                        pos_hint={"center_x": .5, "center_y": .5})
        button.bind(on_press=lambda self: Identify(textinput.text))
        layout.add_widget(button)
        button = Button(text=buttons[1], size_hint=(.5, .5),
                        pos_hint={"center_x": .5, "center_y": .5})
        button.bind(on_press=lambda self: Compare(textinput.text))
        layout.add_widget(button)
        return layout


# 用于GUI的对比按键的函数，输入要对比的脚本，返回一个包含所有脚本对比信息的列表
def Compare(message):
    addlist = init.getmessage(message)
    tem = []
    for x in fileIdentify.fileIdentify(addlist):
        x[2], lll = init.init(x[2])
        x.append(lll)
        tem.append(x)
    tem = init.comparescriptlist(tem)
    generatePdf.generate2(tem)


# 用于GUI的识别按键的函数,输入GUI文本框中的文字，调用需要的函数
def Identify(message):
    addlist = init.getmessage(message)
    tem = []
    for x in fileIdentify.fileIdentify(addlist):
        x[2], lll = init.init(x[2])
        x.append(lll)
        tem.append(x)
    generatePdf.generate1(tem)


if __name__ == "__main__":
    app = boxLayoutExample()
    app.run()
