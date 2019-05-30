import re
import time
import json

j = '{ "lastName" : "Doe" , "children": [{"firstName": "Alice", "age": 6}, {"firstName": "Bob", "age": 8}], "hobbies": ["running", "sky diving", "singing"], "firstName": "Jane", "age": 35}'
js = '{ "kek" : [ "eee" , "kkk" , "eeee" , 1234 , {"firstName": "Alice"} ]}'
jjj = '{ "age": 35, "name" : "Всян", "isAdmin": false, "friends": [0,1,2,3] }'

class PelkJson():

    def search__object(self, s=''):
        matches = re.findall(r"([\w]+)\"[\s]{0,}:[\s]{0,}({[\w\":,{}\s]+?})", s, re.MULTILINE)
        if len(matches):
             d = {key: self.parse(val) for key, val in matches}
             return d
        return {}

    def search__list(self, s=''):
        matches = re.findall(r"([\w]+)\"[\s]{0,}:[\s]{0,}(\[[\w\":,{}\s]+?\])", s, re.MULTILINE)
        if len(matches):
            d = {}
            for key, val in matches:
                vv = re.sub(r"({[\w\":,{}\s]+?})", '', val)
                str__list = re.findall(r"\"([\w\s]+)\"", vv, re.MULTILINE)
                num__list = re.findall(r"([\d]+)", vv, re.MULTILINE)
                obj__list = re.findall(r"({[\w\":,{}\s]+?})", val, re.MULTILINE)
                objects = []
                if len(obj__list):
                    objects = [self.parse(o) for o in obj__list]
                if(len(num__list)):
                    num__list = [float(num) for num in num__list]
                d[key] = str__list + num__list + objects
            return d
        return {}


    def search__string(self, s=''):
        ss = re.sub(r"([\w\s]+)\"[\s]{0,}:[\s]{0,}({[\w\":,{}\s]+?})", '', s, re.MULTILINE)
        ss = re.sub(r"([\w\s]+)\"[\s]{0,}:[\s]{0,}(\[[\w\":,{}\s]+?\])", '', ss, re.MULTILINE)
        matches = re.findall(r'\"([\w]+?)\"[\s]{0,}:[\s]{0,}\"([\s\w]+)\"', ss, re.MULTILINE)
        if len(matches):
            d = {key: val for key, val in matches}
            return d
        return {}

    def search__number(self, s=''):
        ss = re.sub(r"([\w]+)\"[\s]{0,}:[\s]{0,}({[\w\":,{}\s]+?})", '', s, re.MULTILINE)
        ss = re.sub(r"([\w\s]+)\"[\s]{0,}:[\s]{0,}(\[[\w\":,{}\s]+?\])", '', ss, re.MULTILINE)
        matches = re.findall(r'\"([\w]+?)\"[\s]{0,}:[\s]{0,}([\d]+)', ss, re.MULTILINE)
        if len(matches):
            d = {key: float(val) for key, val in matches}
            return d
        return {}

    def search__boolean(self, s=''):
        ss = re.sub(r"([\w]+)\"[\s]{0,}:[\s]{0,}({[\w\":,{}\s]+?})", '', s, re.MULTILINE)
        ss = re.sub(r"([\w\s]+)\"[\s]{0,}:[\s]{0,}(\[[\w\":,{}\s]+?\])", '', ss, re.MULTILINE)
        matches = re.findall(r'\"([\w]+?)\"[\s]{0,}:[\s]{0,}(false|true)', ss, re.MULTILINE)
        if len(matches):
            d = {key: True if val == 'true' else False for key, val in matches}
            return d
        return {}

    def parse(self, str='{}'):
        obj = self.search__object(str)
        obj.update(self.search__string(str))
        obj.update(self.search__number(str))
        obj.update(self.search__list(str))
        obj.update(self.search__boolean(str))
        return obj


jso = PelkJson().parse(str=j)
print(jso)






