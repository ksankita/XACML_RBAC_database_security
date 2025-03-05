from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .src.policy_evaluator import PolicyEvaluator  # Ensure this import is correct

@csrf_exempt  # Disable CSRF for testing purposes (remove this in production)
def evaluate_access(request):
    if request.method == "POST":
        try:
            # Handle both form-encoded and JSON requests
            if request.content_type == "application/json":
                data = json.loads(request.body)  # Parse JSON data
            else:
                data = request.POST  # Handle form data

            role = data.get("role")
            location = data.get("location")
            access_time = data.get("accessTime")

            # Validate input fields
            if not all([role, location, access_time]):
                return JsonResponse({"decision": "Invalid request parameters"}, status=400)

            try:
                access_time = int(access_time)  # Convert to integer
            except ValueError:
                return JsonResponse({"decision": "Invalid access time"}, status=400)

            # Adjust the policy path if needed
            policy_path = "myapp/policies/policy.xml"
            evaluator = PolicyEvaluator(policy_path)
            decision = evaluator.evaluate_request(role, location, access_time)

            return JsonResponse({"decision": decision})

        except json.JSONDecodeError:
            return JsonResponse({"decision": "Invalid JSON format"}, status=400)

        except Exception as e:
            return JsonResponse({"decision": f"Error: {str(e)}"}, status=500)

    return render(request, "index.html")  # Serve the HTML page for GET requests
