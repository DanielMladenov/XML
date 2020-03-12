import pandas as pd
import xml.etree.ElementTree as ET
import re

tree = ET.parse('C:\\Users\\Daniel.Mladenov\\Documents\\GitHub\\XML\\Convert_MDD_To_XML\\ManualTest.xml')
root = tree.getroot()


for flatQuestions in root.iter('columns'):
    for variable in flatQuestions.findall('variable'):
        print(variable.get('level'))


for gridQuestions in root.iter('tables'):
    for variable in gridQuestions.findall('variable'):
        print(variable.get('level'))
        for invariable in variable.findall('variable'):
            print(invariable.get('level'))
