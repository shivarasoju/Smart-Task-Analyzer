
from datetime import date, datetime



def calculate_task_score(task_data, all_tasks=None):
    """
    Calculates a weighted priority score for a task.
    Higher score = higher priority.
    Handles:
    - urgency
    - importance
    - effort
    - custom priority
    - dependency urgency & penalty
    """

    score = 0
    today = date.today()


    due_date = task_data.get('due_date')

    if isinstance(due_date, str):
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            return 0  

    days_until_due = (due_date - today).days

    if days_until_due < 0:
        score += 120
    elif days_until_due == 0:
        score += 70
    elif days_until_due <= 3:
        score += 50
    elif days_until_due <= 7:
        score += 20


    importance = task_data.get('importance', 1)
    score += importance * 5
    effort = task_data.get('estimated_hours', 1)

    if effort <= 1:
        score += 15
    elif effort <= 3:
        score += 5
    else:
        score -= 5

    custom_priority = task_data.get('custom_priority', 0)
    score += custom_priority * 10


    deps = task_data.get("dependencies", [])

    if deps and isinstance(deps, list):

        score -= len(deps) * 5
        if all_tasks:
            task_map = {t["title"]: t for t in all_tasks}

            for dep_title in deps:
                dep_task = task_map.get(dep_title)
                if not dep_task:
                    continue 

                
                dep_due = dep_task["due_date"]
                if isinstance(dep_due, str):
                    try:
                        dep_due = datetime.strptime(dep_due, "%Y-%m-%d").date()
                    except:
                        continue

                diff = (dep_due - today).days


                if diff < 0:
                    score += 20   
                elif diff == 0:
                    score += 10    
                elif diff <= 3:
                    score += 5   

    return score
