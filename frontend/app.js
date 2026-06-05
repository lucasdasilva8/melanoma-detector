const API_URL = window.APP_CONFIG?.API_URL || "http://localhost:8000";

const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("file-input");
const preview = document.getElementById("preview");
const analyzeBtn = document.getElementById("analyze-btn");
const clearBtn = document.getElementById("clear-btn");
const statusEl = document.getElementById("status");
const resultsSection = document.getElementById("results");
const riskBadge = document.getElementById("risk-badge");
const resultSummary = document.getElementById("result-summary");
const confidenceValue = document.getElementById("confidence-value");
const confidenceFill = document.getElementById("confidence-fill");
const ctaText = document.getElementById("cta-text");

let selectedFile = null;

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.classList.toggle("error", isError);
}

function handleFile(file) {
  if (!file) return;

  if (!["image/jpeg", "image/png", "image/jpg"].includes(file.type)) {
    setStatus("Please upload a JPEG or PNG image.", true);
    return;
  }

  if (file.size > 10 * 1024 * 1024) {
    setStatus("Image must be 10 MB or smaller.", true);
    return;
  }

  selectedFile = file;
  preview.src = URL.createObjectURL(file);
  preview.classList.remove("hidden");
  dropzone.classList.add("has-preview");
  analyzeBtn.disabled = false;
  clearBtn.classList.remove("hidden");
  resultsSection.classList.add("hidden");
  setStatus("Image ready. Click Analyze to continue.");
}

dropzone.addEventListener("click", () => fileInput.click());
dropzone.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    fileInput.click();
  }
});

fileInput.addEventListener("change", (event) => {
  handleFile(event.target.files[0]);
});

dropzone.addEventListener("dragover", (event) => {
  event.preventDefault();
  dropzone.classList.add("dragover");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("dragover");
});

dropzone.addEventListener("drop", (event) => {
  event.preventDefault();
  dropzone.classList.remove("dragover");
  handleFile(event.dataTransfer.files[0]);
});

clearBtn.addEventListener("click", () => {
  selectedFile = null;
  fileInput.value = "";
  preview.src = "";
  preview.classList.add("hidden");
  dropzone.classList.remove("has-preview");
  analyzeBtn.disabled = true;
  clearBtn.classList.add("hidden");
  resultsSection.classList.add("hidden");
  setStatus("");
});

analyzeBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  analyzeBtn.disabled = true;
  setStatus("Analyzing image...");

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Analysis failed.");
    }

    showResults(data);
    setStatus("Analysis complete.");
  } catch (error) {
    setStatus(error.message || "Could not reach the API. Is the backend running?", true);
  } finally {
    analyzeBtn.disabled = false;
  }
});

function showResults(data) {
  const isHighRisk = data.risk_level === "high";
  const confidencePct = Math.round(data.confidence * 100);

  riskBadge.textContent = isHighRisk
    ? "Possible melanoma — consult a doctor"
    : "Likely benign";
  riskBadge.className = `risk-badge ${isHighRisk ? "high" : "low"}`;

  resultSummary.textContent = isHighRisk
    ? "The model detected patterns that may be consistent with melanoma. This does not mean you have cancer — only a dermatologist can provide a diagnosis."
    : "The model did not detect strong melanoma patterns in this image. Continue regular skin checks and see a doctor if anything changes.";

  confidenceValue.textContent = `${confidencePct}%`;
  confidenceFill.style.width = `${confidencePct}%`;
  confidenceFill.classList.toggle("high-risk", isHighRisk);

  ctaText.textContent = isHighRisk
    ? "We recommend scheduling an appointment with a dermatologist as soon as possible."
    : "If you notice changes in size, shape, or color, consult a dermatologist regardless of this result.";

  resultsSection.classList.remove("hidden");
}
