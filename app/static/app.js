let exerciseMetaCache = {
    body_parts: [],
    equipment: [],
    difficulty: [],
    exercise_types: [],
    total_exercises: 0
};

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("workout-form");

    if (form) {
        form.addEventListener("submit", createWorkout);
    }

    setTodayDate();
    initializeDashboard();
});

async function initializeDashboard() {
    await Promise.all([
        loadWorkouts(),
        loadAnalytics(),
        loadExerciseMeta(),
        loadExercises(),
        loadTopRatedExercises()
    ]);

    ensureAtLeastOneWorkoutExerciseRow();
}

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
        notes: document.getElementById("notes").value || null,
        exercises: collectWorkoutExercises()
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
            const errorText = await safeReadError(res);
            message.textContent = errorText || "Error creating workout.";
            return;
        }

        message.textContent = "Workout added successfully.";
        document.getElementById("workout-form").reset();
        setTodayDate();
        resetWorkoutExerciseRows();

        await loadWorkouts();
        await loadAnalytics();
    } catch (error) {
        message.textContent = "Network error while creating workout.";
    }
}

function collectWorkoutExercises() {
    const rows = document.querySelectorAll(".workout-exercise-row");

    return Array.from(rows)
        .map(row => {
            const exerciseId = row.querySelector(".workout-exercise-select")?.value || "";
            const sets = row.querySelector(".workout-exercise-sets")?.value || "";
            const reps = row.querySelector(".workout-exercise-reps")?.value || "";
            const weight = row.querySelector(".workout-exercise-weight")?.value || "";

            if (!exerciseId || !sets || !reps) {
                return null;
            }

            return {
                exercise_id: parseInt(exerciseId, 10),
                sets: parseInt(sets, 10),
                reps: parseInt(reps, 10),
                weight_kg: weight === "" ? null : parseInt(weight, 10)
            };
        })
        .filter(Boolean);
}

function ensureAtLeastOneWorkoutExerciseRow() {
    const container = document.getElementById("workout-exercise-rows");
    if (!container) return;

    if (container.children.length === 0) {
        addWorkoutExerciseRow();
    }
}

function resetWorkoutExerciseRows() {
    const container = document.getElementById("workout-exercise-rows");
    if (!container) return;

    container.innerHTML = "";
    addWorkoutExerciseRow();
}

function addWorkoutExerciseRow() {
    const container = document.getElementById("workout-exercise-rows");
    if (!container) return;

    const row = document.createElement("div");
    row.className = "workout-exercise-row";

    row.innerHTML = `
        <div class="workout-exercise-grid">
            <select class="workout-exercise-select">
                <option value="">Select exercise</option>
            </select>

            <input
                class="workout-exercise-search"
                type="text"
                placeholder="Optional quick filter by name"
            >

            <input
                class="workout-exercise-sets"
                type="number"
                min="1"
                placeholder="Sets"
            >

            <input
                class="workout-exercise-reps"
                type="number"
                min="1"
                placeholder="Reps"
            >

            <input
                class="workout-exercise-weight"
                type="number"
                min="0"
                placeholder="Weight (kg)"
            >

            <button type="button" class="delete remove-row-btn">Remove</button>
        </div>
    `;

    container.appendChild(row);

    populateWorkoutExerciseSelect(row.querySelector(".workout-exercise-select"), []);
    attachWorkoutExerciseRowEvents(row);
}

function attachWorkoutExerciseRowEvents(row) {
    const select = row.querySelector(".workout-exercise-select");
    const searchInput = row.querySelector(".workout-exercise-search");
    const removeBtn = row.querySelector(".remove-row-btn");

    searchInput.addEventListener("input", async () => {
        await populateWorkoutExerciseSelect(select, await fetchExercisesForSelect(searchInput.value.trim()));
    });

    removeBtn.addEventListener("click", () => {
        row.remove();
        ensureAtLeastOneWorkoutExerciseRow();
    });
}

async function fetchExercisesForSelect(query) {
    const params = new URLSearchParams();
    if (query) params.append("q", query);
    params.append("limit", "30");
    params.append("sort_by", "recommended");

    try {
        const res = await fetch(`/exercises?${params.toString()}`);
        const data = await res.json();
        return Array.isArray(data) ? data : [];
    } catch (error) {
        return [];
    }
}

async function populateWorkoutExerciseSelect(selectElement, exercises) {
    if (!selectElement) return;

    const currentValue = selectElement.value || "";

    let dataset = exercises;
    if (!dataset || dataset.length === 0) {
        dataset = await fetchExercisesForSelect("");
    }

    selectElement.innerHTML = `<option value="">Select exercise</option>`;

    dataset.forEach(exercise => {
        const option = document.createElement("option");
        option.value = exercise.id;
        option.textContent = `${exercise.name} (${exercise.body_part ?? "N/A"})`;
        selectElement.appendChild(option);
    });

    if ([...selectElement.options].some(option => option.value === currentValue)) {
        selectElement.value = currentValue;
    }
}

