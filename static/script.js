// -------------------------------------------------------
// Helper: Show the reply in the answer box
// -------------------------------------------------------
function showReply(text) {
    const answerBox = document.getElementById("answerBox");
    answerBox.innerHTML = text.replace(/\n/g, "<br>");
}

// -------------------------------------------------------
// ASK QUESTION
// -------------------------------------------------------
async function sendQuestion() {
    const question = document.getElementById("questionInput").value.trim();
    const extra = document.getElementById("extraInput").value.trim();

    if (!question) {
        showReply("Please type a question first 😊");
        return;
    }

    showReply("Thinking... 🔄");

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: question, extra: extra })
        });

        const data = await response.json();
        showReply(data.reply || "No answer received.");
    } catch (err) {
        showReply("❌ Error connecting to server.");
        console.error(err);
    }
}


// -------------------------------------------------------
// SUMMARIZE NOTES
// -------------------------------------------------------
async function summarizeNotes() {
    const notes = document.getElementById("notesInput").value.trim();

    if (!notes) {
        showReply("Paste some notes to summarize 📝");
        return;
    }

    showReply("Summarizing... ✨");

    try {
        const response = await fetch("/summarize", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ notes: notes })
        });

        const data = await response.json();
        showReply(data.reply || "No summary received.");
    } catch (err) {
        showReply("❌ Error connecting to server.");
        console.error(err);
    }
}


// -------------------------------------------------------
// GENERATE QUIZ
// -------------------------------------------------------
async function generateQuiz() {
    const notes = document.getElementById("notesInput").value.trim();

    if (!notes) {
        showReply("Paste notes or a topic to generate a quiz 😊");
        return;
    }

    showReply("Generating quiz... 🧠");

    try {
        const response = await fetch("/quiz", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ notes: notes })
        });

        const data = await response.json();
        showReply(data.reply || "No quiz received.");
    } catch (err) {
        showReply("❌ Error connecting to server.");
        console.error(err);
    }
}


// -------------------------------------------------------
// EVENT LISTENERS
// -------------------------------------------------------
document.getElementById("sendBtn").addEventListener("click", sendQuestion);
document.getElementById("summarizeBtn").addEventListener("click", summarizeNotes);
document.getElementById("quizBtn").addEventListener("click", generateQuiz);

