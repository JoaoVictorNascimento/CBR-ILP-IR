# -*- coding: utf-8 -*-
import os
import sys
import re
import csv
import pandas as pd


def count_verify_void_line(line):
    count = line.count("\n") + line.count(" ")
    return count


def remove_finals_spaces_and_asterisk(line):
    while(line[-1] == " "):
        line = line[:-1]
    
    if(line[-1] == "*"):
        line = line[:-1]

    return line

def wos():
    fileRI = open('RI-x.txt', "r", encoding='ISO-8859-1')
    lines = fileRI.readlines()
    file = open("wos_titles.txt", "w")
    for line in lines:
        file.write('\"' + str(line) + '\"' + " OR ")
    
    file.close()

def write_title_file(titles, name):
    file = open(name, "w")
    for title in titles:
        file.write(str(title) + "\n")
    
    file.close()


def print_list_file(path):
    list_file = os.listdir(str(path))
    
    for file in list_file:
        print(file)


def get_list_file(path):
    list_file = os.listdir(str(path))
    return list_file


def get_articles(path, list_file):
    articles = []
    for article in list_file:
        path_article = "./" + str(path) + str(article)
        art = open(path_article, "r", encoding='ISO-8859-1')
        lines = art.readlines()
        articles.append(lines)
        art.close()

    return articles


def get_titles_articles(articles):
    titles = []
    for article in articles:
        title = []
        for line in article:
            if(len(line) == count_verify_void_line(line)):
                break
            else:
                title.append(line)
        formated_title = ""
        for token_title in title:
            formated_title = formated_title + (remove_finals_spaces_and_asterisk(token_title[:-1]) + " ")
        titles.append(formated_title[:-1])
    
    return titles

def csv_title_and_class(titles_file, titles_articles):
    with open('title_and_class.csv', mode='w', encoding='utf-8', newline='') as csv_file:
        fieldnames = ['title', 'class']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for title_file, title_article in zip(titles_file, titles_articles):
            if(title_article[2] == '-'):
                writer.writerow({'title': title_file, 'class': title_article[:2]})    
            else:
                writer.writerow({'title': title_file, 'class': title_article[:3]})

def found():
    data2 = pd.read_csv("articles_not_found.csv").drop_duplicates(subset=None, keep='first', inplace=False)
    data1 = pd.read_csv("title_and_class.csv").drop_duplicates(subset=None, keep='first', inplace=False)
    merged_left = pd.merge(left=data1,right=data2, 
                            how='left', left_on='title', right_on='title')
    
    data = merged_left[ pd.isnull(merged_left.class_y) ]
    data = data.drop(['class_y'], axis=1)
    data.to_csv('articles_found.csv', index=False)

def get_by_class(clasS):
    file = open('articles_not_found.csv')
    lines = csv.reader(file)
    clas = [] 

    for line in lines:
        if(line[1] == clasS):
            clas.append(line[0])
    
    return clas

def tagIdentifyCiw(list_line):
    tagsCIW = {
        "AU": "%A",	#Authors
        "BE": "%E",	#Editors
        "TI": "%T",	#Document Title
        "LA": "%G", #Language
        "DT": "%0", #Reference Type
        "AB": "%X",	#Abstract
        "PU": "%I",	#Publisher
        "PA": "%C",	#Publisher Address
        "PY": "%D", #Year Published
        "VL": "%V", #Volume
        "DI": "%R", #Digital Object Identifier (DOI)
    }

    referenceType = {
        "Proceedings Paper": "Conference Proceedings",
        "Article": "Journal Article",
    }
    tag = list_line[0][0:2]
        
    if tag in tagsCIW.keys():
        list_newLine = []
        if tag == "AU" or  tag == "BE":
            for line in list_line:
                if(line[0:2] == tag):
                    newLine = tagsCIW[tag] + line[2:]
                else:
                    newLine = tagsCIW[tag] + line[2:]
                list_newLine.append(newLine)
            
            return list_newLine
        
        if tag == "DT":
            newLine = tagsCIW[tag]
            if list_line[0][2:].find('Article') != -1:
                newLine += " " + referenceType['Article']
            else:
                newLine += " " + referenceType['Proceedings Paper'] 
            
            list_newLine.append(newLine + "\n")
            return list_newLine
        else:
            newLine = tagsCIW[tag]
            for line in list_line:
                newLine +=  line[2:].strip("\n")
            
            list_newLine.append(newLine + "\n")
            return list_newLine
    else:
        return None

