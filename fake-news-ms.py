import sys
import csv
import string
sys.setrecursionlimit(2500)
'''Filename: fake-news-ms.py
Author: Michael Burman

The purpose of this program is to utilize the merge-sort algorithm to complete the tasks denoted in the fake-news
program, except without the utilization of linked lists.

Which is, the program takes a csv file full of data from news websites, and analyzes article names, then takes only the title
column, and makes a list of each word that occurs in each title, and assigns it a number based on how many times the
word appears in the column, it returns them based on if the count for each word is greater than an
inputted integer N, and if words have the same count, are organized in alphabetical order.'''


class Word:
    def __init__(self, s):
        self._count = 1
        self._word = s

    def word(self):
        '''Getter for the word string.'''
        return self._word

    def count(self):
        '''Getter for the count.'''
        return int(self._count)

    def incr(self):
        '''Increments the word object's count by one.'''
        self._count += 1

    def __str__(self):
        return str(self._word) + " : "  + str(self._count)

def merge(L1, L2, merged):
    '''Pre-condition: takes two split lists of word objects and an empty list.

    Post-condition: After recursively running, returns the, "merged" list as it's the result of the first and second
    lists merged by organizing through count.

    Base case and other code taken from lecture slides.'''
    if L1 == [] or L2 == []:
        return merged + L1 + L2
    else:
        count1 = Word.count(L1[0])
        count2 = Word.count(L2[0])
        word1 = Word.word(L1[0])
        word2 = Word.word(L2[0])
        if count1 > count2:
            new_merged = merged + [L1[0]]
            new_L1 = L1[1:]
            new_L2 = L2
        elif count1 == count2:
            if word1 > word2:
                new_merged = merged + [L2[0]]
                new_L1 = L1
                new_L2 = L2[1:]

            if word2 > word1:
                new_merged = merged + [L1[0]]
                new_L1 = L1[1:]
                new_L2 = L2
        else:
            new_merged = merged + [L2[0]]
            new_L1 = L1
            new_L2 = L2[1:]
        return merge(new_L1, new_L2, new_merged)

def msort(L):
    '''Pre-condition: takes a list of unsorted word objects.

    Post-condition: returns a sorted list of word objects that utilize the merge sort algorithm.
    Merge sort code taken from lecture 13, slide 105.'''
    if len(L) <= 1:
        return L
    else:
        split_pt = len(L)//2
        L1 = L[:split_pt]
        L2 = L[split_pt:]
        sortedL1 = msort(L1)
        sortedL2 = msort(L2)
        return merge(sortedL1, sortedL2, [])

def read_file_data():
    '''CSV reader code taken from csv-example.py.
    Post condition: the csv file is read and returned in a formatted state.
    Code taken from fake-news.py'''
    csv_file_data = []
    csv_file = input("File: ")
    try:
    ##csv_file = "dummy.csv"
        csv_file = open(csv_file)
    except IOError:
        print("ERROR: Could not open file", str(csv_file))
        quit()
    csvreader = csv.reader(csv_file)
    for row in csvreader:
        if str('#') in row[0]:
            continue
        csv_file_data.append(row)

    csv_file.close()
    return csv_file_data

def data_format(csv_data):
    '''Pre-condition: The csv file is in an unformatted list (large amt of data).

    Takes each title and formats it by replacing the punctuation with whitespace, then it splits each title
    into a list of words and removes the appropriately small words. Returns the formatted 2D list.

    Post-condition: The csv file has been formatted and the function returns a new 2D list with
    it data being the data the program needs.
    Code taken from fake-news.py'''
    csv_data_formatted = []
    punctuation = string.punctuation
    for row in csv_data:
        title = row[4]
        for char in punctuation:
            title = title.replace(char, ' ')
        title = title.lower()
        title = title.split()
        title = [word for word in title if len(word) > 2]
        csv_data_formatted.append(title)
    return csv_data_formatted

def data_into_word_objects(csv_data_formtted):
    '''Pre-condition: Takes a 2D list of strings of words.

    Takes the 2D list of strings and converts them into word objects, and if the word object already exists, increments
    its count by one. It organizes these word objects in a python list.

    Post-condition: The 2D list has been formatted and now has each word object in a python list that it returns.'''
    main_list = []
    object_list = []
    for title in csv_data_formtted:
        for item in title:
            if str(item) not in main_list:
                main_list.append(str(item))
                word_obj = Word(item)
                object_list.append(word_obj)
            else:
                for word_obj in object_list:
                    word_obj_str = Word.word(word_obj)
                    if word_obj_str == item:
                        Word.incr(word_obj)
    return object_list

def merge_sort_object_list(object_list):
    '''Pre-condition: takes a list of unsorted word objects.

    This function takes the list of word objects and utilizes the merge-sort sorting algorithm to create a sorted list
    of words sorted by count. Words that share a count are sorted alphabetically.

    Post-condition: Returns a sorted list of word objects.'''
    sorted_object_list = msort(object_list)
    return sorted_object_list

def find_words_with_n(sorted_object_list):
    '''Function that calls the linked list method which finds the word at position N and returns that word object's count
    as integer k, then returns each word in the linked list that has the same count as k. Program ends here.'''
    n = input('N: ')
    try:
        n = int(n)
    except ValueError:
        print("ERROR: Could not read N")
        quit()
    assert (n >= 0)
    k = Word.count(sorted_object_list[n])
    for word in sorted_object_list:
        word_count = Word.count(word)
        if word_count >= k:
            print(str(word))


def main():
    csv_data = read_file_data()
    csv_data_formatted = data_format(csv_data)
    object_list = data_into_word_objects(csv_data_formatted)
    merge_sorted_list = merge_sort_object_list(object_list)
    find_words_with_n(merge_sorted_list)

main()