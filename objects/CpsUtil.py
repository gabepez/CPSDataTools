# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 10:01:57 2023

@author: gabe
"""

class DataDictonaryElement:
    
    def __init__(self, name, size, description, start, end):
        self.Name = str(name)
        self.Size = int(size)
        self.Description = str(description)
        self.Start = int(start)
        self.End = int(end)
    
    # def __str__(self):
    #     return "DataDictionaryElement: Name=\"{}\"".format(self.Name)
    
    def __str__(self):
        return self.Name

    def __repr__(self):
        return f'DataDictionaryElement: (\'{self.Name}\', {self.Description})'
        
    # def __init__(self):
    #     self.Name = ""
    #     self.Size = 0
    #     self.Description = ""
    #     self.Start = 0
    #     self.End = 0
        
    