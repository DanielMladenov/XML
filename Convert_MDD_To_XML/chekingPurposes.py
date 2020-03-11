import pandas as pd
import xml.etree.ElementTree as ET
import re

tree = ET.parse('C:\\Users\\Daniel.Mladenov\\Documents\\GitHub\\XML\\Convert_MDD_To_XML\\ManualTest.xml')
root = tree.getroot()


for MddTree in root.iter('variable'):
    #Flat_Grid = MddTree.attrib.values()
    flat_Grid = MddTree.get('level')
    print(flat_Grid)
    for ques in MddTree.iter('name'):
        print(ques.text)
    for title in MddTree.iter('title'):
        for titleText in title.iter('text'):
            print(titleText.text)
    for categories in MddTree.iter('categories'):
        for value in categories.iter('value'):
            print(value.text)
            for valueText in value.iter('text'):
                print(valueText.text)
