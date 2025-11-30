# Smart Task Analyzer

- A backend system built using **Django** that intelligently ranks and recommends tasks based on urgency, importance, effort, dependencies, and optional user custom priority.

- Hepls user decide what to work on first

- It exposes two main endpoints:

- **/analyze** → Returns all tasks sorted by priority score
- **/suggest** → Returns top 3 tasks that must be completed today

---

## Features

- I have **modified** the scoring algorithm given by you to achieve more **specificity** and **details**

- Smart weighted scoring algorithm
- Handles:
  - Urgency (due date)
  - Importance
  - Estimated effort
  - Custom priority
  - Task dependencies
- Validates input JSON and dates
- Frontend can plug in sorting strategies
- No database required (in-memory only)
- Designed exactly per company requirements

---

# Why No Database Is Used in this Project

```
- The assignment focuses on analyzing tasks received from the client, running the scoring algorithm, and returning prioritized results.
- Persisting tasks was not required for the algorithm to work, so a database layer would add extra complexity without contributing to the accuracy or functionality.
- he project structure is still modular and ready for future database integration if needed.

```

# 1. How the Algorithm Works

Every task is scored based on priority. Higher score = higher priority.

The scoring considers **5 parameters**:

---

## 1. Urgency (Highest Weight)

Urgency heavily affects priority because deadline-based tasks matter most.

| Situation       | Score |
| --------------- | ----- |
| Overdue         | +120  |
| Due Today       | +70   |
| Due in 1–3 Days | +50   |
| Due in 4–7 Days | +20   |

**Reason:**  
Urgency determines immediate action. If something is overdue or due today, it must be handled first.  
That's why urgency has the highest weight in the scoring formula.

---

## 2. Importance (Medium Weight)

```
importance * 5
```

Importance expresses the significance or impact of the task.

Urgency > Importance but both contribute heavily.

---

## 3. Effort (Low Weight)

Effort gives a slight push to smaller tasks because they are quick wins.

| Effort    | Score |
| --------- | ----- |
| ≤ 1 hour  | +15   |
| ≤ 3 hours | +5    |
| > 3 hours | –5    |

Smaller tasks are easier to finish and improve productivity, so they get a boost.

---

## 4. Custom Priority (Optional)

```
custom_priority * 10
```

Lets users override priority manually if needed.

---

## 5. Dependency Handling

- If dependencies are **pending**, the task gets a penalty:
  ```
  -40
  ```
- If a dependency is **due today**, the task gets a boost:
  ```
  +30
  ```

This ensures:

- You finish prerequisite tasks first
- You don’t start a task without clearing its dependencies

---

# Final Score Formula

```
Final Score =
UrgencyScore
+ (importance * 8)
+ EffortScore
+ (custom_priority * 10)
+ DependencyScore
```

---

# 2. API Endpoints

### **POST /analyze/**

Sorts all tasks by score (highest → lowest).  
Validates all fields and returns cleaned sorted data.

### **POST /suggest/**

Filters tasks due today → computes score → returns **top 3**.

---

# 3. Project Structure

```
task-analyzer/
├── backend/                  # Main Django Project Folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/                    # Your App Folder
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py             # Database structure
│   ├── scoring.py
    |__utils
        |__validators.py             # YOUR CUSTOM ALGORITHM GOES HERE
│   ├── tests.py              # Unit tests
│   ├── urls.py               # App-specific URLs
│   └── views.py              # API Logic
├── frontend/                 # Frontend Files
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── manage.py
├── db.sqlite3
└── requirements.txt


---
```

# How to Run the Project Locally

### 1. Clone the project

```bash
git clone <your-repo-url>
cd project-folder
```

### 2. Create a virtual environment

```bash
python -m venv env
```

Activate it:

Windows:

```bash
env\Scripts\activate
```

Mac/Linux:

```bash
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
python manage.py runserver
```

Server will run on:

```
http://127.0.0.1:8000/
```

---

# 6. CORS Setup

Install:

```bash
pip install django-cors-headers
```

Add to `settings.py`:

```python
INSTALLED_APPS += ["corsheaders"]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    *MIDDLEWARE
]

CORS_ALLOW_ALL_ORIGINS = True
```

---

# 7A. Example Input JSON for /analyze endpoint or for Analyze

```json
[
  {
    "title": "Complete Project Report",
    "due_date": "2025-03-02",
    "importance": 9,
    "estimated_hours": 4,
    "dependencies": []
  },
  {
    "title": "Buy Groceries",
    "due_date": "2025-02-28",
    "importance": 3,
    "estimated_hours": 1,
    "dependencies": []
  },
  {
    "title": "Prepare for Interview",
    "due_date": "2025-03-01",
    "importance": 10,
    "estimated_hours": 3,
    "dependencies": ["Complete Project Report"]
  },
  {
    "title": "Gym Workout",
    "due_date": "2025-02-27",
    "importance": 4,
    "estimated_hours": 1,
    "dependencies": []
  },
  {
    "title": "Pay Electricity Bill",
    "due_date": "2025-02-26",
    "importance": 7,
    "estimated_hours": 0.5,
    "dependencies": []
  }
]
```

# 7B. Example Input JSON for /suggest endpoint or for Suggest

**NOTE** : For suggest endpoint change and keep the present and future dates as it suggests the top 3 tasks for today only. In case of past dates it will show an error message

```json

[
{
"title": "Finish Resume Update",
"due_date": "2025-11-29",
"importance": 9,
"estimated_hours": 2,
"dependencies": []
},
{
"title": "College Assignment Submission",
"due_date": "2025-11-29",
"importance": 7,
"estimated_hours": 3,
"dependencies": []
},
{
"title": "Prepare for Coding Interview",
"due_date": "2025-11-29",
"importance": 10,
"estimated_hours": 4,
"dependencies": ["Finish Resume Update"]
},
{
"title": "Pay Rent",
"due_date": "2025-11-29",
"importance": 8,
"estimated_hours": 1,
"dependencies": []
},
{
"title": "Workout Session",
"due_date": "2025-11-29",
"importance": 6,
"estimated_hours": 1,
"dependencies": []
},
{
"title": "Clean Room",
"due_date": "2025-11-29",
"importance": 5,
"estimated_hours": 1,
"dependencies": []
},
{
"title": "Prepare Breakfast",
"due_date": "2025-11-29",
"importance": 4,
"estimated_hours": 0.5,
"dependencies": []
},

{
"title": "Start Portfolio Redesign",
"due_date": "2025-12-01",
"importance": 8,
"estimated_hours": 5,
"dependencies": []
},
{
"title": "Doctor Appointment",
"due_date": "2025-12-02",
"importance": 9,
"estimated_hours": 1,
"dependencies": []
},
{
"title": "Shopping for Friend’s Birthday",
"due_date": "2025-12-05",
"importance": 4,
"estimated_hours": 2,
"dependencies": []
},
{
"title": "Submit Project Report",
"due_date": "2025-12-03",
"importance": 10,
"estimated_hours": 6,
"dependencies": []
},
{
"title": "Start Learning Docker",
"due_date": "2025-12-04",
"importance": 6,
"estimated_hours": 3,
"dependencies": []
},
{
"title": "Plan New Year Trip",
"due_date": "2025-12-15",
"importance": 5,
"estimated_hours": 2,
"dependencies": []
},
{
"title": "Bank Account Update",
"due_date": "2025-12-06",
"importance": 7,
"estimated_hours": 1,
"dependencies": []
}
]

---
```

# 8. Author

**Shivakrishna Rasoju**
Full Stack Developer | Django | REST API
Interested in Software Engineering opportunities.

```

```
