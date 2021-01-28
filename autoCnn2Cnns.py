# -*- coding: utf-8 -*-
# @Author: Terry Chan
# @Date:   2021-01-28 17:11:59
#!/usr/bin/env python
# coding=utf-8
"""用于批量转换ann文件为anns



"""



# from tkinter import *
# from tkinter.ttk import * # Frame, Button, Label, Style, Scrollbar
# from tkinter import filedialog as tkFileDialog
# from tkinter import font as tkFont
# from tkinter import messagebox as tkMessageBox

import re
from collections import deque
import pickle
import os.path
import platform
import codecs
import regex
from utils.recommend import *
import os
# import pdb
# pdb.set_trace()
from YEDDA_Annotator import getWordTagPairs

Bert_path="/home/terry/dev/model/chinese_roberta_wwm_ext_pytorch/"
    
    
    
    # def generateSequenceFile(self):
    #     """生成序列标注文件"""
    #     if (".ann" not in self.fileName) and (".txt" not in self.fileName): 
    #         out_error = u"导出功能只能用于 .ann 或 .txt 文件。"
    #         print(out_error)
    #         tkMessageBox.showerror(u"导出错误!", out_error)
    #         return -1
			
    #     with codecs.open(self.fileName, 'rU', encoding='utf-8') as f:
    #         fileLines = f.readlines()
        
    #     lineNum = len(fileLines)
    #     new_filename = self.fileName.split('.ann')[0]+ '.anns'
    #     with codecs.open(new_filename, 'w', encoding='utf-8') as seqFile: 
    #         for line in fileLines:
    #             if len(line) <= 2:
    #                 seqFile.write('\n')
    #                 continue
    #             else:
    #                 if not self.keepRecommend:
    #                     line = removeRecommendContent(line, self.recommendRe)
    #                 # print(line, self.seged, self.tagScheme, self.onlyNP, self.goldAndrecomRe)
    #                 # exit()
    #                 #处理一句标记信息
    #                 wordTagPairs = getWordTagPairs(line, self.seged, self.tagScheme, self.onlyNP, self.goldAndrecomRe)
    #                 for wordTag in wordTagPairs:
    #                     seqFile.write(wordTag)
    #                 ## use null line to seperate sentences
    #                 seqFile.write('\n')

    #     print(u"导出序列标注文件：", new_filename)
    #     print(u"行数：", lineNum)
    #     showMessage =  u"导出文件成功！\n\n"   
    #     showMessage += u"格式：" + self.tagScheme + "\n\n"
    #     showMessage += u"推荐：" + str(self.keepRecommend) + "\n\n"
    #     showMessage += u"分词：" + str(self.seged) + "\n\n"
    #     showMessage += u"行数：" + str(lineNum) + "\n\n"
    #     showMessage += u"文件：" + new_filename
    #     tkMessageBox.showinfo(u"导出信息", showMessage)

# 
def readFile(filename="./data/ChineseDemo.txt.ann"):
    """读取文件
    """
    textData=[]
    for line2 in open(filename):
        # print (line2)
        # if len(line2.split(" "))==2:
        textData.append(line2)
        # else:
        #     textData.append("\n"*2)

        

    text="".join(textData)


    return text
 
def main(file_path,seged, tagScheme, onlyNP, goldAndrecomRe):
    data=[]
    g = os.walk(file_path)  

    for path,dir_list,file_list in g:  
        for file_name in file_list:  
            if "ann" in file_name and ("anns" not in file_name):
                # print(os.path.join(path, file_name) )
                # print(readFile(os.path.join(path, file_name)))
                text=readFile(os.path.join(path, file_name))
                # print(len(text.split("\n")))

                # 分割后保留分隔符
                sentences=re.split(r"([。|！|？|\n])",text)
                sentences.append("")
                sentences = ["".join(i) for i in zip(sentences[0::2],sentences[1::2])]

                data=data+sentences
                
    # with open('data.txt','w') as f:    #设置文件对象
    #     for line in data[]:

    with open('dev.txt','w') as f:    #设置文件对象

        items=data[:int(len(data)*0.15)]
        for line in items:
            # line="我觉[@得你们#症状1*]啊，你们……[@我感觉你们新闻#描述1*]界还要学习[@一个，你们非常熟悉#描述1*]西方的这一套value。"
            tagedList= getWordTagPairs(line, seged, tagScheme, onlyNP, goldAndrecomRe)
            f.write(''.join(tagedList))
            f.write("\n\n")
    with open('train.txt','w') as f:    #设置文件对象

        items=data[int(len(data)*0.15):int(len(data)*0.85)]
        for line in items:
            # print(len(line))
            # if len(line)>100:
            #     print(line)
            # line="我觉[@得你们#症状1*]啊，你们……[@我感觉你们新闻#描述1*]界还要学习[@一个，你们非常熟悉#描述1*]西方的这一套value。"
            tagedList= getWordTagPairs(line, seged, tagScheme, onlyNP, goldAndrecomRe)
            f.write(''.join(tagedList))
            f.write("\n\n")
    with open('test.txt','w') as f:    #设置文件对象
        items=data[int(len(data)*0.85):]
        for line in items:
            # line="我觉[@得你们#症状1*]啊，你们……[@我感觉你们新闻#描述1*]界还要学习[@一个，你们非常熟悉#描述1*]西方的这一套value。"
            tagedList= getWordTagPairs(line, seged, tagScheme, onlyNP, goldAndrecomRe)
            f.write(''.join(tagedList))
            f.write("\n\n")
if __name__ == '__main__':
    seged=True
    tagScheme="BMES"
    onlyNP=False
    goldAndrecomRe=r'\[\@.*?\#.*?\*\](?!\#)'
    file_path="/home/terry/dev/data/药典标注后/"
    # file_path="/home/terry/dev/data/test/"
    # file_path=input("anns文件目录")
    main(file_path,seged, tagScheme, onlyNP, goldAndrecomRe)