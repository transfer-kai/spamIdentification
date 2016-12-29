# -*- coding:utf-8 -*-
#英文垃圾邮件识别
#@zhangkai
#2016.12.29
import re
import sklearn.naive_bayes as NBC
#定义一个垃圾邮件识别类
class spamIdentification(object):
    def __init__(self):
        pass

#词袋：创建一个包含在所有文档中的不重复的词的列表
    def createVocabList(self,dataSet):
        vocabSet=set([])
        for document in dataSet:
            vocabSet=vocabSet|set(document)
        return list(vocabSet)

#接受字符串并将其解析为字符串列表
    def textParse(self,bigString):
        listOfTkones=re.split(r'\W*',bigString)
        token=[tok.lower() for tok in listOfTkones if len(tok)>2]
        return token

#词向量1：向量的每一位置为1或0，表示单词是否在词袋中
    def setOfWords2Vec(self,vocabList,inputset):
        returnVec=[0]*len(vocabList)
        for word in inputset:
            if word in vocabList:
                returnVec[vocabList.index(word)]=1
        return returnVec

#词向量2：向量的每一位置表示在词袋中单词出现的次数
    def bagOfWords2Vec(self,vocabList,inputset):
        returnVec=[0]*len(vocabList)
        for word in inputset:
            if word in vocabList:
                returnVec[vocabList.index(word)]+=1
        return returnVec

#Email:表示训练邮件的位置;ham_num:非垃圾邮件数量；spam_num:垃圾邮件数量
    def Email2Vec(self,Email,ham_num,spam_num):
        docList=[]
        classList=[]
        fullText=[]
        for i in range(1,ham_num+1):
            wordList=self.textParse(open('Email/spam/%d.txt' %i).read())
            docList.append(wordList)
            classList.append(1)

        for i in range(1,spam_num+1):
            wordList=self.textParse(open('Email/spam/%d.txt' %i).read())
            docList.append(wordList)
            classList.append(0)

        vocabList=self.createVocabList(docList)

        trainMat=[]
        trainClasses=[]

        for i in range(ham_num+spam_num):
            trainMat.append(self.bagOfWords2Vec(vocabList,docList[i]))
            trainClasses.append(classList[i])
#返回email向量，email的label,和词袋
        return trainMat,trainClasses,vocabList

#此处用sklearn自带贝叶斯分类器
    def classifier_NBC(self):
        clf=NBC.GaussianNB()
        return clf

if __name__ == '__main__':
    email=spamIdentification()
    data,label,vocabList=email.Email2Vec(email,25,25)
#待识别邮件
    """
    emain_new='''
    You Have Everything To Gain!
    Incredib1e gains in length of
    3 - 4 inches to yourPenis, PERMANANTLY Amazing increase in thickness of yourPenis, up to 30 %
    BetterEjacu1ation control Experience Rock - HardErecetions Explosive, intenseOrgasns
    Increase volume of Ejacu1ate Doctor designed and endorsed
    100 % herbal, 100 % Natural, 100 % Safe'''
    """
#从文件中读入待识别邮件
    email_new=open('email_test.txt').read()

    emain_word=email.textParse(email_new)
    emain_data=email.bagOfWords2Vec(vocabList,emain_word)
#高斯朴素贝叶斯分类算法
    clf=email.classifier_NBC()
    clf.fit(data,label)
    predy=clf.predict(emain_data)
    if predy==1:
        print"This is a ham email"
    else:
        print "this is a spam email"




