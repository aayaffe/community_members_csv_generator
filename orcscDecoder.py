import csv
import xml.etree.ElementTree as ET

classes = {}
results = {}

def getClasses(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    classItems = {}
    for item in root.findall('./Cls/ROW'):

        # empty class dictionary
        name = ""
        id = ""

        # iterate child elements of item
        for child in item:

            # special checking for namespace object content:media
            if child.tag == 'ClassId':
                id = child.text
            elif child.tag == 'ClassName':
                name = child.text
        classItems[id] = name

        # return boat items list
    return classItems

def getClass(id):
    return classes[id]


def getResult(id):
    return results[id]


def parseXML(xmlfile):
    # create element tree object
    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()

    # create empty list for boat items
    boatitems = []

    # iterate boat items
    for item in root.findall('./Fleet/ROW'):

        # empty boat dictionary
        boat = {}

        # iterate child elements of item
        for child in item:

            # special checking for namespace object content:media
            if child.tag == 'YID':
                boat['YID'] = child.text
            elif child.tag =='YachtName':
                boat['Name'] = child.text
            elif child.tag == 'ClassId':
                boat['Class'] = getClass(child.text)

                # append boat dictionary to boat items list
        boat['Overall'] = getResult(boat['YID'])
        boatitems.append(boat)

        # return boat items list
    return boatitems


def savetoCSV(boatitems, filename):
    # specifying the fields for csv file
    fields = ['YID', 'Name', 'Class', 'Overall']

    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(boatitems)


def getResults(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    resItems = {}
    for item in root.findall('./Rslt/ROW'):

        # empty class dictionary
        res = ""
        yid = ""

        # iterate child elements of item
        for child in item:

            # special checking for namespace object content:media
            if child.tag == 'YID':
                yid = child.text
            elif child.tag == 'PosOvl':
                res = child.text
        resItems[yid] = res

        # return boat items list
    return resItems


def first():
    global classes, results
    classes = getClasses('results.orcsc')
    results = getResults('results.orcsc')
    boatitems = parseXML('results.orcsc')




    # store boat items in a csv file
    savetoCSV(boatitems, 'topboat.csv')


first()
