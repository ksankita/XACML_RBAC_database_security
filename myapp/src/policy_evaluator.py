from datetime import datetime
from lxml import etree
from policy_loader import PolicyLoader

class PolicyEvaluator:
    def __init__(self, policy_file):
        self.loader = PolicyLoader(policy_file)
        self.policy_root = self.loader.get_policy_root()
        self.ns = {'xacml': 'urn:oasis:names:tc:xacml:3.0:core:schema:wd-17'}  # Define namespace

    def evaluate_request(self, role, location, access_time):
        if self.policy_root is None:
            return "Error: Policy not loaded."

        for rule in self.policy_root.findall('.//xacml:Rule', namespaces=self.ns):
            rule_id = rule.get('RuleId')
            effect = rule.get('Effect')

            conditions = rule.findall('.//xacml:Condition', namespaces=self.ns)

            if not conditions:
                return effect  # Permit or Deny based on the rule's effect

            for condition in conditions:
                apply_elements = condition.findall('.//xacml:Apply', namespaces=self.ns)

                for apply in apply_elements:
                    function_id = apply.get("FunctionId")

                    # Evaluate role condition
                    if function_id == "urn:oasis:names:tc:xacml:1.0:function:string-equal":
                        attr_id_elem = apply.find('.//xacml:AttributeDesignator', namespaces=self.ns)
                        attr_value_elem = apply.find('.//xacml:AttributeValue', namespaces=self.ns)

                        if attr_id_elem is not None and attr_value_elem is not None:
                            attr_id = attr_id_elem.get("AttributeId")
                            attr_value = attr_value_elem.text

                            if attr_id == "role" and attr_value != role:
                                return "Deny"
                            if attr_id == "location" and attr_value != location:
                                return "Deny"

                    # Evaluate time condition
                    if function_id == "urn:oasis:names:tc:xacml:1.0:function:greater-than-or-equal":
                        min_time = int(apply.find('.//xacml:AttributeValue', namespaces=self.ns).text)
                        if access_time < min_time:
                            return "Deny"

                    if function_id == "urn:oasis:names:tc:xacml:1.0:function:less-than-or-equal":
                        max_time = int(apply.find('.//xacml:AttributeValue', namespaces=self.ns).text)
                        if access_time > max_time:
                            return "Deny"

                return effect  # Permit or Deny based on the rule's effect

        return "Deny"  # Default deny
