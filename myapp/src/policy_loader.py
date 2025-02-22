from lxml import etree

class PolicyLoader:
    def __init__(self, policy_file):
        self.policy_file = policy_file
        self.policy_tree = self.load_policy()

    def load_policy(self):
        try:
            with open(self.policy_file, 'r') as file:
                return etree.parse(file)
        except etree.XMLSyntaxError as e:
            print(f"XML Syntax Error: {e}")
        except Exception as e:
            print(f"Error loading policy file: {e}")
        return None

    def get_policy_root(self):
        return self.policy_tree.getroot() if self.policy_tree is not None else None
