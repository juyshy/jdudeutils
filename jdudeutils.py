# !/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Copyright:   (c) Jukka 2014
# Licence:     <your licence>
# -------------------------------------------------------------------------------


import zipfile
import json
import time
import os
import hashlib
import itertools
import re
from diskwalk_api import diskwalk

try:
    from PIL import Image
except:
    print('PIL not found')
try:
    import pyperclip
except:
    print('pyperclip not found')


import sys  # , re
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import string
from datetime import datetime
import subprocess

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("BeautifulSoup not found")


try:
    def paste_from_clipboard():
        return pyperclip.paste()

    def copy_to_clipboard(msg):
        pyperclip.copy(msg)
except:
    pass


from difflib import SequenceMatcher

def getStrDiffs(str1, str2):
    s = SequenceMatcher(None, str1, str2)

    diffs=[]
    diffs2=[]
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag != 'equal':
            diffs.append((tag, i1, i2, str1[i1:i2], j1, j2, str2[j1:j2]))
            diffs2.append((tag,   str1[i1:i2],   str2[j1:j2]))
    return diffs, diffs2

def getStrEquals(str1, str2):
    s = SequenceMatcher(None, str1, str2)

    equals=[]
    #diffs2=[]
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'equal':
            #diffs.append((tag, i1, i2, str1[i1:i2], j1, j2, str2[j1:j2]))
            equals.append((tag,   str1[i1:i2],   str2[j1:j2]))
    return equals


def get_urli(urli):
    """ load a reseource from url

    :param urli:
    :return:
    """
    uresource = urlopen(urli)
    return uresource.read()

def tallennatiedostoUTF8(tiednimi, sisalto):
    with open(tiednimi, 'w', encoding='utf-8') as f_out:
        f_out.write(sisalto)


def tallennatiedosto(tiednimi, sisalto):
    """ Save a File

    :param tiednimi:
    :param sisalto:
    :return:
    """
    fil = open(tiednimi, 'w')
    fil.write(sisalto)
    fil.close()

def saveFileAsUtf8(tiednimi, sisalto):
    tallennatiedostoUTF8(tiednimi, sisalto)

def tallennatiedostoUTF8(tiednimi, sisalto):
    """ Save a File

    :param tiednimi:
    :param sisalto:
    :return:
    """
    fil = open(tiednimi, 'w',encoding='utf-8')
    fil.write(sisalto)
    fil.close()


def tallennatiedostoCp437(tiednimi, sisalto):
    """ Save a File

    :param tiednimi:
    :param sisalto:
    :return:
    """
    fil = open(tiednimi, 'w',encoding='cp437')
    fil.write(sisalto)
    fil.close()


def tallennatiedosto_append(tiednimi,sisalto):
    f = open(tiednimi, 'a')
    f.write(sisalto)
    f.close()

def lataa_tied(tiednimi):
    """ Load a file
    :param tiednimi:
    :return:
    """
    readfil = open(tiednimi, 'r')
    html_doc = readfil.read()
    readfil.close()
    return html_doc

def lataa_tiedUtf(tiednimi):
    """ Load a file
    :param tiednimi:
    :return:
    """
    readfil = open(tiednimi, 'r', encoding="utf8")
    html_doc = readfil.read()
    readfil.close()
    return html_doc


def lataa_tiedcp437(tiednimi):
    """ Load a file
    :param tiednimi:
    :return:
    """
    readfil = open(tiednimi, 'r', encoding="cp437" )
    html_doc = readfil.read()
    readfil.close()
    return html_doc


def listojen_erot(list1, list2):
    """ set operation: get the differences of two lists

    :param list1:
    :param list2:
    :return:
    """
    return list(set(list1) - set(list2))


def listojen_leikkaus(list1, list2):
    """ intersection of two lists as sets

    :param list1:
    :param list2:
    :return:
    """
    return list(set(list1) & set(list2))


def filter_dups2(lista):
    """ filter duplicates from a list
    returns unique members in origial order

    :param lista:
    :return:
    """
    list_uniq = []
    for list_item in lista:
        if list_item not in list_uniq:
            list_uniq.append(list_item)
    return list_uniq

def filter_dups(lista):
    uniqlistHash={}
    uniqlist= []
    for list_item in lista:
        if list_item not in uniqlistHash:
            uniqlistHash[list_item] = True
            uniqlist.append(list_item)

    return uniqlist

