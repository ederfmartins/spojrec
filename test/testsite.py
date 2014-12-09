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
        
    def test_combo_box(self):
        combo = HtmlElement('select')
        combo.addAttr(Attr('name', "dif"))
        combo.addAttr(Attr('id', "dif"))
        for dificult in ['Fácil', 'Médio', 'Difícil']:
        	item = HtmlElement('item')
        	item.addAttr(Attr('value', dificult))
        	item.addNode(dificult)
        	combo.addNode(item)
        
        self.assertEqual(str(combo), '<select name="dif" id="dif"><item value="Fácil">Fácil</item><item value="Médio">Médio</item><item value="Difícil">Difícil</item></select>')
        
        searchDiv = HtmlElement('div')
        searchDiv.addAttr(Attr('class', "inner"))
        searchDiv.addNode(combo)
        self.assertEqual(str(searchDiv), '<div class="inner"><select name="dif" id="dif"><item value="Fácil">Fácil</item><item value="Médio">Médio</item><item value="Difícil">Difícil</item></select></div>')

if __name__ == '__main__':
    unittest.main()
