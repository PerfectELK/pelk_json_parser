import re

j = '{"lastName": "Doe", "children": [{"firstName": "Alice", "age": 6}, {"firstName": "Bob", "age": 8}], "hobbies": ["running", "sky diving", "singing"], "firstName": "Jane", "age": 35}'
js = '{ "kek" : [ "eee" , "kkk" , "eeee" , 1234 , {"firstName": "Alice"} ]}'

class PelkJson():

    def search__object(self, s=''):
        matches = re.findall(r"([\w]+)\"[\s]{0,}:[\s]{0,}({[\w\":,{}\s]+?})", s)
        if len(matches):
             d = {key: self.parse(val) for key, val in matches}
             return d
        return {}

    def search__list(self, s=''):
        matches = re.findall(r"([\w]+)\"[\s]{0,}:[\s]{0,}(\[[\w\":,{}\s]+?\])", s)
        if len(matches):
            d = {}
            for key, val in matches:
                vv = re.sub(r"({[\w\":,{}\s]+?})", '', val)
                str__list = re.findall(r"\"([\w\s]+)\"", vv)
                num__list = re.findall(r"([\d]+)", vv)
                obj__list = re.findall(r"({[\w\":,{}\s]+?})", val)
                objects = []
                if len(obj__list):
                    objects = [self.parse(o) for o in obj__list]
                d[key] = str__list + num__list + objects
            return d
        return {}


    def search__string(self, s=''):
        ss = re.sub(r"([\w]+)\"[\s]{0,}:[\s]{0,}({[\w\":,{}\s]+?})", '', s)
        ss = re.sub(r"([\w]+)\"[\s]{0,}:[\s]{0,}([[\w\":,{}\s]+?])", '', ss)
        matches = re.findall(r'\"([\w]+?)\"[\s]{0,}:[\s]{0,}\"([\s\w]+)\"', ss)
        if len(matches):
            d = {key: val for key, val in matches}
            return d
        return {}

    def search__number(self, s=''):
        ss = re.sub(r"([\w]+)\"[\s]{0,}:[\s]{0,}({[\w\":,{}\s]+?})", '', s)
        ss = re.sub(r"([\w]+)\"[\s]{0,}:[\s]{0,}({[\w\":,{}\s]+?})", '', ss)
        matches = re.findall(r'\"([\w]+?)\"[\s]{0,}:[\s]{0,}([\d]+)', ss)
        if len(matches):
            d = {key: val for key, val in matches}
            return d
        return {}

    def parse(self, str='{}'):
        nums = self.search__number(str)
        words = self.search__string(str)
        obj = self.search__object(str)
        list = self.search__list(str)
        obj.update(words)
        obj.update(nums)
        obj.update(list)
        return obj


jso = PelkJson().parse(str=j)