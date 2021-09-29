import os


# 输入rpm包地址将其解压
def unpack(rpmpath):
    try:
        os.system("rpm2cpio {} | cpio -div.format()")
    except Exception:
        print("解压不成功")


# 在windows中无法调用file命令，可以用这个函数来判断shell脚本
def isShellfile(path):
    f = open(path)
    data = f.readline()
    if data.startswith('#!/usr/bin/env sh'):
        return True
    else:
        return False


# # 调用file命令判断一个文件是否为shell文件
# def isShellfile(path):
#     string = str(os.system("file -b " + path))
#     return string.startswith("Bourne-Again shell script") | \
#            string.startswith("a /usr/bin/sh script") | \
#            string.startswith("POSIX shell script")


# 输入路径获取文件名
def getrpmname(str):
    return os.path.split(str)[1]


# 输入一个文件目录和一个空的list，以数组形式返回该目录下的所有文件地址，
def get_filelist(dir, Filelist):
    newDir = dir
    if os.path.isfile(dir):
        Filelist.append(dir)
        # # 若只是要返回文件文，使用这个
        # Filelist.append(os.path.basename(dir))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            # if s == "xxx":
            # continue
            newDir = os.path.join(dir, s)
            get_filelist(newDir, Filelist)
    return Filelist


# 输入一个目录列表，将每个目录视作一个解压后的软件包，返回一个三元组列表
# 第一个元素为软件包的名称，第二个元素为软件包地址，第三个元素为软件包中的内容
def fileIdentify(list):
    out = []
    tem = []
    data = ''
    for x in list:
        try:
            # unpack(x)
            tem.append(getrpmname(x))
            tem.append(x)
            temlist = get_filelist(x, [])
            for i in temlist:
                if isShellfile(i):
                    with open(i, 'r') as f:
                        data += f.read()
            tem.append(data)
            data = ''
        except(Exception):
            print('读入文件错误')
        out.append(tem)
        tem = []
    return out
