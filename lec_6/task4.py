"""
Реализовать метод __str__, позволяющий выводить все папки и файлы из данной, например так:
> print(folder1)
V folder1
|-> V folder2
|   |-> V folder3
|   |   |-> file3
|   |-> file2
|-> file1
А так же возможность проверить, находится ли файл или папка в другой папке:
> print(file3 in folder2)
True
"""
import os
import re


class PrintableFolder:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def point(name):
        return re.findall(r'\\.[^\\]*$', name)[0][1:]

    @staticmethod
    def walking(name, walk='', result=[]):
        if os.path.isfile(name):
            result.append(
                ''.join([walk, ' ', PrintableFolder.point(name), '\n']))
        else:
            result.append(
                ''.join([walk, 'V ', PrintableFolder.point(name), '\n']))
            walk = walk[:-2]
            if len(walk) > 0:
                walk += '\t/'
            else:
                walk += '/'
            for i in os.listdir(name):
                PrintableFolder.walking(name+'\\'+i, walk + '->', result)
        return result

    @staticmethod
    def printable(result):
        return ''.join(result)

    def __str__(self):
        return PrintableFolder.printable(PrintableFolder.walking(self.name))

    def __contains__(self, item):
        return item.name.find(self.name) != -1


class PrintableFile:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return re.findall(r'\\.[^\\]*$', self.name)[0][1:]