def histogram(list_arr):
    """ Create a histogram

    :param list_arr:
    :return:
    """
    hashi = dict()
    for limtem in list_arr:
        if limtem not in hashi:
            hashi[limtem] = 1
        else:
            hashi[limtem] += 1
    return hashi


def order_histo(histo):
    """ Convert histogram hash to list and sort it
    :param histo:
    :return:
    """
    histoar = [[histo[key1], key1] for key1 in histo.keys()]
    histoar.sort()
    return histoar


def ordered_histo(list_arr):
    """
    create ordered histogram list
    :param list_arr:
    :return:
    """
    return order_histo(histogram(list_arr))


def formatedTimestampFromNow():
    return   "{0:%d%m%Y-%H%M%S}".format(datetime.now())


def formatedTimestampFromDate(dt):
    return   "{0:%d%m%Y-%H%M%S}".format(dt)

def formatedDateFromDate(dt):
    return   "{0:%d.%m.%Y %H:%M:%S}".format(dt)




#create_checksum
#  O'reilly Python for Unix and Linux System Administration example code: data\code\checksum.py
def create_md5checksum(path):
        """
        Reads in file.  Creates checksum of file line by line.
        Returns complete checksum total for file.

        """
        fp = open(path ,'rb')
        checksum = hashlib.md5()
        while True:
            buffer = fp.read(8192)
            if not buffer:break
            checksum.update(buffer)
        fp.close()
        checksum = checksum.digest()
        return checksum



def powshcomd(cmd):
   pspath=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
   response=subprocess.check_output([pspath, cmd], shell=True)
   return response


#https://stackoverflow.com/a/3431835
def hash_bytestr_iter(bytesiter, hasher, ashexstr=False):
    for block in bytesiter:
        hasher.update(block)
    return (hasher.hexdigest() if ashexstr else hasher.digest())

def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)

def create_checksum(fname):
    return hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')), hashlib.sha256())


def powshcomd(cmd):
    pspath=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
    response=subprocess.check_output([pspath, cmd], shell=True)
    return response


def pairList2Dict(lista):
    dicti={}
    for eka,toka in lista:
        dicti[eka]=toka
    return dicti

def pairList2DictDupKeys(lista):
    dicti={}
    for eka,toka in lista:
        if eka not in dicti:
            dicti[eka]=[]
        dicti[eka].append(toka)
    return dicti

def pairList2DictBoth(lista):
    dicti={}
    dicti2={}
    for eka,toka in lista:
        dicti[eka]=toka
        dicti2[toka]=eka
    return dicti, dicti2


def listindexoflist(lista, indx):
    return [row[indx] for row in lista]

def listindexRangeoflist(lista, indx1,indx2):
    return [row[indx1:indx2] for row in lista]

def loadFileList(fileList):
    return lataaFilLista(fileList)

def loadFileListUtf8(fileList):
    return lataaFilListaUTF8(fileList)

def lataaFilLista(lista):
    filconts=[]
    for fil in lista:
        filconts.append( (fil,lataa_tied(fil)))
    return filconts

def lataaFilListaUTF8(lista):
    filconts=[]
    for fil in lista:
        filconts.append( (fil,lataa_tiedUtf(fil)))
    return filconts

def lataaFilLista437(lista):
    filconts=[]
    for fil in lista:
        filconts.append( (fil,lataa_tiedcp437(fil)))
    return filconts

def zeroPadNum(num,padlen):
    if len(str(num)) < padlen:
        return "0"*(padlen-len(str(num))) + str(num)
    else:
        return str(num)


#https://ericscrivner.me/2015/07/python-tip-convert-xml-tree-to-a-dictionary/
def make_dict_from_tree(element_tree):
    """Traverse the given XML element tree to convert it into a dictionary.

    :param element_tree: An XML element tree
    :type element_tree: xml.etree.ElementTree
    :rtype: dict
    """
    def internal_iter(tree, accum):
        """Recursively iterate through the elements of the tree accumulating
        a dictionary result.

        :param tree: The XML element tree
        :type tree: xml.etree.ElementTree
        :param accum: Dictionary into which data is accumulated
        :type accum: dict
        :rtype: dict
        """
        if tree is None:
            return accum
        if tree.getchildren():
            accum[tree.tag] = {}
            for each in tree.getchildren():
                result = internal_iter(each, {})
                if each.tag in accum[tree.tag]:
                    if not isinstance(accum[tree.tag][each.tag], list):
                        accum[tree.tag][each.tag] = [
                            accum[tree.tag][each.tag]
                        ]
                    accum[tree.tag][each.tag].append(result[each.tag])
                else:
                    accum[tree.tag].update(result)
        else:
            accum[tree.tag] = tree.text
        return accum
    return internal_iter(element_tree, {})


