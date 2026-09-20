
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Secret key for login sessions
app.secret_key = "devops-task-manager-secret-key"

# Demo login credentials
USERNAME = "admin"
PASSWORD = "admin123"

# Task data
tasks = [
    {"id": 1, "title": "Learn Docker", "completed": False},
    {"id": 2, "title": "Create GitHub repository", "completed": True},
]


# ---------------- LOGIN ----------------

@app.route("/", methods=["GET", "POST"])
def login():

    if "username" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            session["username"] = username
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login"))

    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["completed"])
    pending_tasks = total_tasks - completed_tasks

    if total_tasks > 0:
        progress = round((completed_tasks / total_tasks) * 100)
    else:
        progress = 0

    return render_template(
        "index.html",
        tasks=tasks,
        username=session["username"],
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        progress=progress
    )


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect(url_for("login"))


# ---------------- ADD TASK ----------------

@app.route("/add", methods=["POST"])
def add_task():

    if "username" not in session:
        return redirect(url_for("login"))

    title = request.form.get("title", "").strip()

    if title:

        new_id = max(
            [task["id"] for task in tasks],
            default=0
        ) + 1

        tasks.append({
            "id": new_id,
            "title": title,
            "completed": False
        })

    return redirect(url_for("dashboard"))


# ---------------- COMPLETE TASK ----------------

@app.route("/complete/<int:task_id>")
def complete_task(task_id):

    if "username" not in session:
        return redirect(url_for("login"))

    for task in tasks:

        if task["id"] == task_id:
            task["completed"] = True
            break

    return redirect(url_for("dashboard"))


# ---------------- DELETE TASK ----------------

@app.route("/delete/<int:task_id>")
def delete_task(task_id):

    if "username" not in session:
        return redirect(url_for("login"))

    global tasks

    tasks = [
        task for task in tasks
        if task["id"] != task_id
    ]

    return redirect(url_for("dashboard"))


# ---------------- HEALTH CHECK ----------------

@app.route("/health")
def health():

    return {"status": "healthy"}, 200


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
