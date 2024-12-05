import YaraParser
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
