let tasks = [];

function addTask() {
    tasks.push({
        title: document.getElementById("title").value,
        due_date: document.getElementById("due").value,
        estimated_hours: Number(document.getElementById("hours").value),
        importance: Number(document.getElementById("importance").value),
        dependencies: document.getElementById("deps").value.split(",").map(s => s.trim()).filter(Boolean)
    });
    alert("Task added!");
}

function loadJson() {
    tasks = JSON.parse(document.getElementById("taskJson").value);
    alert("Loaded JSON tasks");
}

async function analyze() {
    const res = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(tasks)
    });

    const data = await res.json();
    render(data);
}

function render(tasks) {
    const div = document.getElementById("output");
    div.innerHTML = "";

    tasks.forEach(t => {
        div.innerHTML += `
            <div class="task">
                <h3>${t.title}</h3>
                <p>Score: ${t.score}</p>
                <p>${t.explanation}</p>
            </div>
        `;
    });
}
