async function uploadImage() {
  const fileInput = document.getElementById("imageInput");
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const res = await fetch("/analyze", {
    method: "POST",
    body: formData
  });

  const data = await res.json();

  document.getElementById("resultText").innerText = `Sonuç: ${data.result}\nGüven: %${data.confidence}`;
  document.getElementById("resultModal").style.display = "block";

  loadStats();
  loadHistory();
}

function closeModal() {
  document.getElementById("resultModal").style.display = "none";
}

async function loadStats() {
  const res = await fetch("/stats");
  const data = await res.json();

  const ctx = document.getElementById('statsChart').getContext('2d');
  if (window.statsChart && typeof window.statsChart.destroy === "function") {
    window.statsChart.destroy();
  }

  window.statsChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Normal', 'Zatürre'],
      datasets: [{
        data: [data.normal, data.pneumonia],
        backgroundColor: ['#4CAF50', '#F44336']
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' },
        title: {
          display: true,
          text: `Toplam: ${data.total} - Ortalama Güven: %${data.average_confidence}`
        }
      }
    }
  });
}

async function loadHistory() {
  try {
    const res = await fetch("/history");
    const history = await res.json();

    if (!Array.isArray(history)) throw new Error("Geçersiz veri formatı");

    const table = document.getElementById("historyTable");
    table.innerHTML = "";

    history.reverse().forEach(item => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.timestamp}</td>
        <td>${item.filename}</td>
        <td>${item.result}</td>
        <td>%${item.confidence}</td>
      `;
      table.appendChild(row);
    });
  } catch (err) {
    console.error("Analiz geçmişi yüklenemedi:", err.message);
  }
}

window.onload = () => {
  loadStats();
  loadHistory();

  const dropArea = document.getElementById("upload-area");
  const input = document.getElementById("imageInput");

  // Drag Over
  dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("dragover");
  });

  dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("dragover");
  });

  // Drop
  dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("dragover");
    input.files = e.dataTransfer.files;
  });
};
