#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Brass Currant code name generator. version 1.0.0.0

Usage:
    python brass_currant.py
    for more usage information, python brass_currant.py --help

Copyright (c) 2015 MIYAKE Hikaru

Released under the MIT license
http://opensource.org/licenses/mit-license.php
"""

import os
import random
import argparse
import ConfigParser


class WordBook:
    """
    WordBook class is named word list.
    WordBook instance has words.
    CodeNameGenerator pick up word from WordBook.
    """
    def __init__(self, name, work_book_files_dir):
        """
        init method load named text file, and set line to words array.
        :rtype : WordBook
        """
        self.name = name
        self.work_book_files_dir = work_book_files_dir
        self.path = os.path.join(self.work_book_files_dir, name)
        self.words = []
        for line in open(self.path):
            line = line.replace("\n", "")
            line = line.replace("-", "")
            line = line.strip()
            line = line.title()
            line = line.replace(" ", "")
            self.words.append(line.replace("\n", ""))


class WordBookShelf:
    """
    WordBookShelf class is shelf of WordBook.
    WordBookShelf instance has WordBook instances.
    CodeNameGenerator pick up WordBook instance from WordBookShelf.
    """
    def __init__(self):
        """
        init method walk text file directory, create WordBook instances, and put WordBook instance to self.
        :rtype : WordBookShelf
        """
        self.word_books = []
        self.work_book_files_dir = os.path.join(os.path.dirname(__file__), config.get("settings", "word_books_dir"))
        word_file_names = os.listdir(self.work_book_files_dir)
        for word_file_name in word_file_names:
            self.word_books.append(WordBook(word_file_name, self.work_book_files_dir))


class CodeName:
    """
    CodeName class is CodeNameGenerator's result data.
    CodeName instance has name, full_name, short_name, original_word_book, short_name_length.
    name is generic codename like "BrassCurrent".
    full_name is separated space like "Brass Current". I use this image search key word.
    short_name is shorting name to short_name_length like "BrassCurnt". I use this hostname.
    original_word_book is array of WordBook instance.
    """
    def __init__(self, short_name_length=12):
        """
        init method initialize each values.
        :rtype : CodeName
        :param short_name_length: length of your expected short_name.
        """
        self.name = ""
        self.full_name = ""
        self.short_name = ""
        self.original_word_book = []
        self.short_name_length = short_name_length


class CodeNameGenerator:
    """
    CodeNameGenerator class is code name generator.
    CodeNameGenerator instance generate CodeName.
    """
    @staticmethod
    def is_vowel(value):
        """
        is_vowel method is check value is vowel.
        :rtype : bool
        """
        return value in ["a", "e", "i", "o", "u"]

    def __init__(self, short_name_length=12, word_book_names=None):
        """
        init method prepare CodeGenerator's work space.
        """
        self.word_book_shelf = WordBookShelf()
        self.code_name = CodeName()
        self.code_name.short_name_length = short_name_length
        if word_book_names is None:
            word_book_names = ["colors", "fruits"]
        self.word_book_names = word_book_names
        self.word_books = []

    def generate(self):
        """
        generate method select WordBook instances from WordBookShelf instance,
        choice word from WordBook instances, and create CodeName.
        """
        self.select_word_books()
        for word_book in self.word_books:
            self.code_name.full_name += random.choice(word_book.words) + " "
            self.code_name.original_word_book.append(word_book)
        self.code_name.full_name.strip()
        self.code_name.name = self.code_name.full_name.replace(" ", "")
        self.shorting_code_name()
        return self.code_name

    def select_word_books(self):
        """
        select_word_book method select WordBook instances from WordBookShelf instance.
        """
        for word_book_name in self.word_book_names:
            for word_book in self.word_book_shelf.word_books:
                if word_book.name == word_book_name:
                    self.word_books.append(word_book)
                    self.word_book_shelf.word_books.remove(word_book)

    def shorting_code_name(self):
        """
        shorting_code_name method remove character from codename until short_name length to short_name_length.
        The character for removal is selected random. But, it is not upper character, and is not non vowel character.
        Because, if short name of "Brass Current" is "assuen", it has not meaning of original code name.
        However, all shorting name characters are non vowel character, since there is no way,
        generator remove non vowel character. Similarly, generator remove upper case character.

        """
        short_name = self.code_name.name
        short_name_length = self.code_name.short_name_length
        while len(short_name) != short_name_length:
            i = random.randint(0, len(short_name) - 1)
            if self.is_vowel(short_name[i]) \
                    and not short_name[i].isupper() \
                    or all(not self.is_vowel(value) for value in short_name) \
                    and not short_name[i].isupper() \
                    or all(not value.isupper() for value in short_name):
                if len(short_name) > short_name_length:
                    short_name = short_name[0:i] + short_name[i + 1:]
                else:
                    short_name = short_name[0:i] + short_name[i] * 2 + short_name[i + 1:]
        self.code_name.short_name = short_name


config = ConfigParser.SafeConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))


def initialize_argument_parser():
    """
    initialize_argument_parser method initialize argument parser.
    :return: argument_parser
    """
    argument_parser = argparse.ArgumentParser(description="Blass Currant code name generator.")
    argument_parser.add_argument("-v", "--version", action="version",
                                 version="Blass Currant code name generator 1.0.0.0")
    argument_parser.add_argument("-l", "--short-name-length", action="store", nargs="?", const=None, default=12,
                                 type=int, choices=None, help="set length of short name. (default: 12)", metavar=None)
    argument_parser.add_argument("-w", "--word-books", action="store", nargs="*", const=None,
                                 default=["colors", "fruits"], type=str, choices=None,
                                 help="set word books (default: colors fruits)", metavar=None)
    return argument_parser

if __name__ == "__main__":
    parser = initialize_argument_parser()
    args = parser.parse_args()
    generator = CodeNameGenerator(args.short_name_length, args.word_books)
    codename = generator.generate()
    print("Full name: %s, Name: %s, Short name: %s" % (codename.full_name, codename.name, codename.short_name))
