from datetime import datetime, date
from django.http import JsonResponse

def validate_task(task, allow_today_only=False):
    """
    Validates a single task.
    Returns JsonResponse(error) if invalid, otherwise returns None.
    """

    required_fields = ["title", "due_date", "importance", "estimated_hours"]

    # Checking for the required fields here
    for field in required_fields:
        if field not in task:
            return JsonResponse(
                {"error": f"Missing required field: {field}", "task": task},
                status=400
            )

    # Validating title type
    if not isinstance(task["title"], str):
        return JsonResponse(
            {"error": "title must be a string", "task": task},
            status=400
        )

    # Validating importance
    try:
        imp = int(task["importance"])
        if imp < 1 or imp > 10:
            return JsonResponse(
                {"error": "Importance must be between 1 and 10", "task": task},
                status=400
            )
    except:
        return JsonResponse(
            {"error": "Importance must be a number", "task": task},
            status=400
        )

    # Validating estimated_hours here
    try:
        hours = float(task["estimated_hours"])
        if hours <= 0:
            return JsonResponse(
                {"error": "Estimated hours must be greater than 0", "task": task},
                status=400
            )
    except:
        return JsonResponse(
            {"error": "Estimated hours must be a number", "task": task},
            status=400
        )

    # Validating dependencies array in this
    if "dependencies" in task:
        if not isinstance(task["dependencies"], list):
            return JsonResponse(
                {"error": "dependencies must be a list", "task": task},
                status=400
            )

    # Checking the date format
    try:
        due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
    except:
        return JsonResponse(
            {"error": "Invalid date format (use YYYY-MM-DD)", "task": task},
            status=400
        )

    # 7. Removing the past dates
    today = date.today()

    if allow_today_only:
        #rejecting the past date
        if due < today:
            return JsonResponse(
                {"error": "Task due_date is in the past", "task": task},
                status=400
            )
    else:
        # analyze_view: reject unrealistic dates (1990 etc)
        if due.year < 2024:
            return JsonResponse(
                {"error": "Due date cannot be in the past or unrealistic", "task": task},
                status=400
            )

    return None  #Finally it is valid
