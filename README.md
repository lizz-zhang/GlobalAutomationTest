# README

---

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)


## Install
安装python3.8.2，并配置path环境变量

Python官网：https://www.python.org/


本工具基于python3.8.2开发，需要安装以下第三方插件：

```
直接通过requirements.txt安装
pip install -r requirements.txt
或者通过下列指令安装：
pip install pytest
pip install allure-pytest
pip install requests
pip install selenium
pip install pyyaml
pip install pyodbc
pip install jsonschema
pip install deepdiff
pip install filelock
pip install pytest-xdist
pip install pytest-assume
```

此外，还需要安装allure，具体安装步骤可以参考下面文档
https://www.cnblogs.com/wsy1103/p/10530397.html

性能测试框架工具：
https://locust.io

JsonSchema相关内容参考：
```
通过json串自动生成schema: 
https://jsonschema.net/
https://www.liquid-technologies.com/online-json-to-schema-converter
jasonchema的相关介绍:
https://json-schema.org/understanding-json-schema/index.html
浏览器运行exe下载可以参考：
https://npm.taobao.org/mirrors/chromedriver/
```





## File Structure

```
.\pytest.ini	#基础pytest参数
.\autoUtils     #测试使用的工具类
.\autoConfig	#测试使用的配置信息
.\testCases\apiTestCases\test_xxx.py    #接口测试用例
.\testCases\uiTestCases\test_xxx.py     #UI测试用例
.\testCases\performanceTestCases\test_xxx.py    #性能测试用例
.\testCases\testData                            #测试数据（根据环境命名，每个环境下面对应api和ui,性能测试用例）
.\autoReports\xxx                               #测试结果，用于生成报告
```

## Usage
在pytest.ini文件中进行pytest参数的配置，然后运行下面命令

```
*指定环境和标签运行用例
$ python -m pytest --environment dash11testing -m illegalinputtest 按照pytest.ini配置项进行选择运行对应的case。环境是dash11testing环境，指定运行反向用例
说明：--environment 指定需要运行的测试环境
      -m 指定运行带有指定标签的用例（类似于 pytest -m smoke），一个case可以打多个mark（标签示例： @pytest.mark.smoke） 
*多workd和分布式运行用例。由于有scope=class的装饰器。所以我们设计和运行分布式时，都通过下面方式运行,按照loadfile或者class/module分组
*我们用例采用多标签标识，方便指定运行和不运行特定标签的case，由于目前未做校验，illegalinputtest用例将不执行
$ python -m pytest --environment dash11testing -m "bot and not illegalinputtest" -n 4 --dist=loadfile
$ python -m pytest --environment dash11testing -m nash -n 4 --dist=loadscope

# 运行完成后，在项目的根目录下，cmd中使用下面命令生成allure测试结果
allure generate autoreports\ -o autoreports\html\ --clean
此时会在autoreports\html文件夹下面生成allure报告，浏览器访问index.html页面即可查看报告

PS：这里还有一种方式生成allure测试结果
$ allure serve autoreports\	
```

## Maintenances

BotTeam
