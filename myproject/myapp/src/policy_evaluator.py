from datetime import datetime
from lxml import etree
from .policy_loader import PolicyLoader    #Loads the XACML policy

class PolicyEvaluator:
    def __init__(self, policy_file):
        self.loader = PolicyLoader(policy_file)
        self.policy_root = self.loader.load_policy()
        self.ns = {'xacml': 'urn:oasis:names:tc:xacml:3.0:core:schema:wd-17'}

    def evaluate_request(self, role, location, access_time):
        print(f"Evaluating Request: role={role}, location={location}, access_time={access_time}")
        
        policy_root = self.policy_root  # Corrected: Access the loaded policy directly
        rules = policy_root.findall('.//{*}Rule')

        for rule in rules:
            rule_id = rule.get("RuleId")
            # print(f"Checking Rule: {rule_id}")

            conditions = rule.find('.//{*}Condition')
            if conditions is None:  # If no conditions, it's a general Permit/Deny rule
                effect = rule.get("Effect")
                # print(f"Rule '{rule_id}' has no conditions, effect: {effect}")
                return effect

            if self.evaluate_conditions(conditions, role, location, access_time):
                effect = rule.get("Effect")
                print(f"Rule '{rule_id}' matched, effect: {effect}")
                return effect
            
        print("No matching rule found. Applying default deny.")
        return "Deny"



    def evaluate_conditions(self, conditions, role, location, access_time):
        role_match = None
        location_match = None
        time_constraints = {"gte": None, "lte": None}

        apply_elements = conditions.findall('.//xacml:Apply', namespaces=self.ns)

        for apply in apply_elements:
            function_id = apply.get("FunctionId")
            result = self.evaluate_apply(function_id, apply, role, location, access_time)

            if function_id == "urn:oasis:names:tc:xacml:1.0:function:string-equal":
                attr_id = apply.find('.//xacml:AttributeDesignator', namespaces=self.ns).get("AttributeId")
                if attr_id == "role":
                    role_match = result
                elif attr_id == "location":
                    location_match = result

            if function_id == "urn:oasis:names:tc:xacml:1.0:function:greater-than-or-equal":
                time_constraints["gte"] = result
            elif function_id == "urn:oasis:names:tc:xacml:1.0:function:less-than-or-equal":
                time_constraints["lte"] = result

        # If the rule is for a manager, role_match is enough
        if role_match is True and location_match is None and time_constraints["gte"] is None and time_constraints["lte"] is None:
            return True

        # If the rule is for an employee, all conditions must be met
        time_match = all(value is True for value in time_constraints.values() if value is not None)
        return all([role_match, location_match, time_match])  # Ensure all conditions are met

    
    def evaluate_apply(self, function_id, apply, role, location, access_time):
        attr_id_elem = apply.find('.//xacml:AttributeDesignator', namespaces=self.ns)
        attr_value_elem = apply.find('.//xacml:AttributeValue', namespaces=self.ns)

        if attr_id_elem is None or attr_value_elem is None:
            return False  # Missing attribute, condition fails

        attr_id = attr_id_elem.get("AttributeId")
        attr_value = attr_value_elem.text

        if function_id == "urn:oasis:names:tc:xacml:1.0:function:string-equal":
            if attr_id == "role":
                return attr_value == role
            elif attr_id == "location":
                return attr_value == location

        
        if function_id == "urn:oasis:names:tc:xacml:1.0:function:greater-than-or-equal":
            return access_time >= int(attr_value)
        
        if function_id == "urn:oasis:names:tc:xacml:1.0:function:less-than-or-equal":
            return access_time <= int(attr_value)
        
        return False