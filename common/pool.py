"""
操作win系统选择图片工具
"""
import win32gui
import win32con


# edit - combobox - comboBoxEx32 - #32770  编辑框在第四级
# button - #32770  打开按钮在第二级

# 前提：window上传窗口已经出现，最好sleep 1-2秒等待窗口出现

def upload(filepath, browser_type="chrome"):
    if browser_type == "chrome":
        title = "打开"
    else:
        title = ""
    # 找元素
    # 从一级开始找，一级窗口“#32770”，“打开”
    dialog = win32gui.FindWindow("#32770", title)  # FindWindow用于找大窗口

    # 二级之后都用FindWindowEx，需要四个参数，
    # 1、元素的父亲，2、从第一个子代开始找元素，3、元素的类型名（class），4、元素的文本值
    comboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级
    comBox = win32gui.FindWindowEx(comboBoxEx32, 0, "ComboBox", None)  # 三级
    # 编辑框
    edit = win32gui.FindWindowEx(comBox, 0, 'Edit', None)  # 四级
    # 打开按钮
    button = win32gui.FindWindowEx(dialog, 0, 'Button', '打开(&0)')  # 二级

    # 往编辑框输入文件路径
    win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filepath)  # 发送文件路径
    win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮


if __name__ == '__main__':
    upload(r'C:\Users\ilzyy\Pictures\Saved Pictures\7c054fa99bb34a7f8ff6cfa161d62d18.jpg')
