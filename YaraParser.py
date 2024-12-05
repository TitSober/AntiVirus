import base64
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import re
import YaraRule


    
class YaraParser: #parses rules into metadata, strings and conditions
    def __init__(self, rule_text):
        self.rules = []
        self.parse_rules(rule_text)
    def split2(self,string, delim):
        split_parts = string.split(delim)
        cleaned_string = ''.join(split_parts)
        return cleaned_string
    def parse_rules(self,rule_text):
        #splitting the text over the rules strings and condition
        rule_name,rule_body = rule_text.split("{")
        rule_name = rule_name[:-1].split(" ")[1]
        rule_body = rule_body[:-1]
        meta = self.parse_meta(rule_body)
        strings = self.parse_strings(rule_body)
        condition = self.parse_condition(rule_body,strings)
        self.rules.append(YaraRule(rule_name, meta, strings, condition))

   
    def parse_meta(self, rule_body):
        meta_block = re.search(r'meta\s*:\s*(.*?)strings\s*:', rule_body, re.S) #Dobimo ven celoten meta 
        meta = {} 
        if meta_block:#če je bil match
            meta_lines = meta_block.group(1).strip().splitlines()#prvi group od matcha strippamo vseh whitespacov in ga splittamo po vrsticah
            for line in meta_lines:
                if not re.match(r'^\s*//.*', line):
                    key, value = line.split('=', 1) #splitamo metapodatke
                    meta[key.strip()] = value.strip().strip('"') #sfriziramo podatke za shranitev v slovar
        return meta

    def parse_strings(self, rule_body):
        strings_block = re.search(r'strings\s*:([\s\S]*?)(?=\n\s*condition:)*:', rule_body, re.S) #matchamo vse stringe 
        #print(strings_block.group(1))
        strings = {}
        if strings_block:
            string_lines = strings_block.group(1).strip().splitlines()
            string_lines = string_lines[:-1]
            for line in string_lines:
                if not re.match(r'^\s*//.*', line):
                    key, value = line.split('=', 1)
                    strings[key.strip()] = value.strip().strip('"').strip('{}')
                    strings[key.strip()] = self.split2(strings[key.strip()], '"')
        return strings

    def parse_condition(self, rule_body,strings):
        condition_block = re.search(r'condition\s*:\s*(.*)', rule_body, re.S)
        temp = condition_block.group(1).strip().split("}")[0] if condition_block else ''
        if "any of them" in temp:
            tempString = " or ".join(strings.keys())
            temp = temp.replace("any of them", tempString)
        elif "all of them" in temp:
            tempString = " and ".join(strings.keys())
            temp = temp.replace("all of them", tempString)

        return temp


    def get_rules(self):
        return self.rules






class YaraLoader: #loads yara files from directory
    def __init__(self, rule_path):
        self.rule_path = rule_path

    def load_rules(self):
        rules = []
        for root, _, files in os.walk(self.rule_path):
            for file in files:
                if file.endswith('.yar') or file.endswith('.yara'):
                    with open(os.path.join(root, file), 'r') as f:
                        rules.extend(self._parse_rules(f.read()))
        return rules

    def _parse_rules(self, rule_text):
        parser = YaraParser(rule_text)
        return parser.get_rules()