def deep_chain_from_iterable(it, n):
    if n == 0:
        return list(it)
    else:
        return deep_chain_from_iterable(itertools.chain.from_iterable(it),n-1)

def flattenList(lista):
    return deep_chain_from_iterable(lista, 1)



def getAllKeysFromListOfDicts(dicts):
    allattrsskeys = [attrs.keys() for attrs in dicts]
    return allattrsskeys



#https://ericscrivner.me/2015/07/python-tip-convert-xml-tree-to-a-dictionary/
def make_dict_from_treeStripNS(element_tree, ns):
    """Traverse the given XML element tree to convert it into a dictionary.

    :param element_tree: An XML element tree
    :type element_tree: xml.etree.ElementTree
    :rtype: dict
    """
    def internal_iter(tree, accum):
        """Recursively iterate through the elements of the tree accumulating
        a dictionary result.

        :param tree: The XML element tree
        :type tree: xml.etree.ElementTree
        :param accum: Dictionary into which data is accumulated
        :type accum: dict
        :rtype: dict
        """
        if tree is None:
            return accum
        if tree.getchildren():
            accum[tree.tag] = {}
            for each in tree.getchildren():
                result = internal_iter(each, {})
                if each.tag in accum[tree.tag]:
                    if not isinstance(accum[tree.tag][each.tag], list):
                        accum[tree.tag][each.tag] = [
                            accum[tree.tag][each.tag]
                        ]
                    accum[tree.tag][each.tag].append(result[each.tag])
                else:
                    accum[tree.tag].update(result)
        else:
            accum[tree.tag] = tree.text
        return accum
    return internal_iter(element_tree, {})


#https://ericscrivner.me/2015/07/python-tip-convert-xml-tree-to-a-dictionary/
def make_dict_from_treeStripNS(element_tree, ns):
    """Traverse the given XML element tree to convert it into a dictionary.

    :param element_tree: An XML element tree
    :type element_tree: xml.etree.ElementTree
    :rtype: dict
    """
    def internal_iter(tree, accum):
        """Recursively iterate through the elements of the tree accumulating
        a dictionary result.

        :param tree: The XML element tree
        :type tree: xml.etree.ElementTree
        :param accum: Dictionary into which data is accumulated
        :type accum: dict
        :rtype: dict
        """
        if tree is None:
            return accum
        treetag = tree.tag.replace(ns, "")
        if tree.getchildren():

            accum[treetag] = {}
            for each in tree.getchildren():
                result = internal_iter(each, {})
                eachtag = each.tag.replace(ns,"")
                if eachtag in accum[treetag]:
                    if not isinstance(accum[treetag][eachtag], list):
                        accum[treetag][eachtag] = [
                            accum[treetag][eachtag]
                        ]
                    accum[treetag][eachtag].append(result[eachtag])
                else:
                    accum[treetag].update(result)
        else:
            accum[treetag] = tree.text
        return accum
    return internal_iter(element_tree, {})


def pairList2DictDupKeys(lista):
    dicti={}
    for eka,toka in lista:
        if eka not in dicti:
            dicti[eka]=[]
        dicti[eka].append(toka)
    return dicti

try:
    import StringIO
    # For Python 2

    def tallennaZipattu(zipfilename, filname, str1, zip64=False):
        buff = StringIO.StringIO()
        zip_archive = zipfile.ZipFile(buff, mode='w', allowZip64=zip64)
        tempsisalto = StringIO.StringIO()
        tempsisalto.write(str1)
        zip_archive.writestr(filname, tempsisalto.getvalue())
        zip_archive.close()
        print(zip_archive.printdir())

        with open(zipfilename, 'w') as f:
            f.write(buff.getvalue())


