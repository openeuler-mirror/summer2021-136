import fileIdentify
import generatePdf
import init

if __name__ == '__main__':
    i = input('请输入要识别的rpm包数量：')
    tem = []
    addlist = []
    for x in range(int(i)):
        addlist.append((input('请输入软件包地址:')))
    # 命令识别
    for x in fileIdentify.fileIdentify(addlist):
        x[2], lll = init.init(x[2])
        x.append(lll)
        tem.append(x)
    generatePdf.generate1(tem)
    tem = init.comparescriptlist(tem)
    generatePdf.generate2(tem)
