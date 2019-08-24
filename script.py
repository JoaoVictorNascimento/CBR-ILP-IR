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

def wos(titles):
    file = open("wos_titles.txt", "w")
    for title in titles:
        file.write('\"' + str(title) + '\"' + " OR ")
    
    file.close()

def write_title_file(titles):
    file = open("titles.txt", "w")
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

def asd():
    from pathlib import Path
    a = list(Path("Endnote").glob("*"))
    b = [i.name for i in a]
    print(b)
    print(sum(b))

def main():
    path = sys.argv[1]
    list_file = get_list_file(path)
    articles = get_articles(path, list_file)
    # for i in list_file:
    #      print(i)
    titles_articles = get_titles_articles(articles)
    wos(titles_articles)
    csv_title_and_class(titles_articles, list_file)
    asd()
    
main()