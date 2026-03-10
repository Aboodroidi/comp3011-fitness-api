document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("workout-form");

    if (form) {
        form.addEventListener("submit", createWorkout);
    }

    setTodayDate();
    loadWorkouts();
    loadAnalytics();
    loadExercises();
});

function setTodayDate() {
    const dateInput = document.getElementById("date");
    if (!dateInput) return;

    const today = new Date().toISOString().split("T")[0];
    dateInput.value = today;
}

async function createWorkout(event) {
    event.preventDefault();

    const message = document.getElementById("message");

    const payload = {
        workout_type: document.getElementById("type").value,
        duration_min: parseInt(document.getElementById("duration").value, 10),
        date: document.getElementById("date").value,
        notes: document.getElementById("notes").value || null
    };

    try {
        const res = await fetch("/workouts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            message.textContent = "Error creating workout.";
            return;
        }

        message.textContent = "Workout added successfully.";
        document.getElementById("workout-form").reset();
        setTodayDate();

        loadWorkouts();
        loadAnalytics();
    } catch (error) {
        message.textContent = "Network error while creating workout.";
    }
}

async function loadWorkouts() {
    const container = document.getElementById("workouts");
    container.innerHTML = "<p>Loading workouts...</p>";

    try {
        const res = await fetch("/workouts");
        const data = await res.json();

        if (!Array.isArray(data) || data.length === 0) {
            container.innerHTML = "<p>No workouts found.</p>";
            return;
        }

        container.innerHTML = data.map(w => `
            <div class="workout">
                <b>${escapeHtml(w.workout_type)}</b><br>
                Date: ${w.date}<br>
                Duration: ${w.duration_min} min<br>
                Notes: ${escapeHtml(w.notes ?? "None")}<br><br>
                <button class="delete" onclick="deleteWorkout(${w.id})">Delete</button>
            </div>
        `).join("");
    } catch (error) {
        container.innerHTML = "<p>Failed to load workouts.</p>";
    }
}

async function deleteWorkout(id) {
    try {
        const res = await fetch(`/workouts/${id}`, {
            method: "DELETE"
        });

        if (!res.ok) {
            alert("Failed to delete workout.");
            return;
        }

        loadWorkouts();
        loadAnalytics();
    } catch (error) {
        alert("Network error while deleting workout.");
    }
}

async function loadAnalytics() {
    try {
        const streakRes = await fetch("/analytics/streak");
        const streak = await streakRes.json();

        document.getElementById("current").textContent = streak.current_streak ?? 0;
        document.getElementById("longest").textContent = streak.longest_streak ?? 0;
        document.getElementById("days").textContent = streak.total_workout_days ?? 0;

        const today = new Date();
        const monday = new Date(today);
        monday.setDate(today.getDate() - (today.getDay() || 7) + 1);
        const weekStart = monday.toISOString().split("T")[0];

        const weeklyRes = await fetch(`/analytics/weekly-summary?week_start=${weekStart}`);
        const weekly = await weeklyRes.json();

        document.getElementById("weekly").innerHTML = `
            <p><strong>Week Start:</strong> ${weekly.week_start}</p>
            <p><strong>Week End:</strong> ${weekly.week_end}</p>
            <p><strong>Total Sessions:</strong> ${weekly.total_sessions}</p>
            <p><strong>Total Minutes:</strong> ${weekly.total_minutes}</p>
        `;
    } catch (error) {
        document.getElementById("weekly").innerHTML = "<p>Failed to load analytics.</p>";
    }
}

async function loadExercises() {
    const q = document.getElementById("exercise-q").value.trim();
    const bodyPart = document.getElementById("exercise-body-part").value.trim();
    const equipment = document.getElementById("exercise-equipment").value.trim();
    const difficulty = document.getElementById("exercise-difficulty").value.trim();
    const exerciseType = document.getElementById("exercise-type").value.trim();
    const sortBy = document.getElementById("exercise-sort").value;

    const params = new URLSearchParams();

    if (q) params.append("q", q);
    if (bodyPart) params.append("body_part", bodyPart);
    if (equipment) params.append("equipment", equipment);
    if (difficulty) params.append("difficulty", difficulty);
    if (exerciseType) params.append("exercise_type", exerciseType);
    if (sortBy) params.append("sort_by", sortBy);

    params.append("limit", "20");

    const container = document.getElementById("exercises-results");
    container.innerHTML = "<p>Loading exercises...</p>";

    try {
        const res = await fetch(`/exercises?${params.toString()}`);
        const data = await res.json();

        if (!Array.isArray(data) || data.length === 0) {
            container.innerHTML = "<p>No exercises found.</p>";
            return;
        }

        container.innerHTML = data.map(exercise => `
            <div class="exercise-card">
                <h4>${escapeHtml(exercise.name)}</h4>
                <div class="exercise-meta">
                    <strong>Body Part:</strong> ${escapeHtml(exercise.body_part ?? "N/A")} |
                    <strong>Equipment:</strong> ${escapeHtml(exercise.equipment ?? "N/A")} |
                    <strong>Difficulty:</strong> ${escapeHtml(exercise.difficulty ?? "N/A")} |
                    <strong>Type:</strong> ${escapeHtml(exercise.exercise_type ?? "N/A")}
                </div>
                <p><strong>Rating:</strong> ${exercise.rating ?? "N/A"}</p>
                <p>${escapeHtml(exercise.description ?? "No description available.")}</p>
            </div>
        `).join("");
    } catch (error) {
        container.innerHTML = "<p>Failed to load exercises.</p>";
    }
}

function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value;
    return div.innerHTML;
}