def convertCIWtoEndNoteAndSaveFolder(folder):
    tagsCIW =["AU","BE","TI","LA","DT","AB","PU","PA","PY","VL","DI"]

    path = "./" + str(folder)
    list_file = get_list_file(path)
    articles = get_articles(str(folder), list_file)
    with open('OutputFile.enw', mode='w', encoding='utf-8', newline='') as file:
        for article in articles:
            list_line = []
            for iterator, line in enumerate(article):
                if(iterator+1 < len(article)):
                    if line[0:2] in tagsCIW or line[0:2] == "  ":
                        list_line.append(line)
                        if article[iterator+1][0:2] != "  ":
                            result = tagIdentifyCiw(list_line)  
                            list_line = []
                            if(result == None):
                                continue
                            else:         
                                for i in result:
                                    file.write(i)
            file.write("\n\n")


def get_dt_ISI(list_title):
    dts = []
    for article in list_title:
        path_article = "./" + "pre-endnote/" + str(article)
        art = open(path_article, "r", encoding='ISO-8859-1')
        lines = art.readlines()
        for line in lines:
            line = line.split()
            if "DT" in line:
                dts.append(line)
        
        art.close()
    
    return dts

def get_0_ISI(list_title):
    dts = []
    for article in list_title:
        path_article = "./" + "Endnote/" + str(article)
        art = open(path_article, "r", encoding='ISO-8859-1')
        lines = art.readlines()
        for line in lines:
            line = line.split()
            if "%0" in line:
                dts.append(line)
        
        art.close()
    
    return dts

def finalOutputFile():
    title_endnote = get_list_file('Endnote/')
    
    with open('OutputFile.enw', mode='a', encoding='utf-8', newline='') as file:
        for title_article in title_endnote:
            path_article = "./" + "Endnote/" + str(title_article)
            art = open(path_article, "r", encoding='ISO-8859-1')
            lines = art.readlines()
            for line in lines:
                file.write(line)
            file.write("\n")
            art.close()
            
def main():
    '''
    Usage: python3 script.py Articles/
    '''
    #path = sys.argv[1]
    # list_file = get_list_file(path)
    # articles = get_articles(path, list_file)
    # title_endnote = get_list_file('Endnote/')
    # write_title_file(title_endnote, "Endnote.txt")
    #riClass = get_by_class('RI')
    #print(len(riClass))
    #list_file = get_list_file("Endnote/")
    #print_list_file("pre-endnote/")
    # pre_endnote = get_list_file('pre-endnote/')
    # Dt = get_dt_ISI(pre_endnote)
    #D3 = get_0_ISI(list_file)
    # for i in Dt:
    #    print(i)
    #for i in D3:
    #    print(i)
    #write_title_file(riClass, "RI-x.txt")
    #      print(i)
    #titles_articles = get_titles_articles(articles)
    #wos()
    #csv_title_and_class(titles_articles, list_file)
    #asd()
    # print(string[2:])
    convertCIWtoEndNoteAndSaveFolder("pre-endnote/")
    #line = tagIdentifyCiw(["AB A Private Information Retrieval (PIR) protocol enables a user to retrieve a data item from a database while hiding the identity of the item being retrieved. In a t-private, k-server PIR protocol the database is replicated among k servers, and the user's privacy is protected from any collusion of up to t servers. The main cost-measure of such protocols is the communication complexity of retrieving a single bit of data.\n", "   This work addresses the information-theoretic setting for PIR, in which the user's privacy should be unconditionally protected from collusions of servers. We present a unified general construction, whose abstract components can be instantiated to yield both old and new families of PIR protocols. A main ingredient in the new protocols is a generalization of a solution by Babai, Kimmel, and Lokam to a communication complexity problem in the so-called simultaneous messages model.\n", '   Our construction strictly improves upon previous constructions and resolves some previous anomalies. In particular, we obtain: (1) t-private k-server PIR protocols with O(n(1/[(2k-1)/t])) communication bits, where n is the database size. For t > 1, this is a substantial asymptotic improvement over the previous state of the art; (2) a constant-factor improvement in the communication complexity of 1-private PIR, providing the first improvement to the 2-server case since PIR protocols were introduced; (3) efficient PIR protocols with logarithmic query length. The latter protocols have applications to the construction of efficient families of locally decodable codes over large alphabets and to PIR protocols with reduced work by the servers.\n'])
    #print(line)
    # string = "Article; Proceedings Paper"
    # find = string.find('Article')
    # print(find)
    finalOutputFile()
    
main()