except ImportError:
    pass


def copyListAsConcatenatedString(lista):
    copy_to_clipboard("\n".join([str(row) for row in lista]))



def openExplorerOnCurrentPWD():
    os.system("explorer " + os.getcwd())

def stripEmptyLines(lista):
    return [row for row in lista if row.strip() != '']



def splitlines(str1):
    if  "\r\n" in str1:
        return str1.split("\r\n")
    elif "\n" in str1:
        return str1.split("\n")
    return str1



def splitAndEmptyLines(str1):
    return stripEmptyLines(splitlines(str1))



def pairList2DictBothDupValues(lista):
    dicti={}
    dicti2={}
    for eka,toka in lista:
        if eka not in dicti:
            dicti[eka]=[]
        dicti[eka].append(toka)
        if toka not in dicti2:
            dicti2[toka]=[]
        dicti2[toka].append(eka)

    return dicti, dicti2


def listIndexOfList(lista, indx):
    return [row[indx] for row in lista]


def getFilContsFromFilList(files):

    bookpagefilconts=[]
    for fil in files:
        bookpagefilconts.append( (fil,lataa_tied(fil)))
    return bookpagefilconts

def getFilContsFromFilListUtf(files):

    bookpagefilconts=[]
    for fil in files:
        bookpagefilconts.append( (fil,lataa_tiedUtf(fil)))
    return bookpagefilconts



def getUniwCharsfromString(str1):
    charlist=list(set(list(str1)))
    charlist.sort()
    return "".join(charlist)


def getFirstTagAndClassAttrFromHtml(targetelement):
    tagi, classi = re.findall(r'^<(\w+)[^<>]*?(?:class="(.*?)")?',targetelement)[0]
    return tagi, classi

def getFirstTagAndAttrFromHtml(targetelement):
    tagi, atrname, classi = re.findall(r'^<(\w+)\s+(\w+)="(.*?)"',targetelement)[0]
    return tagi, atrname,classi

def showSizeInGbs(size,numOfDecs=2):
    return decimalPoints(showInGbs(size),numOfDecs)


def decimalPoints(x, numOfDecs):
    return ("%."+str(numOfDecs) + "f") % x

def showInGbs(size):
    return (1.0 * size / 1000000000)

def showInMbs(size):
    return (1.0 * size / 1000000)




def checkDictDiff2(a1, b1,sortAllLists = True):
    diffdata = {}

    def dictDiff2(a1, b1, depth=0, parentKeys=[]):
        type_a = type(a1)
        type_b = type(b1)
        # assert type_a == type_b
        if isinstance(a1, dict):
            a = a1.copy()
        elif isinstance(a1, list) or isinstance(a1, str):
            a = a1[:]
        else:
            a = a1
        if isinstance(b1, dict):
            b = b1.copy()
        elif isinstance(a1, list) or isinstance(a1, str):
            b = b1[:]
        else:
            b = b1

        if type_a != type_b:
            if 'difftype' not in diffdata:
                diffdata['difftype'] = []
            diffdata['difftype'].append((depth, (type_a, type_b, parentKeys)))
            # return (depth, parentKeys,type_a , type_b)

        if isinstance(a, dict):
            if len(a) != len(b):
                if 'diffkeys' not in diffdata:
                    diffdata['diffkeys'] = []
                listojenerotkeys = listojen_erot2(a.keys(), b.keys())
                diffdata['diffkeys'].append((depth, (len(a), len(b)), listojenerotkeys, parentKeys))

            yhteisetkeys = listojen_leikkaus(a.keys(), b.keys())
            depth += 1

            for key in yhteisetkeys:
                parentKeys2 = parentKeys[:]
                parentKeys2.append(key)
                dictDiff2(a[key], b[key], depth, parentKeys2)
                # return False

            return len(diffdata) == 0

        elif isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):
                diffdata['difflistLen'] = (depth, (len(a) != len(b)), parentKeys)
            depth += 1
            if sortAllLists:
                a.sort()
                b.sort()
            parentKeys.append(None)
            try:
                yhteisetelementit = listojen_leikkausDictElems(a, b)

                for i in range(len(yhteisetelementit)):
                    dictDiff2(a[i], b[i], depth, parentKeys)
            except (Exception) as e:
                if 'errors' not in diffdata:
                    diffdata['errors'] = []
                diffdata['errors'].append((str(e), parentKeys))
                pituus = len(b)
                if len(a) < len(b):
                    pituus= len(a)

                for i in range(pituus):
                    dictDiff2(a[i], b[i], depth, parentKeys)
        else:
            if a == b:
                return True
            else:
                if 'diffcont' not in diffdata:
                    diffdata['diffcont'] = []
                diffdata['diffcont'].append((depth, (a, b), parentKeys))
                # return False

    dictDiff2(a1, b1)
    return diffdata


