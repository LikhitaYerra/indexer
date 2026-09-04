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
const generateBtn = document.getElementById("generateBtn");
const downloadBtn = document.getElementById("downloadBtn");
const indexOutput = document.getElementById("indexOutput");
const appStatus = document.getElementById("appStatus");

let lastGeneratedIndex = "";

const excludedTerms = new Set([
    "The", "A", "An", "And", "Or", "But", "In", "On", "At", "By", "For", "To", "Of",
    "Chapter", "Part", "Section", "Figure", "Table", "Index", "University", "Press",
    "Empire", "Kingdom", "Republic", "City", "County", "Street", "Road", "River",
    "North", "South", "East", "West", "January", "February", "March", "April", "May",
    "June", "July", "August", "September", "October", "November", "December"
]);

const knownPlaceWords = new Set([
    "Rome", "Egypt", "China", "India", "London", "Paris", "Berlin", "Athens", "Sparta",
    "Africa", "Europe", "Asia", "America", "Babylon", "Alexandria", "Peru", "Mexico"
]);

function isLikelyPersonName(term) {
    const cleaned = term.trim().replace(/[.,;:!?]+$/g, "");
    if (cleaned.length < 3) return false;
    if (/^\d+$/.test(cleaned)) return false;

    const parts = cleaned.split(/\s+/);
    if (parts.length > 5) return false;
    if (excludedTerms.has(parts[0])) return false;

    if (parts.length === 1) {
        if (knownPlaceWords.has(parts[0])) return false;
        return /^[A-Z][a-z]+$/.test(parts[0]);
    }

    const roman = /^(I|II|III|IV|V|VI|VII|VIII|IX|X)$/;
    const validParts = parts.every((word, idx) => {
        if (roman.test(word)) return idx === parts.length - 1;
        return /^[A-Z][a-z]+$/.test(word);
    });

    if (!validParts) return false;

    if (parts.some((word) => knownPlaceWords.has(word))) return false;

    return true;
}

function collectCandidateNames(text) {
    const candidates = [];
    const pattern = /\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,4}(?:\s+(?:I|II|III|IV|V|VI|VII|VIII|IX|X))?)\b/g;
    let match;
    while ((match = pattern.exec(text)) !== null) {
        const candidate = match[1].trim();
        if (isLikelyPersonName(candidate)) {
            candidates.push(candidate);
        }
    }
    return candidates;
}

function generateIndexFromText(text, wordsPerPage) {
    const lines = text.split(/\n+/).map((line) => line.trim()).filter(Boolean);
    const indexMap = new Map();

    let cumulativeWords = 0;
    for (const line of lines) {
        const lineWords = line.split(/\s+/).filter(Boolean).length;
        cumulativeWords += lineWords;
        const page = Math.floor(cumulativeWords / wordsPerPage) + 1;

        const names = collectCandidateNames(line);
        for (const name of names) {
            if (!indexMap.has(name)) indexMap.set(name, new Set());
            indexMap.get(name).add(page);
        }
    }

    const sortedNames = Array.from(indexMap.keys()).sort((a, b) => a.localeCompare(b));
    if (sortedNames.length === 0) {
        return "No person names found. Try a longer document or adjust formatting in your manuscript.";
    }

    const out = ["INDEX", "==============================", ""];
    let currentLetter = "";

    for (const name of sortedNames) {
        const letter = name[0].toUpperCase();
        if (letter !== currentLetter) {
            out.push(`-- ${letter} --`);
            currentLetter = letter;
        }
        const pages = Array.from(indexMap.get(name)).sort((a, b) => a - b).join(", ");
        out.push(`${name}, ${pages}`);
    }

    return out.join("\n");
}

async function handleGenerate() {
    const file = fileInput.files[0];
    if (!file) {
        appStatus.textContent = "Please select a .docx file first.";
        return;
    }

    if (!window.mammoth) {
        appStatus.textContent = "Document parser failed to load. Refresh and try again.";
        return;
    }

    const wordsPerPage = Number(wordsPerPageInput.value) || 250;
    appStatus.textContent = "Reading document...";
    downloadBtn.classList.add("hidden");

    try {
        const arrayBuffer = await file.arrayBuffer();
        const result = await window.mammoth.extractRawText({ arrayBuffer });
        appStatus.textContent = "Generating index...";

        const generated = generateIndexFromText(result.value || "", wordsPerPage);
        indexOutput.value = generated;
        lastGeneratedIndex = generated;
        downloadBtn.classList.remove("hidden");
        appStatus.textContent = "Index generated successfully.";
    } catch (error) {
        appStatus.textContent = "Could not process this file. Please upload a valid .docx document.";
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
