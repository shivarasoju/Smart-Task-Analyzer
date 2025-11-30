const input = document.getElementById("taskInput");
const output = document.getElementById("output");
const dropdown = document.getElementById("sortDropdown");

const BASE_URL = window.BACKEND_URL;

let rawTasks = [];
let analyzedTasks = [];

const handleFailedApiCase = (analyzedTasks) => {
  output.textContent = `Cannot suggest tasks as ${analyzedTasks.error}`;
  output.style.backgroundColor = "red";
  output.style.color = "white";
};

function renderTaskCards(taskList) {
  output.innerHTML = "";

  taskList.forEach((task, index) => {
    const card = document.createElement("div");

    card.textContent = task.title || "Untitled Task";

    card.style.padding = "12px";
    card.style.marginBottom = "10px";
    card.style.borderRadius = "10px";
    card.style.background = "rgba(0,0,0,0.25)";
    card.style.color = "white";
    card.style.fontSize = "15px";
    card.style.boxShadow = "0 3px 12px rgba(0,0,0,0.25)";

    if (index === 0) {
      card.style.borderLeft = "6px solid #ef4444";
    } else {
      card.style.borderLeft = "6px solid #22c55e";
    }
    output.style.backgroundColor = "";
    output.appendChild(card);
  });
}

input.addEventListener("change", () => {
  rawTasks = JSON.parse(input.value);
});

document.getElementById("analyzeBtn").onclick = async function () {
  try {
    rawTasks = JSON.parse(input.value);
    const url = BASE_URL
      ? `${BASE_URL}/api/tasks/analyze/`
      : "http://127.0.0.1:8000/api/tasks/analyze/";
    // console.log(url, "this is url");

    let res = await fetch(url, {
      method: "POST",
      body: input.value,
    });

    analyzedTasks = await res.json();
    // console.log(analyzedTasks, "this is data");

    if (res.status !== 200) {
      handleFailedApiCase(analyzedTasks);
      return;
    }

    renderTaskCards(analyzedTasks);
    input.value = "";
  } catch (e) {
    output.textContent = e.message;
  }
};

document.getElementById("suggestBtn").onclick = async function () {
  try {
    rawTasks = JSON.parse(input.value);

    const url = BASE_URL
      ? `${BASE_URL}/api/tasks/suggest/`
      : "http://127.0.0.1:8000/api/tasks/suggest/";

    // console.log(url, "this is suggest url");

    let res = await fetch(url, {
      method: "POST",
      body: input.value,
    });

    let data = await res.json();
    // console.log(data, "this is suggest data");

    if (res.status !== 200) {
      handleFailedApiCase(data);
      return;
    }
    renderTaskCards(data.tasks);
    input.value = "";
  } catch (e) {
    output.textContent = e.message;
  }
};

// dropdown.onchange = function ()

dropdown.addEventListener("change", () => {
  if (rawTasks.length === 0) return;

  let sorted;

  if (dropdown.value === "fastest") {
    sorted = [...rawTasks].sort(
      (a, b) => a.estimated_hours - b.estimated_hours
    );
  }

  if (dropdown.value === "deadline") {
    sorted = [...rawTasks].sort(
      (a, b) => new Date(a.due_date) - new Date(b.due_date)
    );
  }

  if (dropdown.value === "importance") {
    sorted = [...rawTasks].sort((a, b) => b.importance - a.importance);
  }

  renderTaskCards(sorted);
});