async function loadWorkouts() {
    const container = document.getElementById("workouts");
    container.innerHTML = `<p class="loading-state">Loading workouts...</p>`;

    try {
        const res = await fetch("/workouts");
        const data = await res.json();

        if (!Array.isArray(data) || data.length === 0) {
            container.innerHTML = `<p class="empty-state">No workouts found.</p>`;
            return;
        }

        container.innerHTML = data.map(w => `
            <div class="workout-card">
                <h4>${escapeHtml(w.workout_type)}</h4>
                <div class="workout-meta">
                    <strong>Date:</strong> ${escapeHtml(String(w.date))}<br>
                    <strong>Duration:</strong> ${escapeHtml(String(w.duration_min))} min<br>
                    <strong>Notes:</strong> ${escapeHtml(w.notes ?? "None")}
                </div>

                ${
                    Array.isArray(w.exercises) && w.exercises.length > 0
                        ? `
                            <div class="logged-exercises">
                                <h5>Logged Exercises</h5>
                                ${w.exercises.map(ex => `
                                    <div class="logged-exercise-item">
                                        <strong>${escapeHtml(ex.exercise_name ?? `Exercise #${ex.exercise_id}`)}</strong><br>
                                        <span>
                                            Sets: ${escapeHtml(String(ex.sets))} |
                                            Reps: ${escapeHtml(String(ex.reps))} |
                                            Weight: ${escapeHtml(String(ex.weight_kg ?? 0))} kg
                                        </span>
                                    </div>
                                `).join("")}
                            </div>
                        `
                        : `<p class="empty-inline">No exercise details logged.</p>`
                }

                <button class="delete" onclick="deleteWorkout(${w.id})">Delete</button>
            </div>
        `).join("");
    } catch (error) {
        container.innerHTML = `<p class="empty-state">Failed to load workouts.</p>`;
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

        await loadWorkouts();
        await loadAnalytics();
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
            <div class="weekly-box">
                <strong>Week Start</strong>
                <span>${escapeHtml(weekly.week_start ?? "N/A")}</span>
            </div>
            <div class="weekly-box">
                <strong>Week End</strong>
                <span>${escapeHtml(weekly.week_end ?? "N/A")}</span>
            </div>
            <div class="weekly-box">
                <strong>Total Sessions</strong>
                <span>${escapeHtml(String(weekly.total_sessions ?? 0))}</span>
            </div>
            <div class="weekly-box">
                <strong>Total Minutes</strong>
                <span>${escapeHtml(String(weekly.total_minutes ?? 0))}</span>
            </div>
        `;
    } catch (error) {
        document.getElementById("weekly").innerHTML = `<p class="empty-state">Failed to load analytics.</p>`;
    }
}

async function loadExerciseMeta() {
    try {
        const res = await fetch("/exercises/meta/filters");
        const data = await res.json();

        exerciseMetaCache = data;

        document.getElementById("total-exercises").textContent = data.total_exercises ?? 0;
        document.getElementById("meta-body-parts-count").textContent = data.body_parts?.length ?? 0;
        document.getElementById("meta-equipment-count").textContent = data.equipment?.length ?? 0;
        document.getElementById("meta-difficulty-count").textContent = data.difficulty?.length ?? 0;
        document.getElementById("meta-type-count").textContent = data.exercise_types?.length ?? 0;

        populateSelect("exercise-body-part", data.body_parts, "All body parts");
        populateSelect("exercise-equipment", data.equipment, "All equipment");
        populateSelect("exercise-difficulty", data.difficulty, "All difficulty levels");
        populateSelect("exercise-type", data.exercise_types, "All exercise types");

        populateSelect("plan-equipment", data.equipment, "Any Equipment");
        populateSelect("plan-difficulty", data.difficulty, "Any Difficulty");
    } catch (error) {
        console.error("Failed to load exercise metadata", error);
    }
}

function populateSelect(id, values, defaultLabel) {
    const select = document.getElementById(id);
    if (!select) return;

    const currentValue = select.value;

    select.innerHTML = `<option value="">${escapeHtml(defaultLabel)}</option>`;

    (values || []).forEach(value => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        select.appendChild(option);
    });

    if ([...select.options].some(option => option.value === currentValue)) {
        select.value = currentValue;
    }
}

function getExerciseFilterParams() {
    const q = document.getElementById("exercise-q").value.trim();
    const bodyPart = document.getElementById("exercise-body-part").value;
    const equipment = document.getElementById("exercise-equipment").value;
    const difficulty = document.getElementById("exercise-difficulty").value;
    const exerciseType = document.getElementById("exercise-type").value;
    const sortBy = document.getElementById("exercise-sort").value;

    const params = new URLSearchParams();

    if (q) params.append("q", q);
    if (bodyPart) params.append("body_part", bodyPart);
    if (equipment) params.append("equipment", equipment);
    if (difficulty) params.append("difficulty", difficulty);
    if (exerciseType) params.append("exercise_type", exerciseType);
    if (sortBy) params.append("sort_by", sortBy);

    return params;
}

async function loadExercises() {
    const params = getExerciseFilterParams();
    params.append("limit", "20");

    const container = document.getElementById("exercises-results");
    container.innerHTML = `<p class="loading-state">Loading exercises...</p>`;

    try {
        const res = await fetch(`/exercises?${params.toString()}`);
        const data = await res.json();

        if (!Array.isArray(data) || data.length === 0) {
            container.innerHTML = `<p class="empty-state">No exercises found.</p>`;
            return;
        }

        container.innerHTML = data.map(renderExerciseCard).join("");
    } catch (error) {
        container.innerHTML = `<p class="empty-state">Failed to load exercises.</p>`;
    }
}

async function loadRecommendedExercises() {
    const params = getExerciseFilterParams();
    params.append("limit", "6");

    const container = document.getElementById("recommended-results");
    container.innerHTML = `<p class="loading-state">Loading recommendations...</p>`;

    try {
        const res = await fetch(`/exercises/recommend?${params.toString()}`);
        const data = await res.json();

        if (!Array.isArray(data) || data.length === 0) {
            container.innerHTML = `<p class="empty-state">No recommendations available.</p>`;
            return;
        }

        container.innerHTML = data.map(renderExerciseCard).join("");
    } catch (error) {
        container.innerHTML = `<p class="empty-state">Failed to load recommendations.</p>`;
    }
}

async function loadTopRatedExercises() {
    const container = document.getElementById("top-rated-results");
    container.innerHTML = `<p class="loading-state">Loading top rated exercises...</p>`;

    try {
        const res = await fetch("/analytics/top-rated-exercises?limit=6");
        const data = await res.json();

        if (!Array.isArray(data) || data.length === 0) {
            container.innerHTML = `<p class="empty-state">No top rated exercises found.</p>`;
            return;
        }

        container.innerHTML = data.map(renderExerciseCard).join("");
    } catch (error) {
        container.innerHTML = `<p class="empty-state">Failed to load top rated exercises.</p>`;
    }
}

async function loadWorkoutPlan() {
    const goal = document.getElementById("plan-goal").value;
    const days = document.getElementById("plan-days").value;
    const equipment = document.getElementById("plan-equipment").value;
    const difficulty = document.getElementById("plan-difficulty").value;

    const params = new URLSearchParams();
    params.append("goal", goal);
    params.append("days", days);
    if (equipment) params.append("equipment", equipment);
    if (difficulty) params.append("difficulty", difficulty);

    const container = document.getElementById("plan-results");
    container.innerHTML = `<p class="loading-state">Generating workout plan...</p>`;

    try {
        const res = await fetch(`/workouts/suggest-plan?${params.toString()}`);
        const data = await res.json();

        if (!data.plan || !Array.isArray(data.plan) || data.plan.length === 0) {
            container.innerHTML = `<p class="empty-state">No workout plan available.</p>`;
            return;
        }

        container.innerHTML = `
            <div class="plan-card">
                <h4>${formatTitle(data.goal)} Plan</h4>
                <div class="plan-meta">
                    <strong>Days:</strong> ${escapeHtml(String(data.days))}<br>
                    <strong>Equipment:</strong> ${escapeHtml(data.equipment ?? "Any")}<br>
                    <strong>Difficulty:</strong> ${escapeHtml(data.difficulty ?? "Any")}
                </div>
            </div>
            ${data.plan.map(day => `
                <div class="plan-card">
                    <h4>Day ${escapeHtml(String(day.day))} — ${escapeHtml(day.focus)}</h4>
                    <ul class="plan-exercise-list">
                        ${(day.exercises || []).map(ex => `<li>${escapeHtml(ex)}</li>`).join("")}
                    </ul>
                </div>
            `).join("")}
        `;
    } catch (error) {
        container.innerHTML = `<p class="empty-state">Failed to generate workout plan.</p>`;
    }
}

function resetExerciseFilters() {
    document.getElementById("exercise-q").value = "";
    document.getElementById("exercise-body-part").value = "";
    document.getElementById("exercise-equipment").value = "";
    document.getElementById("exercise-difficulty").value = "";
    document.getElementById("exercise-type").value = "";
    document.getElementById("exercise-sort").value = "recommended";

    loadExercises();
}

function renderExerciseCard(exercise) {
    return `
        <div class="exercise-card">
            <h4>${escapeHtml(exercise.name)}</h4>
            <div class="exercise-meta">
                <strong>Body Part:</strong> ${escapeHtml(exercise.body_part ?? "N/A")}<br>
                <strong>Equipment:</strong> ${escapeHtml(exercise.equipment ?? "N/A")}<br>
                <strong>Difficulty:</strong> ${escapeHtml(exercise.difficulty ?? "N/A")}<br>
                <strong>Type:</strong> ${escapeHtml(exercise.exercise_type ?? "N/A")}<br>
                <strong>Rating:</strong> ${exercise.rating ?? "N/A"}
            </div>
            <p class="exercise-description">${escapeHtml(exercise.description ?? "No description available.")}</p>
        </div>
    `;
}

async function safeReadError(response) {
    try {
        const data = await response.json();
        return data.detail || null;
    } catch (error) {
        return null;
    }
}

function formatTitle(value) {
    if (!value) return "Workout";
    return value
        .split("_")
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
}

function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value;
    return div.innerHTML;
}