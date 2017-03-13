'''
Cameron Skaggs
name_finder.py
CSCI 404: Natural Language Processing

'''
import nltk
import re
import requests
from nltk import bigrams
import sys
import numpy as np
from operator import itemgetter

def read_name_file(text):
    with open(text, 'r') as name_file:
        raw =  name_file.read()
    tokens = nltk.word_tokenize(raw)
    tokens = [x for x in tokens if not (x[0].isdigit())]
    return tokens

def read_file(book):
    with open(book, 'r') as bookfile:
        raw = bookfile.read()
    tokens = nltk.word_tokenize(raw)
    return tokens

'''Using the formatting of the Gutenberg standard,
   this functions should return the title of the book'''
def findTitle(tokens):
    title = []
    for i in range(0, len(tokens)):
        #title was found in the text
        if tokens[i] == 'Title' and tokens[i+1] == ":":
            #the next token will be the title
            i += 2
            title.append(tokens[i])
            i += 1
            '''the title may be multiple tokens long,
            the title is over when the author is introduced
            Note: the release comes if the book lacks an author (ie the Bible)'''
            while(tokens[i] != 'Author' and tokens[i] != 'Release'):
                title.append(tokens[i])
                i += 1
            #make the title a string
            stitle = ' '.join(title)
            return stitle

def findNames(tokens, lst, surnames):
    names = []
    for i in range(0,len(tokens)):
        if tokens[i].upper() in lst and tokens[i][0].isupper():
            if tokens[i+1].upper() in surnames and tokens[i+1][0].isupper():
                names.append(tokens[i] + " " + tokens[i+1])
            else:
                names.append(tokens[i])
    return names

def findNames2(tokens, lst, lst2, surnames):
    names = []
    for i in range(0,len(tokens)):
        if tokens[i].upper() in lst and tokens[i][0].isupper() and tokens[i].upper() not in lst2:
            if tokens[i+1].upper() in surnames and tokens[i+1][0].isupper():
                names.append(tokens[i] + " " + tokens[i+1])
            else:
                names.append(tokens[i])
    return names

def freq_names(name_list):
    fdist = nltk.FreqDist(name_list)
    main_chars = []
    for chars in fdist.most_common():
        if chars[1] >= 5:
            main_chars.append(chars)
    new_main_chars = main_chars[:]
    for char in main_chars:
        for char2 in main_chars:
            if char[0] in char2[0] and char[0] != char2[0] and char in new_main_chars and char2 in new_main_chars:
                new_main_chars.append((char2[0], char[1] + char2[1]))
                new_main_chars.remove(char)
                new_main_chars.remove(char2)

    main_chars = sorted(new_main_chars, key=lambda x: x[1])
    main_chars.reverse()
    for char in main_chars:
        print(char[0])

def findSurname(tokens, name, surname, full_names):

    for i in range(0, len(tokens)):
        if tokens[i] == name and tokens[i+1].upper() in surname and tokens[i+1][0].isupper():
            full_names.append(tokens[i] + " " + tokens[i+1])
def main():

    total_male_name_list = read_name_file('male_names.txt')
    total_female_name_list = read_name_file('female_names.txt')
    total_surname_list = read_name_file('surnames.txt')

    for i in range(1, len(sys.argv)):
        tokens = read_file(sys.argv[i])
        title = findTitle(tokens)
        print(title)
        male_names_list = findNames(tokens, total_male_name_list, total_surname_list)
        female_name_list = findNames2(tokens, total_female_name_list, total_male_name_list, total_surname_list)

        freq_names(male_names_list)
        freq_names(female_name_list)

if __name__ == '__main__':
    main()
