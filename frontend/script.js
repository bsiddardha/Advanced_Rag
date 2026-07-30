// =======================================
// Upload Log File
// =======================================
document.getElementById("uploadBtn").onclick = async () => {

    const fileInput = document.getElementById("logFile");

    if (fileInput.files.length === 0) {
        alert("Please select a log file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    document.getElementById("answer").innerHTML =
        "<h3>Uploading and processing logs...</h3>";

    try {

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        document.getElementById("answer").innerHTML = `
            <h2>✅ Upload Successful</h2>

            <p><strong>Status:</strong> ${data.message}</p>

            <p><strong>Total Chunks:</strong> ${data.chunks}</p>

            <hr>

            <p>You can now ask questions.</p>
        `;

    } catch (error) {

        console.error(error);

        document.getElementById("answer").innerHTML =
            "<h3 style='color:red;'>Upload failed.</h3>";
    }

};


// =======================================
// Process Pasted Logs
// =======================================
document.getElementById("processBtn").onclick = async () => {

    const logs = document.getElementById("logs").value.trim();

    if (logs === "") {
        alert("Please paste logs first.");
        return;
    }

    document.getElementById("answer").innerHTML =
        "<h3>Processing pasted logs...</h3>";

    try {

        const response = await fetch("/paste", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                logs: logs
            })

        });

        const data = await response.json();

        document.getElementById("answer").innerHTML = `
            <h2>✅ Logs Processed</h2>

            <p><strong>Status:</strong> ${data.message}</p>

            <p><strong>Total Chunks:</strong> ${data.chunks}</p>

            <hr>

            <p>You can now ask questions.</p>
        `;

    } catch (error) {

        console.error(error);

        document.getElementById("answer").innerHTML =
            "<h3 style='color:red;'>Processing failed.</h3>";
    }

};


// =======================================
// Ask Question
// =======================================
document.getElementById("askBtn").onclick = async () => {

    const question = document.getElementById("question").value.trim();

    if (question === "") {
        alert("Please enter a question.");
        return;
    }

    document.getElementById("answer").innerHTML =
        "<h3>Analyzing logs...</h3>";

    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        const data = await response.json();

        let html = `
            <h2>Answer</h2>

            <div style="
                background:#f7f7f7;
                padding:15px;
                border-radius:8px;
                margin-bottom:20px;
            ">
                ${data.answer.replace(/\n/g, "<br>")}
            </div>

            <hr>

            <h2>Retrieved Chunks (${data.sources.length})</h2>
        `;

        data.sources.forEach((source, index) => {

            html += `
                <div style="
                    border:1px solid #ddd;
                    border-radius:8px;
                    padding:15px;
                    margin-bottom:15px;
                    background:#fafafa;
                ">

                    <h3>Chunk ${index + 1}</h3>

                    <p>
                        <strong>Source:</strong>
                        ${source.metadata.source || "Unknown"}
                    </p>

                    <pre style="
                        white-space:pre-wrap;
                        overflow-x:auto;
                        background:white;
                        padding:10px;
                    ">${source.content}</pre>

                </div>
            `;
        });

        document.getElementById("answer").innerHTML = html;

    } catch (error) {

        console.error(error);

        document.getElementById("answer").innerHTML =
            "<h3 style='color:red;'>Failed to analyze logs.</h3>";
    }

};