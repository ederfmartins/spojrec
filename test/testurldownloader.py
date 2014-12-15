# -*- coding: utf-8 -*-
import unittest

from urlDownloaderJob import extract_problem_data, extract_submissions_data, extract_user_data
from urlDownloaderJob import follow
from crawler.downloadQueue import DonloadQueue

#DEPRECATED

class TestFollowFunc(unittest.TestCase):
    
    def test_follow(self):
        self.assertTrue(follow('http://br.spoj.com/users/lucklacs/'))
        self.assertTrue(follow('http://br.spoj.com/status/lucklacs/signedlist/'))
        
        self.assertTrue(follow('http://br.spoj.com/problems/BAPOSTAS/'))
        
        self.assertTrue(follow('http://br.spoj.com/ranks/BAPOSTAS/start=740'))
        self.assertTrue(follow('http://br.spoj.com/ranks/BAPOSTAS/'))
        self.assertTrue(follow('http://br.spoj.com/problems/seletivas/'))
        
        self.assertFalse(follow('http://br.spoj.com/register'))
        self.assertFalse(follow('http://br.spoj.com/status'))
        self.assertFalse(follow('http://br.spoj.com/submit'))
        self.assertFalse(follow('http://br.spoj.com/ranks'))
        self.assertFalse(follow('http://br.spoj.com/embed/info/'))
        self.assertFalse(follow('https://www.spoj.com'))
        self.assertFalse(follow('http://br.spoj.com/status/AERO,lucklacs/'))
        self.assertFalse(follow('http://br.spoj.com/status/,lucklacs/'))
        


class TestExtractors(unittest.TestCase):

    PROBLEM_PAGE = 'http://br.spoj.com/problems/PLACAR/'
    USER_PAGE = 'http://br.spoj.com/users/ederfmartins/'
    SUBMISSIONS_PAGE = 'http://br.spoj.com/status/ederfmartins/signedlist/'
    
    def get_document(self, page):
        queue = DonloadQueue()
        doc = queue.download(page)
        return doc
    
    def run_extract_function(self, url, extractFunc):
        doc = self.get_document(url)
        item = extractFunc(doc, url)
        self.assertEqual(item.url, url)
        return item

    def test_extract_problem_data(self):
        item = self.run_extract_function(self.PROBLEM_PAGE, extract_problem_data)
        self.assertEqual(item.spojId, 'PLACAR')
        self.assertEqual(item.title, '1734. Quem vai ser reprovado')
    
    def test_extract_submissions_data(self):
        item = self.run_extract_function(self.SUBMISSIONS_PAGE, extract_submissions_data)
        self.assertEqual(item.spojId, 'ederfmartins')
        self.assertTrue(len(item.data) > 0)
        
    def test_extract_user_data(self):
        item = self.run_extract_function(self.USER_PAGE, extract_user_data)
        self.assertEqual(item.spojId, 'ederfmartins')
        self.assertEqual(item.name, 'Eder F. M.')
        self.assertEqual(item.country, 'BRAZIL')
        self.assertEqual(item.school, 'UFMG - Universidade Federal de Minas Gerais')
        
        # should raise an exception for an immutable sequence
        #self.assertRaises(TypeError, random.shuffle, (1,2,3))

if __name__ == '__main__':
    unittest.main()
