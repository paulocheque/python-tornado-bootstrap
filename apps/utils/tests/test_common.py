# coding: utf-8
import unittest

from ..common import *


class Str2BoolTests(unittest.TestCase):
    def test_1(self):
        self.assertEquals(False, str2bool(None))
        self.assertEquals(False, str2bool(False))
        self.assertEquals(False, str2bool(''))
        self.assertEquals(False, str2bool('None'))
        self.assertEquals(False, str2bool('none'))
        self.assertEquals(False, str2bool('Null'))
        self.assertEquals(False, str2bool('null'))
        self.assertEquals(False, str2bool('Nil'))
        self.assertEquals(False, str2bool('nil'))
        self.assertEquals(False, str2bool('False'))
        self.assertEquals(False, str2bool('false'))
        self.assertEquals(False, str2bool('F'))
        self.assertEquals(False, str2bool('f'))
        self.assertEquals(False, str2bool('No'))
        self.assertEquals(False, str2bool('no'))
        self.assertEquals(False, str2bool('0'))
        self.assertEquals(True, str2bool(True))
        self.assertEquals(True, str2bool('True'))
        self.assertEquals(True, str2bool('true'))
        self.assertEquals(True, str2bool('1'))
        self.assertEquals(True, str2bool('x'))


class SmartSplitTests(unittest.TestCase):
    def test_1(self):
        self.assertEquals(None, smart_split(None))
        self.assertEquals([], smart_split(''))
        self.assertEquals(['a'], smart_split('a'))
        self.assertEquals(['a'], smart_split(u'a'))
        self.assertEquals(['a'], smart_split(['a']))
        self.assertEquals(['a', 'b'], smart_split('a,b'))
        self.assertEquals(['a', 'b'], smart_split(u'a,b'))
        self.assertEquals(['a', 'b'], smart_split('a,b,'))
        self.assertEquals(['a', 'b'], smart_split(' a , b ,'))
        self.assertEquals(['a', 'b'], smart_split(' a , b , a,b'))
        self.assertEquals(['a', 'A', 'B', 'b'], smart_split(' a , B , A,b'))
        self.assertEquals(['a', 'A', 'B', 'b'], smart_split(' a \n B \n A\r\nb', comma='\n'))


class ToLowerCaseTests(unittest.TestCase):
    def test_1(self):
        self.assertEquals(None, to_lower_case(None))
        self.assertEquals('', to_lower_case(''))
        self.assertEquals('aaa', to_lower_case('aaa'))
        self.assertEquals('aaa', to_lower_case('AAA'))
        self.assertEquals(['a', 'b'], to_lower_case(['A', 'B']))


class TaggifyTests(unittest.TestCase):
    def test_accepts_strings(self):
        self.assertEquals(None, taggify(None))
        self.assertEquals([], taggify(''))
        self.assertEquals(['a'], taggify('a'))
        self.assertEquals(['a'], taggify(u'a'))
        self.assertEquals(['a'], taggify(['a']))
        self.assertEquals(['a', 'b'], taggify('a,b'))
        self.assertEquals(['a', 'b'], taggify(u'a,b'))
        self.assertEquals(['a', 'b'], taggify('a,b,'))
        self.assertEquals(['a', 'b'], taggify(' a , b ,'))
        self.assertEquals(['a', 'b'], taggify(' a , b , a,b'))
        self.assertEquals(['a', 'b'], taggify(' a , B , A,b'))
        self.assertEquals(['a', 'b'], taggify(' a \n B \n A\r\nb', comma='\n'))

    def test_accepts_lists(self):
        self.assertEquals(None, taggify(None))
        self.assertEquals([], taggify(['']))
        self.assertEquals(['a'], taggify(['a']))
        self.assertEquals(['a'], taggify([u'a']))
        self.assertEquals(['a'], taggify(['a']))
        self.assertEquals(['a', 'b'], taggify(['a', 'b']))
        self.assertEquals(['a', 'b'], taggify([u'a', u'b']))
        self.assertEquals(['a', 'b'], taggify([' a ',' b ',' a', 'b']))
        self.assertEquals(['a', 'b'], taggify([' a ',' B ',' A', 'b']))


class CamelCaseTests(unittest.TestCase):
    def test_slugify(self):
        self.assertEquals(None, space_out_camel_case(None))
        self.assertEquals('', space_out_camel_case(''))
        self.assertEquals('a', space_out_camel_case('a'))
        self.assertEquals('A', space_out_camel_case('A'))
        self.assertEquals('Camel Case', space_out_camel_case('CamelCase'))
        self.assertEquals('Camel-Case', space_out_camel_case('CamelCase', join='-'))
        self.assertEquals(u'ç', space_out_camel_case(u'ç'))
        self.assertEquals('ç', space_out_camel_case('ç'))
        self.assertEquals('çáéíóú', space_out_camel_case('çáéíóú'))
        self.assertEquals('Party XXI Tes T', space_out_camel_case('Party XXI TesT'))


class SlugifyTests(unittest.TestCase):
    def test_slugify(self):
        self.assertEquals(None, slugify(None))
        self.assertEquals('', slugify(''))
        self.assertEquals('a', slugify('a'))
        self.assertEquals('a', slugify('A'))
        self.assertEquals('camel-case', slugify('CamelCase'))
        self.assertEquals('c', slugify(u'ç'))
        self.assertEquals('caeiou', slugify('çáéíóú'))
        self.assertEquals('caeiou', slugify('çáÉíÓú'))
        self.assertEquals('party-xxi-tes-t', slugify('Party XXI TesT'))
        self.assertEquals('fea-club-house-party', slugify('FeaClub - HouseParty!'))
        self.assertEquals('bota-dentro-odonto-usp', slugify('BOTA DENTRO Odonto USP'))
        self.assertEquals('sanfriendly-apresenta-tran-slinda-casti', slugify('Sanfriendly apresenta: "TRANSlinda casti'))
        self.assertEquals('xi-ffa-da-rateria', slugify('XI FFA DA RATERIA'))
        self.assertEquals('example-x-with-hyphen', slugify('EXAMPLE X - - With Hyphen'))

    def test_date_slugify(self):
        self.assertEquals(datetime.today().strftime('%Y-%m-%d') + '-camel-case', slugify_with_date('CamelCase'))
