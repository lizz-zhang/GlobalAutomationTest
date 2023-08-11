# -*- coding: utf-8 -*-
"""
======================
@author:nash
@time:12/17/2021:3:18 PM
@email:nash.xiang@comm100.com
======================
"""
import yaml
from pathlib import Path
import os
from autoUtils.optionUtil import ifItemInKeysAndValueNotNone

class ReadFile:
    def __init__(self, filename):
        basedir = Path(__file__).resolve().parent.parent
        self.path = os.path.join(basedir, filename)
        self.result = []
        #print("filepath is ", self.path)

    def _get_data(self, *paras):
        case_name = []
        case_input = []
        case_output = []
        with open(self.path, 'r', encoding='utf-8') as f:
            data = yaml.load(f.read(), Loader=yaml.SafeLoader)
            for cases in data['alltest']:
                for testType in cases.keys():
                    if testType == str(paras[0]):
                        for icases in cases[testType]:
                            case_name.append(icases.get(paras[1], ''))
                            case_input.append(icases.get(paras[2], {}))
                            case_output.append(icases.get(paras[3], {}))
        parameters = zip(case_name, case_input, case_output)
        return case_name, parameters

    def get_businessTests_data(self):
        return self._get_data('businessTests', 'case', 'http', 'expect')

    def get_ingressPathTest_data(self):
        return self._get_data('ingressPathTest', 'case', 'http', 'expect')

    def get_illegalInputTests_data(self):
        '''
        通过获取类型是illegalInputTest的用例标识。获取对应的标准输入body和case
        然后通过body改造器讲body进行自动生成各种错误的输入用例
        再通过dict的特性，每次更新最初的dict，将更改后的用例名称，body，expect内容更改后。重新组合成新的测试用例
        新测试用例和原始的测试用例保持格式一致。直接可用于测试用例使用
        :return: list（caseNames），zip（case，http，expect）
        '''
        case_name = []
        case_input = []
        case_output = []
        returnCaseName,returnCaseData = self._get_data('illegalInputTest','case', 'http', 'expect')
        #经过Body数据的更新,
        flist, initialDict, changeBodyList = self.updateDictByKey(self.getDictKeyValue, self.getDict)
        if isinstance(returnCaseData, zip):
            caseName = returnCaseName[0]
            flistLenth = len(flist)
            for i in range(0, flistLenth, 1):
                requireField = self.getCaseInfoByElement('requirefield')
                for filed in requireField:
                    if str(filed).__contains__('0'):
                        newFiled = str(filed).replace('.0','')
                    else:
                        newFiled = filed
                    if newFiled == flist[i]:
                        expectDict = self.getCaseInfoByElement('expect')
                        httpDict = self.getCaseInfoByElement('http')
                        case_name.append(caseName + ' - ' + flist[i] + ' field miss')
                        httpDict['body'] = changeBodyList[i]
                        case_input.append(httpDict)
                        message = str(self.getCaseInfoByElement('errormessage'))
                        #字典每次都会更新掉，只能获取到最后一个字典
                        if ifItemInKeysAndValueNotNone('errormessage', expectDict):
                            expectDict['errormessage'] = message % str(flist[i])
                        case_output.append(expectDict)
        parameters = zip(case_name, case_input, case_output)
        return case_name, parameters

    def get_illegalInputTests_data_MissField(self):
        '''
        通过获取类型是illegalInputTest的用例标识。获取对应的标准输入body和case
        然后通过body改造器将body进行自动生成各种错误的输入用例
        再通过dict的特性，每次更新最初的dict，将更改后的用例名称，body，expect内容更改后。重新组合成新的测试用例
        新测试用例和原始的测试用例保持格式一致。直接可用于测试用例使用
        :return: list（caseNames），zip（case，http，expect）
        '''
        case_name = []
        case_input = []
        case_output = []
        returnCaseName,returnCaseData = self._get_data('illegalInputTest','case', 'http', 'expect')
        if isinstance(returnCaseData, zip):
            caseName = returnCaseName[0]
            requireField = self.getCaseInfoByElement('requirefield')
            changeBodyList = self.removeDictKeyByKey(requireField, self.getDict)
            requireFieldLen = len(requireField)
            for k in range(0, requireFieldLen, 1):
                expectDict = self.getCaseInfoByElement('expect')
                httpDict = self.getCaseInfoByElement('http')
                case_name.append(caseName + ' - ' + requireField[k] + ' field miss')
                httpDict['body'] = changeBodyList[k]
                case_input.append(httpDict)
                message = str(self.getCaseInfoByElement('errormessage'))
                # 字典每次都会更新掉，只能获取到最后一个字典
                expectDict['errormessage'] = message % str(requireField[k])
                case_output.append(expectDict)
        parameters = zip(case_name, case_input, case_output)
        return case_name, parameters

    def getDictKeyValue(self, keyStr, udict):
        if not isinstance(udict, dict):  # 对传入数据进行格式校验
            return 'argv[1] not an dict'
        for key in udict.keys():  # 传入数据不符合则对其value值进行遍历
            keyString = ''
            if not keyStr:
                keyString = key
            else:
                keyString = keyStr + '.' + key
            self.result.append(keyString)
            if isinstance(udict[key], dict):
                self.getDictKeyValue(keyString, udict[key])  # 传入数据的value值是字典，则直接调用自身
            elif isinstance(udict[key], (list, tuple)):
                for val_ in udict[key]:
                    if isinstance(val_, dict):
                        self.getDictKeyValue(keyString, val_)  # 传入数据的value值是字典，则调用get_target_value
            else:
                pass
        return self.result

    def getDict(self):
        with open(self.path, 'r', encoding='utf-8') as newf:
            newData = yaml.load(newf.read(), Loader=yaml.SafeLoader)
            for cases in newData['alltest']:
                for testType in cases.keys():
                    if testType == 'illegalInputTest' and len(cases[testType]) == 1:
                        for icases in cases[testType]:
                            return (icases.get('http'))['body']

    def getCaseInfoByElement(self,message):
        with open(self.path, 'r', encoding='utf-8') as newM:
            newData = yaml.load(newM.read(), Loader=yaml.SafeLoader)
            for cases in newData['alltest']:
                for testType in cases.keys():
                    if testType == 'illegalInputTest' and len(cases[testType]) == 1:
                        for icases in cases[testType]:
                            if message in icases.get('expect').keys():
                                return icases.get('expect')[message]
                            elif message == 'http':
                                return icases.get('http')
                            elif message == 'expect':
                                return icases.get('expect')
                            else:
                                return None

    def getHttpDict(self):
        with open(self.path, 'r', encoding='utf-8') as newM:
            newData = yaml.load(newM.read(), Loader=yaml.SafeLoader)
            for cases in newData['alltest']:
                for testType in cases.keys():
                    if testType == 'illegalInputTest' and len(cases[testType]) == 1:
                        for icases in cases[testType]:
                            return icases.get('expect')


    def updateDictByKey(self,getkeyListFunc, getDictFunc):

        lResult = []
        initialDict = getDictFunc()
        keyList = getkeyListFunc('', initialDict)
        if not isinstance(keyList, list):  # 对传入数据进行格式校验
            return 'argv[1] not a List'
        # 循环遍历字典的所有key，如果有子节点。就用.连接所有的几点。比如：bbb.c.c2
        for key in keyList:
            # 确保每次获取的字典都是一样的
            ardict = getDictFunc()
            # 对列表的每一项进行处理。已确定当前的节点，是否是dict或者是list，如果是dict就直接赋值。如果是list则需要拼装dict取值语句
            if str(key).count('.') > 0:
                k = 'ardict'
                evalk = ''
                icount = 0
                kList = key.split('.')
                for i in kList:
                    # 拼接执行语句，eval调用可以返回执行的结果
                    evalk = 'isinstance(' + k + "['" + i + "']" + ', dict)'
                    # print(evalk)
                    # 判断当前节点是否是dict或者list
                    isDict = eval(evalk)
                    # 如果是dict，则拼接执行语句为dict['aaaa']。如果是list，则拼接执行语句为dict['aaaa'][0]['bb']
                    icount += 1
                    if not isDict:
                        # 这里连续相同的参数，导致判断是否为最后一个出现问题。通过icount计数和key.split('.')的长度作比较来判断是不是最后一个元素
                        if str(key).endswith(i) and len(kList) == icount:
                            k = k + "['" + i + "']"
                        else:
                            k = k + "['" + i + "'][0]"
                    elif isDict:
                        k = k + "['" + i + "']"
                # 拼接最后的值。可以自定义多个值，循环处理
                k = k + ' = None'
                #print(k)
                # 执行拼接的python语句。并不返回
                exec(k)
                # 将获取到的字典，加入到结果list中
                lResult.append(ardict)
            else:
                ardict[str(key)] = None
                lResult.append(ardict)
            #print(ardict)
        return keyList,initialDict,lResult

    def removeDictKeyByKey(self, removeKeyList, getDictFunc):

        dlResult = []
        initialDict = getDictFunc()
        if not isinstance(removeKeyList, list):  # 对传入数据进行格式校验
            return 'argv[1] not a List'
        # 循环遍历字典的所有key，如果有子节点。就用.连接所有的几点。比如：bbb.c.c2
        for item in removeKeyList:
            # 确保每次获取的字典都是一样的
            initDict = getDictFunc()
            self.deepDictDel(item,initDict)
            dlResult.append(initDict)
        return dlResult

    def deepDictDel(self,path, dict):
        for key in path.split('.'):
            owner = dict
            if key == '0':
                dict = dict[int(key)]
            else:
                dict = dict[key]
        del owner[key]


if __name__ == "__main__":
    # for test
    #filepath1 = 'F:\\auto\\pytest\\data\\webpage\\test_webpage.yml'
    filepath2 = 'E:\\share\\NewBotAutomation\\testCases\\TestData\\bottesting\\apiTestData\\test_api.yml'

    rf = ReadFile(filepath2)
    #test = rf.updateDictByKey(rf.getDictKeyValue,rf.getDict)
    #for i in test:
    #    print(json.dumps(i))
    #print(type(test))
    #tt = rf.getDict()
    #print(tt)
    #print({"A": {"C": {"D": [{"E": 4, "D": "test"}], "F": 5}}, "D": 2})

    #t1 = rf.removeDictKeyByKey(['A.C.D','A.C.D.0.D'],rf.getDict)
    #t1 = rf.getCaseInfoByElement('responsestate')
    if str("A.C.D.0.D").__contains__('0') and str("A.C.D.0.D").replace('.0', '') == 'A.C.D.D':
        print("passed")
    t2,t3 = rf.get_illegalInputTests_data()
    print(t2)
    print(list(t3))
    print("finished")