def listojen_leikkausDictElems(list1, list2):

    dupmsLeikkaus=list(set([json.dumps(a) for a in list1]) & set([json.dumps(b) for b in list2]))
    return [json.loads(a) for a in dupmsLeikkaus]


def listojen_erot2(list1, list2):
    """ set operation: get the differences of two lists

    :param list1:
    :param list2:
    :return:
    """
    return list(set(list1) - set(list2)),list(set(list2) - set(list1))



def applyToList(lista, func):
    return [func(item) for item in lista ]


def collectSequentialPairs(lista):
    sequentialPairs=[]
    for i, item in enumerate(  lista[:-1]):
        sequentialPairs.append((item, lista[i+1]))
    return sequentialPairs

def isSequential(listOfNums):
    seqpairs=collectSequentialPairs(listOfNums)
    return [( prev, next) for  prev, next in seqpairs if next -prev != 1] == []


def getsegmentedList(nums2,seg_length = 2):
    return [nums2[x:x+seg_length] for x in range(0,len(nums2),seg_length)]

def popFirstIfEmptyStr(arr):
    if arr[0] == '':
        return arr.pop(0)
    return None



def getpairsFromInxsList(loadmethodsindxss):
    pairsFromInxsList=[]
    for i,indx in enumerate(loadmethodsindxss[:-1]):
        pairsFromInxsList.append((indx,loadmethodsindxss[i+1]))
    return pairsFromInxsList



def getdups(list_arr):
    histo1 = ordered_histo(list_arr)
    dups = [item for item in histo1 if item[0] > 1]
    return dups


htmlTemplate= '''<!DOCTYPE html>
  <head>
    <title>testi</title>
    <link rel="shortcut icon" type="image/x-icon" href="./assets/favicon.ico" />
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
  </head>

  <body></body>
</html>'''

def getEpubTitle(xfile ):
    #print( xfile)
    file = zipfile.ZipFile(xfile, "r")
    title = "notfound"
    contentnames = []
    for name in file.namelist():

        if "content.opf" in name or "book.opf" in name:
            # break
            data = file.read(name)
            data =data.decode('utf8')
            # print re.findall(r'<dc:title.*?>(.*?)</dc:title>',data)
            title = re.findall(r'<dc:title.*?>(.*?)</dc:title>', data)[0]

    return title


def getVolWindowsSerial(letter):
    if ":" not in letter:
        letter = letter + ":"
    listaus2 = subprocess.check_output("vol " + letter, shell=True)
    listaus2 = listaus2.decode('ascii')
    return re.findall(r'Volume Serial Number is ([\w\d\-]+)\r', listaus2)[0]





def ejectDrives(readerdrives):
    cmdstr = "$Eject =  New-Object -comObject Shell.Application\n"
    #powshcomd(cmdstr)
    for drl in readerdrives:
        print(drl)

        if not os.path.exists(drl):
            print("skippin " ,drl)
            continue
        drl = drl.replace(":", "")
        cmdstr1 ='$Eject.NameSpace(17).ParseName("' + drl+ ':").InvokeVerb("Eject")' + ";\n"
        cmdstr +=cmdstr1
        #powshcomd(cmdstr1)
    print(cmdstr)
    #copy_to_clipboard(cmdstr)

    os.chdir(r'D:\adm\po\tmp')
    os.getcwd()
    tallennatiedosto("tmpeject.ps1", cmdstr)
    #powshcomd( cmdstr)
    os.system(  r".\tmpeject.ps1")


def createDirs(thumbspath1):
    if not os.path.exists(thumbspath1):
        os.makedirs(thumbspath1)
    assert os.path.exists(thumbspath1)



