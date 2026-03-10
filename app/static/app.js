const API_BASE = "";

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("workout-form").addEventListener("submit", createWorkout);
  document.getElementById("refresh-btn").addEventListener("click", loadWorkouts);

  setTodayDate();
  loadWorkouts();
  loadStreak();
  loadWeeklySummary();
});

function setTodayDate() {
  const today = new Date().toISOString().split("T")[0];
  document.getElementById("date").value = today;
}

async function createWorkout(event) {
  event.preventDefault();

  const message = document.getElementById("form-message");
  message.textContent = "";

  const payload = {
    workout_type: document.getElementById("workout_type").value,
    duration_min: parseInt(document.getElementById("duration_min").value),
    date: document.getElementById("date").value,
    notes: document.getElementById("notes").value || null
  };

  try {
    const response = await fetch(`${API_BASE}/workouts`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const error = await response.json();
      message.textContent = `Error: ${error.detail || "Failed to create workout"}`;
      return;
    }

    message.textContent = "Workout added successfully.";
    document.getElementById("workout-form").reset();
    setTodayDate();

    loadWorkouts();
    loadStreak();
    loadWeeklySummary();
  } catch (error) {
    message.textContent = "Network error while creating workout.";
  }
}

async function loadWorkouts() {
  const container = document.getElementById("workouts-list");
  container.innerHTML = "<p>Loading workouts...</p>";

  try {
    const response = await fetch(`${API_BASE}/workouts`);
    const workouts = await response.json();

    if (!Array.isArray(workouts) || workouts.length === 0) {
      container.innerHTML = "<p>No workouts found.</p>";
      return;
    }

    container.innerHTML = workouts
      .map(workout => `
        <div class="workout-item">
          <h4>${escapeHtml(workout.workout_type)}</h4>
          <p><strong>Date:</strong> ${workout.date}</p>
          <p><strong>Duration:</strong> ${workout.duration_min} min</p>
          <p><strong>Notes:</strong> ${escapeHtml(workout.notes || "None")}</p>
          <div class="workout-actions">
            <button class="delete-btn" onclick="deleteWorkout(${workout.id})">Delete</button>
          </div>
        </div>
      `)
      .join("");
  } catch (error) {
    container.innerHTML = "<p>Failed to load workouts.</p>";
  }
}

async function deleteWorkout(id) {
  try {
    const response = await fetch(`${API_BASE}/workouts/${id}`, {
      method: "DELETE"
    });

    if (!response.ok) {
      alert("Failed to delete workout.");
      return;
    }

    loadWorkouts();
    loadStreak();
    loadWeeklySummary();
  } catch (error) {
    alert("Network error while deleting workout.");
  }
}

async function loadStreak() {
  try {
    const response = await fetch(`${API_BASE}/analytics/streak`);
    const data = await response.json();

    document.getElementById("current-streak").textContent = data.current_streak ?? "-";
    document.getElementById("longest-streak").textContent = data.longest_streak ?? "-";
    document.getElementById("total-workout-days").textContent = data.total_workout_days ?? "-";
  } catch (error) {
    document.getElementById("current-streak").textContent = "Error";
    document.getElementById("longest-streak").textContent = "Error";
    document.getElementById("total-workout-days").textContent = "Error";
  }
}

async function loadWeeklySummary() {
  const container = document.getElementById("weekly-summary");

  const today = new Date();
  const day = today.getDay();
  const diffToMonday = day === 0 ? 6 : day - 1;
  const monday = new Date(today);
  monday.setDate(today.getDate() - diffToMonday);

  const weekStart = monday.toISOString().split("T")[0];

  try {
    const response = await fetch(`${API_BASE}/analytics/weekly-summary?week_start=${weekStart}`);
    const data = await response.json();

    const typeEntries = data.sessions_by_type
      ? Object.entries(data.sessions_by_type)
          .map(([type, count]) => `<li>${escapeHtml(type)}: ${count}</li>`)
          .join("")
      : "";

    container.innerHTML = `
      <p><strong>Week Start:</strong> ${data.week_start}</p>
      <p><strong>Week End:</strong> ${data.week_end}</p>
      <p><strong>Total Sessions:</strong> ${data.total_sessions}</p>
      <p><strong>Total Minutes:</strong> ${data.total_minutes}</p>
      <div>
        <strong>Sessions by Type:</strong>
        <ul>${typeEntries || "<li>No sessions this week</li>"}</ul>
      </div>
    `;
  } catch (error) {
    container.innerHTML = "<p>Failed to load weekly summary.</p>";
  }
}

function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = value;
  return div.innerHTML;
}