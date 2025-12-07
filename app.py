from flask import Flask, render_template_string

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Study & Task Tracker – Local Only</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- Bootstrap for quick modern UI -->
  <link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
    rel="stylesheet"
  >

  <style>
    body {
      background: #0f172a;
      color: #e5e7eb;
      min-height: 100vh;
    }
    .card {
      background: #020617;
      border-radius: 18px;
      border: 1px solid #1f2937;
    }
    .badge-status {
      font-size: 0.75rem;
      border-radius: 999px;
      padding: 0.25rem 0.6rem;
    }
    .btn-rounded {
      border-radius: 999px;
      font-size: 0.8rem;
      padding-inline: 0.9rem;
    }
    .gradient-title {
      background: linear-gradient(90deg,#38bdf8,#a855f7,#f97316);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .form-control {
      background: #020617;
      border-radius: 999px;
      border: 1px solid #1f2937;
      color: #e5e7eb;
      font-size: 0.9rem;
    }
    .form-control::placeholder {
      color: #6b7280;
    }
    .chip {
      border-radius: 999px;
      border: 1px solid #1f2937;
      padding: 0.3rem 0.7rem;
      font-size: 0.75rem;
      color: #9ca3af;
    }
    a {
      text-decoration: none;
    }
    .list-group-item {
      background: transparent;
      border-color: #1f2937;
    }
  </style>
</head>
<body>
  <div class="container py-4 py-md-5">
    <div class="row justify-content-center">
      <div class="col-lg-10 col-xl-9">

        <!-- Header / stats -->
        <div class="mb-4">
          <div class="d-flex flex-wrap align-items-center justify-content-between gap-3">
            <div>
              <h1 class="h3 fw-bold mb-1 gradient-title">
                📚 Study & Task Tracker
              </h1>
              <p class="text-secondary mb-0" style="font-size:0.9rem;">
                Each device has its <strong>own</strong> tasks. Nothing is shared. Perfect for students.
              </p>
            </div>
            <div class="text-end">
              <div class="chip mb-1" id="today-chip">
                📅 Today:
              </div>
              <div class="d-flex gap-2 justify-content-end flex-wrap" style="font-size:0.8rem;">
                <span class="chip">🧾 Total: <span id="stat-total">0</span></span>
                <span class="chip">✅ Done: <span id="stat-done">0</span></span>
                <span class="chip">⏳ Pending: <span id="stat-pending">0</span></span>
              </div>
            </div>
          </div>
        </div>

        <!-- Add Task Card -->
        <div class="card shadow-sm mb-4">
          <div class="card-body p-3 p-md-4">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h2 class="h6 mb-0 text-light">Add new task</h2>
              <span style="font-size:0.75rem;" class="text-secondary">Stored only on this browser (localStorage)</span>
            </div>
            <form id="task-form">
              <div class="row g-2 g-md-3 align-items-center">
                <div class="col-md-4">
                  <input
                    type="text"
                    id="title-input"
                    class="form-control"
                    placeholder="Task title (eg: DS assignment)"
                    required
                  >
                </div>
                <div class="col-md-3">
                  <input
                    type="text"
                    id="subject-input"
                    class="form-control"
                    placeholder="Subject (optional)"
                  >
                </div>
                <div class="col-md-3">
                  <input
                    type="text"
                    id="deadline-input"
                    class="form-control"
                    placeholder="Deadline (eg: 10-12-2025 evening)"
                  >
                </div>
                <div class="col-md-2 d-grid">
                  <button type="submit" class="btn btn-primary btn-rounded">
                    ➕ Add
                  </button>
                </div>
                <div class="col-12">
                  <input
                    type="text"
                    id="note-input"
                    class="form-control mt-2"
                    placeholder="Extra note (optional)"
                  >
                </div>
              </div>
            </form>
          </div>
        </div>

        <!-- Tasks List -->
        <div class="card shadow-sm">
          <div class="card-body p-3 p-md-4">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h2 class="h6 mb-0 text-light">Your tasks</h2>
              <span class="text-secondary" style="font-size:0.8rem;">
                This list is private to this device.
              </span>
            </div>

            <div id="empty-state" class="text-center py-4" style="display:none;">
              <p class="mb-1">No tasks yet.</p>
              <p class="text-secondary mb-0" style="font-size:0.9rem;">
                Add your first task above and start tracking your semester properly 🚀
              </p>
            </div>

            <div id="task-list" class="list-group list-group-flush">
              <!-- tasks will be injected here by JavaScript -->
            </div>
          </div>
        </div>

        <p class="text-center text-secondary mt-3 mb-0" style="font-size:0.75rem;">
          Built with Flask + localStorage · Each user gets their own tasks, even if they use the same link 💻
        </p>

      </div>
    </div>
  </div>

  <script>
    const STORAGE_KEY = "study_tracker_tasks_v1";

    let tasks = [];

    function formatToday() {
      const now = new Date();
      const options = { day: "2-digit", month: "short", year: "numeric" };
      return now.toLocaleDateString(undefined, options);
    }

    function loadTasks() {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        tasks = [];
        return;
      }
      try {
        tasks = JSON.parse(raw) || [];
      } catch (e) {
        tasks = [];
      }
    }

    function saveTasks() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
    }

    function updateStats() {
      const total = tasks.length;
      const done = tasks.filter(t => t.completed).length;
      const pending = total - done;

      document.getElementById("stat-total").innerText = total;
      document.getElementById("stat-done").innerText = done;
      document.getElementById("stat-pending").innerText = pending;
    }

    function renderTasks() {
      const list = document.getElementById("task-list");
      const emptyState = document.getElementById("empty-state");
      list.innerHTML = "";

      if (tasks.length === 0) {
        emptyState.style.display = "block";
      } else {
        emptyState.style.display = "none";
      }

      tasks.forEach(task => {
        const item = document.createElement("div");
        item.className = "list-group-item px-0 py-3";

        const statusBadge = task.completed
          ? '<span class="badge bg-success badge-status">Done</span>'
          : '<span class="badge bg-warning text-dark badge-status">Pending</span>';

        const titleClass = task.completed ? "text-success" : "text-light";

        let chipsHtml = "";
        if (task.subject) {
          chipsHtml += '<span class="chip">📚 ' + escapeHtml(task.subject) + "</span>";
        }
        if (task.deadline) {
          chipsHtml += '<span class="chip">⏰ ' + escapeHtml(task.deadline) + "</span>";
        }
        if (task.note) {
          chipsHtml += '<span class="chip">🗒 ' + escapeHtml(task.note) + "</span>";
        }
        if (task.created_at) {
          chipsHtml += '<span class="chip">🕒 ' + escapeHtml(task.created_at) + "</span>";
        }

        item.innerHTML = `
          <div class="d-flex justify-content-between align-items-start gap-3">
            <div>
              <div class="d-flex align-items-center gap-2 mb-1">
                <span class="text-secondary" style="font-size:0.75rem;">#${task.id}</span>
                <span class="fw-semibold ${titleClass}">
                  ${escapeHtml(task.title)}
                </span>
                ${statusBadge}
              </div>
              <div class="d-flex flex-wrap gap-2" style="font-size:0.8rem;">
                ${chipsHtml}
              </div>
            </div>
            <div class="d-flex flex-column flex-md-row gap-2">
              ${!task.completed ? `
              <button class="btn btn-success btn-sm btn-rounded" data-action="done" data-id="${task.id}">
                ✅ Done
              </button>` : ""}
              <button class="btn btn-outline-danger btn-sm btn-rounded" data-action="delete" data-id="${task.id}">
                🗑 Delete
              </button>
            </div>
          </div>
        `;

        list.appendChild(item);
      });

      updateStats();
    }

    function escapeHtml(text) {
      return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    }

    function addTaskFromForm(event) {
      event.preventDefault();

      const titleInput = document.getElementById("title-input");
      const subjectInput = document.getElementById("subject-input");
      const deadlineInput = document.getElementById("deadline-input");
      const noteInput = document.getElementById("note-input");

      const title = titleInput.value.trim();
      const subject = subjectInput.value.trim();
      const deadline = deadlineInput.value.trim();
      const note = noteInput.value.trim();

      if (!title) {
        return;
      }

      const nextId = tasks.length > 0 ? Math.max(...tasks.map(t => t.id)) + 1 : 1;

      const now = new Date();
      const createdAt = now.toLocaleString();

      const newTask = {
        id: nextId,
        title,
        subject,
        deadline,
        note,
        completed: false,
        created_at: createdAt
      };

      tasks.push(newTask);
      saveTasks();
      renderTasks();

      titleInput.value = "";
      subjectInput.value = "";
      deadlineInput.value = "";
      noteInput.value = "";
    }

    function handleListClick(event) {
      const btn = event.target.closest("button[data-action]");
      if (!btn) return;

      const action = btn.getAttribute("data-action");
      const id = parseInt(btn.getAttribute("data-id"));

      if (action === "done") {
        tasks = tasks.map(t =>
          t.id === id ? { ...t, completed: true } : t
        );
      } else if (action === "delete") {
        tasks = tasks.filter(t => t.id !== id);
        // reassign ids
        tasks = tasks.map((t, index) => ({ ...t, id: index + 1 }));
      }

      saveTasks();
      renderTasks();
    }

    document.addEventListener("DOMContentLoaded", () => {
      // set today
      const todayChip = document.getElementById("today-chip");
      todayChip.innerText = "📅 Today: " + formatToday();

      loadTasks();
      renderTasks();

      const form = document.getElementById("task-form");
      form.addEventListener("submit", addTaskFromForm);

      const list = document.getElementById("task-list");
      list.addEventListener("click", handleListClick);
    });
  </script>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(TEMPLATE)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