def totimestamp(dt, kesaaika=False, epoch=datetime(1970, 1, 1)):
    td = dt - epoch
    suomenaikaero = 2
    # return td.total_seconds()
    if kesaaika:
        return (td.microseconds + (td.seconds + td.days * (24) * 3600) * 10 ** 6 - (
                    (suomenaikaero + 1) * 3600 * 10 ** 6)) / 1e6
    else:
        return (td.microseconds + (td.seconds + td.days * (24) * 3600) * 10 ** 6 - (
                    suomenaikaero * 3600 * 10 ** 6)) / 1e6


def listAllFilesrecursive(path1):
    d = diskwalk(path1)
    files = d.enumeratePaths()
    return files


def makeTimeStampedFilPathName(path1,filenameStart, extension):
    timStampNow = formatedTimestampFromNow()
    timStampNow
    filpath = path1 + "\\" + filenameStart + "-" + timStampNow +extension
    return filpath



def getSld(sflpath):

    sld=json.loads(lataa_tied(sflpath))
    return  sld


pspath=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"


def getVolDatasFromGetWmiObjectJson( typpi='3',mounted= [u'C:', u'D:', u'E:',  u'I:', u'J:' ]):

    poshellcmd='Get-WmiObject -Class win32_logicaldisk | ? { $_.driveType -eq ' +str(typpi)+' } | ConvertTo-Json'
    listaus1= subprocess.check_output([pspath, poshellcmd], shell=True)
    explorerwindsjson=json.loads( listaus1.decode("utf8"))

    listaus1[:4]
    len(explorerwindsjson)
    explorerwindsjson

    voldatas2=[]
    for voldata in explorerwindsjson:
        len( voldata.keys())
        voldata
        voldata2={}
        voldata.keys()
        volumeSerialNumber=voldata['VolumeSerialNumber']
        voldata2['VolumeSerialNumber'] = volumeSerialNumber
        volSize=voldata['Size']
        voldata2['Size'] = volSize
        voldata2
        voldata['Path']
        freeSpace = voldata['FreeSpace']

        voldata2['FreeSpace'] = voldata['FreeSpace']
        DeviceID = voldata['DeviceID']
        volumeName = voldata['VolumeName']
        voldata2['VolumeName'] = volumeName
        volumeSerialNumber,volSize,freeSpace ,DeviceID ,volumeName
        DeviceID
        try:
            winSerNum=getVolWindowsSerial(DeviceID)
            voldata2['WindowsSer'] = winSerNum
        except:
            pass
        if volumeSerialNumber != None:
            voldatas2.append((DeviceID,voldata2))
    voldatas2b = [(dr, data) for dr, data in voldatas2 if dr not in mounted]
    return voldatas2b




def getUsbIdFromDriveLetter(letter):
    usbRootDirFils=os.listdir(letter)
    uidfil = [fil for fil in usbRootDirFils if re.findall(r'^(?:(?:ui?d?)|(?:hd))(\d+)\.txt$', fil) != []]
    uidfil
    if uidfil != []:
        uidfil = uidfil[0]
        uid = re.findall(r'^(?:(?:ui?d?)|(?:hd))(\d+)\.txt$', uidfil)[0]
        uid
        return   uid
    return None



def listConnectedDrives(offset):  #
    ofsetindx = string.ascii_uppercase.index(offset)
    asemat = list(string.ascii_uppercase)[ofsetindx:ofsetindx + 10]
    asemat
    kytketytasemat = []
    for asema in asemat:
        try:
            listaus = os.listdir(asema + ":\\")
            kytketytasemat.append(asema)
            print("connected  ", asema)
        except:
            pass

    return kytketytasemat


def getReaderDrives():
    offset = "F"
    kytketytasemat = listConnectedDrives(offset)

    kytketytasemat

    filelists = []
    for asema in kytketytasemat:
        filelists.append(os.listdir(asema + ':/'))

    filelists2 = []
    for asema in kytketytasemat:
        filelists2.append((asema, os.listdir(asema + ':/')))
    filelists2[0][:9]
    readerdrives = [asm[0] for asm in filelists2 if
                    listojen_leikkaus(
                        ['readerid02.txt', 'Sony_Reader', "Setup Reader for PC.exe", "User_Manual_Touch_Lux_4_FI.pdf"],
                        asm[1]) != []]
    return readerdrives

