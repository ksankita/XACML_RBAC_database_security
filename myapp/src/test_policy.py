import unittest
from .policy_evaluator import PolicyEvaluator

class TestPolicyEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = PolicyEvaluator("../policies/policy.xml")

    def test_manager_access_during_working_hours(self):
        self.assertEqual(self.evaluator.evaluate_request("manager", "office", 10), "Permit")

    def test_employee_access_from_home(self):
        self.assertEqual(self.evaluator.evaluate_request("employee", "home", 14), "Deny")

    def test_employee_access_from_office(self):
        self.assertEqual(self.evaluator.evaluate_request("employee", "office", 14), "Permit")

if __name__ == '__main__':
    unittest.main()
