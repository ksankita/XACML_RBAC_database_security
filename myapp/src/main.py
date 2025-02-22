from policy_evaluator import PolicyEvaluator
from datetime import datetime

policy_file = "../policies/policy.xml"
evaluator = PolicyEvaluator(policy_file)

role = input("Enter role (manager/employee): ").strip().lower()
location = input("Enter location (office/home): ").strip().lower()
current_hour = datetime.now().hour

decision = evaluator.evaluate_request(role, location, current_hour)
print(f"Access decision: {decision}")
