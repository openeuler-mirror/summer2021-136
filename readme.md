

#  Summer2021-No.136 识别软件包里的Shell脚本与其调用的系统命令和服务

## 介绍

RPM软件包中会存在一些Shell脚本，他们会调用一些系统命令和服务，通常情况下，是需要我们实际执行这些脚本才能知道他们执行了哪些操作，调用了什么系统命令或服务，这个项目通过对脚本文本进行分析，用一种不执行的方式识别出脚本进行的操作，从而可以提前对软件兼容性进行分析。

## 软件架构

### fileIdentify.py
输入rpm包的地址，将其中的shell脚本识别出来，并且对其进行预处理，以便下一步的识别。
### init.py
init.py是该脚本处理工具的主体。主要是通过PLY对shell文本进行分词后再筛选出所调用的命令。该程序的基本工作流程是，先将shell脚本用PLY的lex模块变成一系列token序列，之后依次提取可能执行的命令（包含在循环块中的命令，包含在条件块中的命令），提取shell脚本中的函数生成函数表，对主程序中调用的命令和函数进行提取，分析出哪些脚本会被调用，并且可以对多个脚本进行对比。
### generatePdf.py
利用reportlab库生成识别和对比报告。
### test.py
用于在命令行下调用程序。
### main.py
使用kivy库为程序提供简单的GUI。
### commands.json
包含了所有要识别的命令。
## 安装说明

运行此项目需要python3.9的环境。

+ 获取项目文件

  ```shell
  git clone https://gitee.com/openeuler-competition/summer2021-136
  ```

+ 安装reportlab库，用来生成pdf

  ```shell
  pip install reportlab
  ```

+ 安装kivy库，用以支持GUI

  ```shell
  python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
  python -m pip install kivy.deps.gstreamer
  python -m pip install kivy
  ```

## 使用说明

### 若采用命令行的方式运行

+ 在命令行下运行以下命令	

  ```shell
  python test.py
  ```

+ 按照提示输入RPM包的地址

+ 若要识别示例文件输入以下内容

  ```
  2
  testfile/rpmtest1
  testfile/rpmtest2
  ```

+ 生成的pdf保存在当前目录下，Script_contrast.pdf保存了脚本对比信息，Script_identification.pdf保存脚本识别信息。

### 采用图形界面方式运行

+ 在命令行下运行以下命令

  ```
  python main.py
  ```

+ 在文本框下输入RPM包地址

+ 若要识别示例文件输入以下内容

  ```
  testfile/rpmtest1
  testfile/rpmtest2
  ```

+ 生成的pdf保存在当前目录下，Script_contrast.pdf保存了脚本对比信息，Script_identification.pdf保存脚本识别信息。


## 帮助

+    [PLY文档](http://www.dabeaz.com/ply/) 这个命令分析器最初的设想是用PLY将所有的python语法识别，进而可以准确的得知哪些命令被运行。但是由于时间原因，没能完成所有的语法解析，对于处于条件块中的语句，不能根据不同的情况，判断出是否会执行，但是对于这些命令，会给出可能会执行的标记。之后完成对shell语法的解析后会对这一块进行优化。
+    [Bash](http://www.gnu.org/software/bash/) Bash的源码中含有最初的yacc文件，可以参考其完成对shell的解析。
