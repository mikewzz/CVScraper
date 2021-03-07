import bs4
import re
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#CHANGE this url to the location of the html form file saved for this specific project
#my_url = input("Please paste the LOCAL URL of the .html file of project form: ")
#cv_pid = input("Please type in the CV project ID (I.e., T001): ")
#FOR TESTING UNCOMMENT CODE BELOW TO MANUALLY INSERT URL
my_url = "file:///C:/Users/mikew/Programming/WebScraper/The%20Market%20Tester%E2%84%A2%20Results%20Upload%20%E2%80%93%20Enabling%20Ideas.html"
#CHANGE THIS TO PROJECT NUMBER IN QUOTATIONS (I.e., "T001")
cv_pid = "T001"


uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

fileName = "DecipherCodeToCopy.txt"
f= open(fileName,"w")
excelName = "ConceptHighlighters.csv"

#Panel Size
pSize_temp = page_soup.find("tr",{"id":"gv-field-21-41"})
if pSize_temp is not None:
    pSize = int(pSize_temp.td.text)
    f.write("#-------------THE PANEL SIZE FOR THIS STUDY IS: " + str(pSize) + "-------------#" + "\n")

#Type Of Study
sType_temp = page_soup.find("tr",{"id":"gv-field-21-16"})
oSType_temp = page_soup.find("tr",{"id":"gv-field-21-17"})
if sType_temp is not None:
    sType = str(sType_temp.td.text)
    if not(sType == "Other"):
        f.write("STUDY_TYPE.val = " + '"' + str(sType) + '"' +"\n")
    elif sType == "Other":
        if oSType_temp is not None:
            oSType = str(oSType_temp.td.text)
            f.write("STUDY_TYPE.val = " + '"' + str(oSType) + '"' + "\n")                                                                          
else:
    f.write("STUDY_TYPE.val = N/A" +"\n")

#Number Of Cells
numCells_temp = page_soup.find("tr",{"id":"gv-field-21-18"})
numCells = int(numCells_temp.td.text)
f.write("CellNum.val = " + str(numCells) +"\n")

#CellNames
cellNameList = []
for count,eachCellIndex in enumerate(range(66,74)):
    if count < numCells:
        temp1 = cellNameList.append(page_soup.find("tr",{"id":"gv-field-21-" + str(eachCellIndex)}).td.text)
        #print(temp1)
#print(cellNameList)
for eachCellLabel in range(numCells):
    f.write("p.cellName" + str(eachCellLabel+1) + " = " + '"' + cellNameList[eachCellLabel] + '"' +"\n")
    f.write("p.cellIMG" + str(eachCellLabel+1) + " = " + '"' + cv_pid + "_Cell_" + str(eachCellLabel+1) + '"' +"\n")


#Type of material used for this study
materialType_temp = page_soup.find("tr",{"id":"gv-field-21-75"})
if materialType_temp is not None:
    materialType = (materialType_temp.td.text)
    if materialType == "text":
        f.write("MATERIAL_TYPE.val = 0" +"\n")
    elif materialType == "image":
        f.write("MATERIAL_TYPE.val = 1" +"\n")      
else:
    f.write("MATERIAL_TYPE.val = 2" +"\n")


#Cell TEXT IF Material Type is "text" based
if materialType_temp is not None and (str(materialType_temp.td.text) == "text"):
    e= open(excelName,"w")
    cellText = []
    cellTextFieldIDs = [74,76,77,78,79,80,81,82]
    for count,eachCellTextIndex in enumerate(cellTextFieldIDs):
        if count < numCells:
            e.write("<define label=\"Con" + str(count+1) +"\" builder:title=\"Concept" + str(count+1) + "\">" +"\n")
            tempFullConcept = (page_soup.find("tr",{"id":"gv-field-21-" + str(eachCellTextIndex)}).td.text)
            listFullConcept = tempFullConcept.split()
            for wordIndex,eachWord in enumerate(listFullConcept):
                e.write("<row label=\"r" + str(wordIndex + 1) + "\" hottext:disable=\"0\" translateable=\"0\">" + str(eachWord) + "</row>" +"\n")
            e.write("</define>" +"\n\n")
#IF Material Type is "image" based; save images locally
elif materialType_temp is not None and (str(materialType_temp.td.text) == "image"):
    print ("PLACEHOLDER")

#Country Filter
countryChk_temp = page_soup.find("tr",{"id":"gv-field-21-39"})
if countryChk_temp is not None:
    countryChk = (countryChk_temp.td.text)
    if countryChk == "ca":
        f.write("COUNTRY_FLAG.val = 0" +"\n")
    elif countryChk == "us":
        f.write("COUNTRY_FLAG.val = 1" +"\n")
    elif countryChk == "both":
        f.write("COUNTRY_FLAG.val = 2" +"\n")        
else:
    f.write("COUNTRY_FLAG.val = 2" +"\n")

