document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", (event) => {
        event.preventDefault();
        const target = document.querySelector(anchor.getAttribute("href"));
        if (target) {
            target.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    });
});

const revealItems = document.querySelectorAll(".card, .price-card, .step, .faq-item, .sample-box, .app-card");

const revealObserver = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                revealObserver.unobserve(entry.target);
            }
        });
    },
    { threshold: 0.12 }
);

revealItems.forEach((item) => {
    item.classList.add("reveal");
    revealObserver.observe(item);
});

const fileInput = document.getElementById("docxFile");
const wordsPerPageInput = document.getElementById("wordsPerPage");
const apiBaseUrlInput = document.getElementById("apiBaseUrl");
const generateBtn = document.getElementById("generateBtn");
const downloadBtn = document.getElementById("downloadBtn");
const indexOutput = document.getElementById("indexOutput");
const appStatus = document.getElementById("appStatus");

let lastGeneratedIndex = "";

const DEFAULT_API_BASE = "https://indexer-azf4.onrender.com";

if (apiBaseUrlInput) {
    apiBaseUrlInput.value = localStorage.getItem("indexerApiBase") || DEFAULT_API_BASE;
}

async function handleGenerate() {
    const file = fileInput.files[0];
    if (!file) {
        appStatus.textContent = "Please select a .docx file first.";
        return;
    }
    
    const baseUrl = (apiBaseUrlInput?.value || "").trim().replace(/\/$/, "");
    if (!baseUrl) {
        appStatus.textContent = "Please enter your Render API URL.";
        return;
    }
    localStorage.setItem("indexerApiBase", baseUrl);

    const wordsPerPage = Number(wordsPerPageInput.value) || 250;
    appStatus.textContent = "Uploading document to high-accuracy API...";
    downloadBtn.classList.add("hidden");
    generateBtn.disabled = true;

    try {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("words_per_page", String(wordsPerPage));

        const response = await fetch(`${baseUrl}/generate-index`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            let detail = "Request failed.";
            try {
                const err = await response.json();
                detail = err.detail || detail;
            } catch (_) {
                // ignore JSON parse issues
            }
            throw new Error(detail);
        }

        const data = await response.json();
        const generated = data.index || "";
        indexOutput.value = generated;
        lastGeneratedIndex = generated;
        if (generated) {
            downloadBtn.classList.remove("hidden");
        }
        appStatus.textContent = `Index generated using ${data.model || "spaCy model"}.`;
    } catch (error) {
        appStatus.textContent = `Generation failed: ${error.message}`;
    } finally {
        generateBtn.disabled = false;
    }
}

function handleDownload() {
    if (!lastGeneratedIndex) return;
    const blob = new Blob([lastGeneratedIndex], { type: "text/plain;charset=utf-8" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "generated_index.txt";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
}

generateBtn?.addEventListener("click", handleGenerate);
downloadBtn?.addEventListener("click", handleDownload);
