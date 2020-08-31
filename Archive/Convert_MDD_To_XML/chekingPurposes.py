import pandas as pd
import xml.etree.ElementTree as ET
import re

tree = ET.parse('C:\\Users\\Daniel.Mladenov\\Documents\\GitHub\\XML\\Convert_MDD_To_XML\\ManualTest.xml')
root = tree.getroot()

for flatQues in root.iter('columns'):
    for MddTree in flatQues.iter('variable'):
        #Flat_Grid = MddTree.attrib.values()
        flat_Grid = MddTree.get('level')
        print(flat_Grid)
        if flat_Grid == '0': #This is for the Flat Questions
            for ques in MddTree.iter('name'):
                print(ques.text)
            for title in MddTree.iter('title'):
                for titleText in title.iter('text'):
                    print(titleText.text)
            for categories in MddTree.iter('categories'):
                for value in categories.iter('value'):
                    print(value.text)
                    for valueText in value.iter('text'):
                        getLanguage = valueText.get('lang')
                        if getLanguage == 'en-US':
                            print(valueText.text)