#Canada Region Filter
caRegion_temp = page_soup.find("tr",{"id":"gv-field-21-48"})
if caRegion_temp is not None:
    caRegion = (caRegion_temp.td.text)
    if caRegion == "Western Canada":
        f.write("CA_REGION_FLAG.val = 0" +"\n")
    elif caRegion == "Eastern Canada":
        f.write("CA_REGION_FLAG.val = 1" +"\n")
else:
    f.write("CA_REGION_FLAG.val = 2" +"\n")

#USA Region Filter
usRegion_temp = page_soup.find("tr",{"id":"gv-field-21-50"})
usRegionlist = ["Northeast","Midwest","South","West"]
if usRegion_temp is not None:
    usRegion = (usRegion_temp.td.ul.text)
    #usRegion = list(filter(bool, usRegion.splitlines()))
    #print(usRegion)
    for eachRegion in range(4):
        if usRegionlist[eachRegion] in usRegion:
            f.write("p.usRegionFlag" + str(eachRegion+1) + " = 1" +"\n")
        else:
            f.write("p.usRegionFlag" + str(eachRegion+1) + " = 0" +"\n")
else:
    for eachRegion in range(4):
        f.write("p.usRegionFlag" + str(eachRegion+1) + " = 1" +"\n")

#Gender Filter
gender_temp = page_soup.find("tr",{"id":"gv-field-21-51"})
if gender_temp is not None:
    genderFilter = (gender_temp.td.text)
    if genderFilter == "Male":
        f.write("GENDER_FLAG.val = 0" +"\n")
    elif genderFilter == "Female":
        f.write("GENDER_FLAG.val = 1" +"\n")
else:
    f.write("GENDER_FLAG.val = 2" +"\n")

#Age Filter
age_temp = page_soup.find("tr",{"id":"gv-field-21-52"})
if age_temp is not None:
    ageFilter = (age_temp.td.text)
    if ageFilter == "Gen Z and Gen Y (18 - 44)":
        f.write("AGE_FLAG.val = 0" +"\n")
    elif ageFilter == "Gen X and Boomers (45+) Choice":
        f.write("AGE_FLAG.val = 1" +"\n")
else:
    f.write("AGE_FLAG.val = 2" +"\n")

#Education Filter
edu_temp = page_soup.find("tr",{"id":"gv-field-21-53"})
if edu_temp is not None:
    eduFilter = (edu_temp.td.text)
    if eduFilter == "High School Diploma or less":
        f.write("EDU_FLAG.val = 0" +"\n")
    elif eduFilter == "Trade, College, University Diploma, Degree or more":
        f.write("EDU_FLAG.val = 1" +"\n")
else:
    f.write("EDU_FLAG.val = 2" +"\n")

#Income Filter
income_temp = page_soup.find("tr",{"id":"gv-field-21-54"})
if income_temp is not None:
    incFilter = (income_temp.td.text)
    if incFilter == "99k or less":
        f.write("INCOME_FLAG.val = 0" +"\n")
    elif incFilter == "100k or moree":
        f.write("INCOME_FLAG.val = 1" +"\n")
else:
    f.write("INCOME_FLAG.val = 2" +"\n")

#q5 question text pipe
q5Txt_temp = page_soup.find("tr",{"id":"gv-field-21-22"})
if q5Txt_temp is not None:
    q5Txt = (q5Txt_temp.td.text)
    f.write("p.q5qtext = " + '"' + str(q5Txt) + '"' + "\n")
else:
    f.write("p.q5qtext = \"0\"" + "\n")

#q6 question text pipe
q6Txt_temp = page_soup.find("tr",{"id":"gv-field-21-61"})
if q6Txt_temp is not None:
    f.write("p.q6ask = 1" +"\n")
    q6Txt = q6Txt_temp.td.table.tbody.text
    #Code to split str new lines, and filter out extra  'blank' elements
    q6Txt = list(filter(bool, q6Txt.splitlines()))
    #print((q6Txt))
    #print((q6Txt[2]))
    for eachQ6Label in range(numCells*2):
        if eachQ6Label %2 == 0:
            #print(eachQ6Label)
            f.write("p.cellPrice" + str((eachQ6Label+2) // 2) + " = " + '"$' + q6Txt[eachQ6Label] + '"' +"\n")
        elif eachQ6Label %2 == 1:
            #print(eachQ6Label)
            f.write("p.cellAmt" + str((eachQ6Label+1) // 2) + " = " + '"' + q6Txt[eachQ6Label] + '"' +"\n")
else:
    f.write("p.q6ask = 0" +"\n")                

#q7 question text pipe
q7Txt_temp = page_soup.find("tr",{"id":"gv-field-21-64"})
if q7Txt_temp is not None:
    q7Txt = (q7Txt_temp.td.ul.text)
    f.write("p.q7qtext = " + '"' + str(q7Txt) + '"' + "\n")
else:
    f.write("p.q7qtext = \"0\"" + "\n")

f.write("p.q8qtext = \"0\"" + "\n")
f.write("p.q9qtext = \"0\"" + "\n")    

f.close()