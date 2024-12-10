from collections import defaultdict
import os
import re
import YaraRule


class YaraParser:
    def __init__(self, rule_text):
        self.rules = []
        self.parse_rules(rule_text)

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
                key, value = line.split('=', 1)
                strings[key.strip()] = value.strip().strip('"').strip('{}')
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





