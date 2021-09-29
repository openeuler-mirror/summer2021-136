from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

# 调用模板，创建指定名称的PDF文档
doc = SimpleDocTemplate("Hello.pdf")
# 获得模板表格
styles = getSampleStyleSheet()
# 指定模板
style = styles['Normal']
# 初始化内容
story = []


# 用于生成表
def generatetable(dict):
    out = []
    tem = []
    out.append(['command', 'state'])
    for key, value in dict.items():
        if value == 0:
            continue
        elif value == -1:
            tem.append(key)
            tem.append('possible')
            out.append(tem)
            tem = []
        elif value > 0:
            tem.append(key)
            tem.append('called')
            out.append(tem)
            tem = []
    return out


# 用于对识别信息的PDF内容添加
def addstory1(list, story):
    for x in list:
        story.append(Paragraph("name of rpm:" + x[0], styles['Heading2']))
        story.append(Paragraph("address of rpm:" + x[1], styles['Heading2']))
        story.append(Paragraph("commands invoked in shell scripts", styles['Heading4']))
        data = generatetable(x[2])
        t = Table(data)
        t.setStyle(TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 2, colors.black)]))
        story.append(t)
        if len(x[-1]) > 0:
            story.append(Paragraph("commands to control services", styles['Heading4']))
            t = Table([x[-1]])
            t.setStyle(TableStyle(
                [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 2, colors.black)]))
            story.append(t)
        story.append(Paragraph(
            '-----------------------------------------------------------------------------------------------------------------------------------'))

    return story


# 用于对比内容的PDF添加
def addstory2(list, story):
    for x in list:
        story.append(Paragraph("Comparison between script " + x[0] + " and script " + x[1], styles['Heading2']))
        tem = []
        tem.append([x[0], '', x[1], ''])
        tem += x[4]
        t = Table(tem)
        t.setStyle(TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 2, colors.black)]))
        story.append(t)
    return story


# 用于生成识别脚本的pdf
def generate1(list):
    # 调用模板，创建指定名称的PDF文档
    doc = SimpleDocTemplate("Script_identification.pdf")
    # 获得模板表格
    styles = getSampleStyleSheet()
    # 指定模板
    style = styles['Normal']
    # 初始化内容
    story = []
    story.append(Paragraph("List of commands", styles['Title']))
    # 用于生成表
    doc.build(addstory1(list, story))


# 用于生成对比脚本的pdf
def generate2(list):
    # 调用模板，创建指定名称的PDF文档
    doc = SimpleDocTemplate("Script_contrast.pdf")
    # 获得模板表格
    styles = getSampleStyleSheet()
    # 指定模板
    style = styles['Normal']
    # 初始化内容
    story = []
    story.append(Paragraph("List of commands", styles['Title']))
    # 用于生成表
    doc.build(addstory2(list, story))
