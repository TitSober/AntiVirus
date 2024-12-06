from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import re
import YaraRule


class YaraRule:
    def __init__(self, name, meta, strings, condition):
        self.name = name
        self.meta = meta
        self.strings = strings
        self.condition = condition
    def print_rule(self):
        print(self.name)
        print(self.meta)
        print(self.strings)
        print(self.condition)





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
        condition = self.parse_condition(rule_body)
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

    def parse_condition(self, rule_body):
        condition_block = re.search(r'condition\s*:\s*(.*)', rule_body, re.S)
        return condition_block.group(1).strip() if condition_block else ''


    def get_rules(self):
        return self.rules


class AntivirusScanner:
    def __init__(self, rules):
        self.rules = rules
        self.compile_conditions()  # Pre-compile rule conditions

    def compile_conditions(self):
        for rule in self.rules:
            rule.compiled_condition = self.compile_condition(rule.condition)

    def compile_condition(self, condition):
        eval_condition = condition
        eval_condition = re.sub(r'#(\w+)', lambda m: f"self.string_matches.get('{m.group(1)}', 0)", eval_condition)
        for var in re.findall(r'\$\w+', eval_condition):
            eval_condition = eval_condition.replace(var, f"self.string_matches.get('{var}', False)")
        return eval_condition

    def scan_file(self, file_path):
        with open(file_path, 'rb') as file:
            file_content = file.read()
            matches = []
            for rule in self.rules:
                if self.apply_rule(rule, file_content):
                    matches.append(rule.name)
            return matches

    def apply_rule(self, rule, file_content):
        self.string_matches = defaultdict(int)
        for var_name, pattern in rule.strings.items():
            count = len(re.findall(re.escape(pattern), file_content.decode(errors='ignore')))
            self.string_matches[var_name] = count

        # Evaluate the compiled condition
        try:
            return eval(rule.compiled_condition)
        except Exception as e:
            print(f"Error evaluating condition '{rule.condition}': {e}")
            return False

    def scan_directory(self, directory_path):
        infected_files = {}
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.scan_file, os.path.join(root, file)): file 
                       for root, _, files in os.walk(directory_path) for file in files}
            for future in as_completed(futures):
                file_path = futures[future]
                matches = future.result()
                if matches:
                    infected_files[file_path] = matches
        return infected_files



with open("test.yar","r") as f:
    rule_text = ""
    rule_raw = f.readlines()
    for line in rule_raw:
        rule_text+=line



