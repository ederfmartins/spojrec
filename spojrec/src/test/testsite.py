# -*- coding: utf-8 -*-
import unittest

from webpages.html import Attr, HtmlElement

class TestHtml(unittest.TestCase):
    
    def test_attr(self):
        attr = Attr('teste', 'value')
        self.assertEqual(str(attr), 'teste="value"')
    
    def test_html(self):
        html = HtmlElement('teste')
        self.assertEqual(str(html), '<teste></teste>')
        
        html.addAttr(Attr('teste', 'value'))
        html.addAttr(Attr('tt', 'vv'))
        self.assertEqual(str(html), '<teste teste="value" tt="vv"></teste>')
        
        html1 = HtmlElement('input')
        html.addNode(html1)
        self.assertEqual(str(html), '<teste teste="value" tt="vv"><input></input></teste>')
        
        html2 = HtmlElement('textarea')
        html.addNode(html2)
        self.assertEqual(str(html), '<teste teste="value" tt="vv"><input></input><textarea></textarea></teste>')
        
        html3 = HtmlElement('t')
        html1.addNode(html3)
        self.assertEqual(str(html), '<teste teste="value" tt="vv"><input><t></t></input><textarea></textarea></teste>')