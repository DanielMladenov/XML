import xml.etree.ElementTree as ET
import pandas as pd
import re


def cleanHtml(row_string):
    if row_string:
        cleanr = re.compile('<.*?>')
        #cleantext = re.sub(cleanr, '', row_string)
        cleantext = row_string.replace('</b>','')
        return str(cleantext)
    else:
        return str('InproperLabel')
def getLayout(quesName, value, labelName, xml):
    tree = ET.parse(xml)
    root = tree.getroot()

    myCat = []
    myLabel = []
    TempDict = {}
    finalDict = {}

    #myDataFrame = pd.DataFrame()

    for MddTree in root.iter('variable'):
        myQues = ''
        myCat = []
        myLabel = []
        TempDict = {}
        for ques in MddTree.iter(quesName):
            print(ques.text)
            myQues = ques.text
        for cat in MddTree.iter(value):
            #print(cat.text)
            totalyNeedlessFlag = False
            myCat.append(cat.text)
            for label in cat.iter(labelName):
                if totalyNeedlessFlag:
                    break
                #print(label.attrib)
                myTempVal = label.attrib.values()
                for key in myTempVal:
                    if key == 'en-US':
                        #print(label.text)
                        tempLabel = cleanHtml(label.text)
                        #if len(tempLabel) == 0 or tempLabel:
                            #tempLabel = "InproperLabel"
                        print(tempLabel)
                        myLabel.append(tempLabel)
                        totalyNeedlessFlag = True


        if len(myCat) > 0 and len(myLabel) > 0:
            #print(myQues, ' - ', myCat, ' - ', myLabel)
            #TempDict = {myQues : dict(zip(myCat, myLabel))}
            TempDict = {myQues : dict(zip(myCat, myLabel))}
            finalDict.update(TempDict)

    # ================ This is for checking Only

    #myDataFrame = pd.DataFrame(finalDict)
    return  finalDict


#C:\\Users\\Daniel.Mladenov\\github\\JTI\\
checkIfWork = getLayout(quesName = "name", value = "value", labelName = "text", xml = 'xml290120MDD.xml')
checkIfWork = pd.DataFrame(checkIfWork)
#print(checkIfWork)
#C:\\Users\\Daniel.Mladenov\\github\\JTI\\
checkIfWork.to_csv(r'TestCsv.csv')


for ques in checkIfWork.columns:
    series = pd.Series(checkIfWork[str(ques)].values)
    series = series.dropna()
    #print(series.dropna())
    if  any(series.duplicated()):
        listOfDup = series[series.duplicated()]
        #print( ques + ' Ima dublikat - ' + str(listOfDup) )
