# -*- coding: utf-8 -*-

class Attr(object):
    def __init__(self, attr, value):
        self.attr = attr
        self.value = value
    
    def __repr__(self):
        return self.attr + '="' + self.value + '"'

class HtmlElement(object):
    def __init__(self, tagName):
        self.tagName = tagName
        self.attrs = []
        self.childrem = []
    
    def addAttr(self, attr):
        self.attrs.append(attr)
        return self
    
    def addNode(self, node):
        self.childrem.append(node)
        return self
        
    def __repr__(self):
        start = '<' + self.tagName
        
        for attr in self.attrs:
            start += ' ' + str(attr) 
        
        start += '>'
        end = '</' + self.tagName + '>'
        body = ''.join(str(x) for x in self.childrem)
        return start + body + end
    
