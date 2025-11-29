import json

from django.http import JsonResponse,HttpResponse

from datetime import date

from django.views.decorators.csrf import csrf_exempt

from datetime import datetime

from .scoring import calculate_task_score

from tasks.utils.validators import validate_task

@csrf_exempt
def analyze_view(request):
    if request.method != "POST":
        return HttpResponse("Post method required")

    taskList = json.loads(request.body)

    # Validatng the all tasks
    for task in taskList:
        error = validate_task(task, allow_today_only=False)
        if error:
            return error

    # Applying scoring algo
    for task in taskList:
        task["score"] = calculate_task_score(task)

    taskList.sort(key=lambda x: x["score"], reverse=True)

    for task in taskList:
        task.pop("score", None)

    return JsonResponse(taskList, safe=False)



@csrf_exempt
def suggest_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        taskLIst = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    if not isinstance(taskLIst, list):
        return JsonResponse({"error": "Input must be a list of tasks"}, status=400)

    today = date.today()
    todays_tasks = []

    # Validation & filteng of today tasks
    for task in taskLIst:
        error = validate_task(task, allow_today_only=True)
        if error:
            return error

        due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()

        if due == today:
            task["score"] = calculate_task_score(task)
            todays_tasks.append(task)

    if not todays_tasks:
        return JsonResponse({
            "message": "No tasks are due today.",
            "tasks": []
        })

    todays_tasks.sort(key=lambda x: x["score"], reverse=True)

    final_tasks = []
    for task in todays_tasks[:3]:
        task.pop("score", None)
        final_tasks.append(task)

    return JsonResponse({
        "message": "Top 3 tasks to complete today:",
        "tasks": final_tasks
    })
