import os
# 输入rpm包地址将其解压
def unpack(rpmpath):
    try:
        os.system("rpm2cpio {} | cpio -div.format()")
    except Exception:
        print("解压不成功")

if __name__=='__main__':
    i = input('请输入要解压的rpm数量:')
    for x in range(int(i)):
        unpack(input('请输入rpm地址:'))