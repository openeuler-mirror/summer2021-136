import os


# 输入rpm包地址将其解压
def unpack(rpmpath):
    try:
        os.system("rpm2cpio {} | cpio -div.format()")
    except Exception:
        print("解压不成功")


# 给出一个文件目录识别其后缀是否为.sh
def isShellfile1(path):
    return path.endswith(".sh")


# 调用file命令判断一个文件是否为shell文件
def isShellfile2(path):
    string = str(os.system("file -b " + path))
    return string.startswith("Bourne-Again shell script") | \
           string.startswith("a /usr/bin/sh script") | \
           string.startswith("POSIX shell script")