def getVolSerial(dri):
    diroutput = subprocess.check_output("dir " + dri + ":\\", shell=True)
    diroutput.decode('cp437')
    volsern = re.findall(r"Volume Serial Number is (.*?)\r", diroutput.decode('cp437'))
    if volsern != []:
        volsern = volsern[0]
        return volsern
    else:
        return None



def getReaderTargetDrive(readerdrives=None):
    if readerdrives == None:
        readerdrives = getReaderDrives()
    readerdrives
    targetdri = None
    for dri in readerdrives:
        print(dri + ":\\")
        diroutput = subprocess.check_output("dir " + dri + ":\\", shell=True)
        diroutput.decode('cp437')
        volsern = re.findall(r"Volume Serial Number is (.*?)\r", diroutput.decode('cp437'))
        volsern
        if volsern != []:
            volsern = volsern[0]
        if volsern in ( "6D0F-0018" ,'143B-F0C1'):
            targetdri = dri
    return targetdri


def powshcomd(cmd):
    pspath=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
    response=subprocess.check_output([pspath, cmd], shell=True)
    return response


def ejectDrives(readerdrives):
    cmdstr = "$Eject =  New-Object -comObject Shell.Application\n"
    powshcomd(cmdstr)
    for drl in readerdrives:
        print(drl)
        cmdstr1 ='$Eject.NameSpace(17).ParseName("' + drl+ ':").InvokeVerb("Eject")' + ";\n"
        cmdstr +=cmdstr1
        #powshcomd(cmdstr1)
    print(cmdstr)
    #copy_to_clipboard(cmdstr)

    os.chdir(r'D:\adm\po\tmp')
    os.getcwd()
    tallennatiedosto("tmpeject.ps1", cmdstr)
    #powshcomd( cmdstr)
    os.system(  r" .\tmpeject.ps1")


def lataaFilutf8(fil):
    with open(fil, "rb") as ins:
        filcoB = ins.read()
    return filcoB.decode('utf8')#cp437


def lataaFilcp437(fil):
    with open(fil, "rb") as ins:
        filcoB = ins.read()
    return filcoB.decode('cp437')#cp437


def getAllFilesinDirWithExt(dlpathbase,ext):
    #os.chdir(dlpathbase)
    files=os.listdir(dlpathbase)
    htmlfiles=[fil for fil in files if ext in fil[-len(ext):]]
    return htmlfiles



def tallennatiedostoAppend(tiednimi,sisalto):
    f = open(tiednimi, 'a')
    f.write(sisalto)
    f.close()

def tallennatiedostoUTF8Append(tiednimi, sisalto):
    with open(tiednimi, 'a', encoding='utf-8') as f_out:
        f_out.write(sisalto)

def wslPath2WPath(path):
    uudempi2 = path.replace("/mnt/", "").replace("/", "\\").replace('"', '')
    uudempi2
    uudempi2wpath = re.sub(r'^(\w)\\', r"\1:\\", uudempi2)
    return uudempi2wpath

def winPath2WslPath(path):
    path
    uudempi2 = "/mnt/" +  path[0].lower() + path[1:].replace("\\", "/").replace(':', '')
    return uudempi2

def sortByLastMod(lista):
    tosort= [ (os.path.getmtime(tied), tied) for tied in lista ]
    tosort.sort()
    return [ tied[1] for tied in tosort ]



def newestFileInDir(dir1, filterStr=""):
    filsindir=os.listdir(dir1)
    filsindir=[dir1 + "\\"+ fil for fil in filsindir if os.path.isfile(dir1 + "\\"+ fil) and filterStr in fil]
    filsindir.sort(key=lambda x:os.path.getmtime(x))
    return filsindir[-1]

def ordered_histo2(list_arr):
    """
    create ordered histogram list
    :param list_arr:
    :return:
    """
    return order_histo(histogram(list_arr),True)

def swapPairTupleList(lista):
    assert  filter_dups( [len(item) for item in lista]) == [2]
    return [ (  item[1], item[0] )  for item in lista]



def getAllHtmlFilesinDir(dlpathbase):
    #os.chdir(dlpathbase)
    files=os.listdir(dlpathbase)
    htmlfiles=[fil for fil in files if ".html" in fil[-5:]]
    return htmlfiles

