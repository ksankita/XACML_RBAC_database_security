import datetime
import os
from .policy_evaluator import PolicyEvaluator

def main():
    print("XACML Policy Evaluation")
    role = input("Enter role (e.g., manager, employee): ").strip().lower()
    location = input("Enter location (e.g., office, home): ").strip().lower()

    # Option to use current time
    use_current_time = input("Use current time? (yes/no): ").strip().lower()
    if use_current_time == "yes":
        access_time = datetime.datetime.now().hour
        print(f"Using current time: {access_time}:00")
    else:
        while True:
            try:
                access_time = int(input("Enter access time in 24-hour format (e.g., 14 for 2 PM): "))
                if 0 <= access_time <= 23:
                    break
                else:
                    print("Invalid time. Please enter a value between 0 and 23.")
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 23.")

    # Check if policy file exists
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    policy_path = os.path.join(BASE_DIR, "myapp", "policies", "policy.xml")
    if not os.path.exists(policy_path):
        print(f"Error: Policy file not found at {policy_path}")
        return

    evaluator = PolicyEvaluator(policy_path)
    decision = evaluator.evaluate_request(role, location, access_time)
    
    print(f"Access Decision: {decision}")

if __name__ == "__main__":
    main()
