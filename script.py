# -*- coding: utf-8 -*-
import os
import sys
import re


def count_verify_void_line(line):
    count = line.count("\n") + line.count(" ")
    return count


def remove_finals_spaces_and_asterisk(line):
    while(line[-1] == " "):
        line = line[:-1]
    
    if(line[-1] == "*"):
        line = line[:-1]

    return line


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


def main():
    path = sys.argv[1]
    list_file = get_list_file(path)
    articles = get_articles(path, list_file)
    titles_articles = get_titles_articles(articles)
    write_title_file(titles_articles)
    
main()