def dropExtensionsFromFileList(files):
    #os.chdir(dlpathbase)

    htmlfiles=[ os.path.splitext(  fil)[0] for fil in files ]
    return htmlfiles



def getLastFileFromDir(path1, filterstr='',lastIndx= 0):
    os.chdir(path1)
    files = os.listdir(path1)
    txtfiles = [fil for fil in files if filterstr in fil]
    txtfiles.sort(key=lambda x: os.path.getmtime(x))
    txtfiles.reverse()
    return txtfiles[lastIndx]

def getParentDirWithDepth(pathstr, maxdepth):
    pathstr, maxdepth
    pathstr
    if '\\' in  pathstr:
        pathexploded= pathstr.split('\\')
    elif '/' in  pathstr:
        pathexploded = pathstr.split('/')

    pathexploded[:maxdepth+1]
    return "\\".join( pathexploded[:maxdepth+1] )



def ejectDrivesCmd(readerdrives):
    cmdstr = "$Eject =  New-Object -comObject Shell.Application\n"
    powshcomd(cmdstr)
    for drl in readerdrives:
        print(drl)
        cmdstr1 = '$Eject.NameSpace(17).ParseName("' + drl + ':").InvokeVerb("Eject")' + ";\n"
        cmdstr += cmdstr1
        # powshcomd(cmdstr1)
    #print(cmdstr)
    #copy_to_clipboard(cmdstr)
    return cmdstr


def getMonthFromStr(monthStr):
    kkhash={}
    kkhash["Mar"]=3
    kkhash["Feb"]=2
    kkhash["Jan"]=1
    kkhash["Dec"]=12
    kkhash["Nov"]=11
    kkhash["Apr"]=4
    kkhash["May"]=5
    kkhash["Jun"]=6
    kkhash["Jul"]=7
    kkhash["Aug"]=8
    kkhash["Sep"]=9
    kkhash["Oct"]=10
    return kkhash[monthStr]


def imgDate(fn):
 "returns the image date from image (if available)\nfrom Orthallelous"
 std_fmt = '%Y:%m:%d %H:%M:%S.%f'
 # for subsecond prec, see doi.org/10.3189/2013JoG12J126 , sect. 2.2, 2.3
 tags = [(36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
         (36868, 37522),  # (DateTimeDigitized, SubsecTimeDigitized)
         (306, 37520), ]  # (DateTime, SubsecTime)
 exif = Image.open(fn)._getexif()

 for t in tags:
     dat = exif.get(t[0])
     sub = exif.get(t[1], 0)

     # PIL.PILLOW_VERSION >= 3.0 returns a tuple
     dat = dat[0] if type(dat) == tuple else dat
     sub = sub[0] if type(sub) == tuple else sub
     if dat != None: break

 if dat == None: return None
 full = '{}.{}'.format(dat, sub)
 T = datetime.strptime(full, std_fmt)
 # T = time.mktime(time.strptime(dat, '%Y:%m:%d %H:%M:%S')) + float('0.%s' % sub)
 return T


def getQueryData(qry1, cnx):
    #print qry1
    cursor = cnx.cursor()
    query = (  qry1 )
    cursor.execute(query )
    dataa=[]
    for (field) in cursor:
        #print  field[0]
        dataa.append(field )
    dataa
    #print(len(dataa))
    return dataa



def getEqualSum(kirjat2tiedosto,    testnimi):
    equals=getStrEquals(kirjat2tiedosto,    testnimi)
    _ , eqStr, eqStr2 =  equals[0]
    eqLenSUm=0
    for _ , eqStr, eqStr2  in   equals:
        if len(eqStr) > 2:
            eqLenSUm += len(eqStr)
    return eqLenSUm


def getLastScreenshot(baseDir):
    now = datetime.now()
    yearMonth = str(now.year) + "-" + str(zeroPadNum(now.month, 2))
    yearMonth
    screenshots = baseDir + "\\" + yearMonth
    screenshots
    os.chdir(screenshots)
    os.getcwd()
    screenshotpics = [f for f in os.listdir(screenshots) if '.png' in f]
    screenshotpics.sort()
    screenshotpics.sort(key=lambda x: os.path.getmtime(x))
    screenshotpics.reverse()
    screenshotpics[:7]
    len(screenshotpics)
    pic = screenshotpics[0]
    return screenshots, pic