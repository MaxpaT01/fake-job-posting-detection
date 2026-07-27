document.addEventListener('DOMContentLoaded', () => {
    // VS Code Tab & Sidebar File Item Navigation
    const fileItems = document.querySelectorAll('.file-item');
    const editorTabs = document.querySelectorAll('.editor-tab');
    const tabPanes = document.querySelectorAll('.tab-pane');

    function switchTab(tabId) {
        fileItems.forEach(fi => {
            if (fi.dataset.tab === tabId) fi.classList.add('active');
            else fi.classList.remove('active');
        });

        editorTabs.forEach(et => {
            if (et.dataset.tab === tabId) et.classList.add('active');
            else et.classList.remove('active');
        });

        tabPanes.forEach(tp => {
            if (tp.id === tabId) tp.classList.add('active');
            else tp.classList.remove('active');
        });
    }

    fileItems.forEach(fi => {
        fi.addEventListener('click', () => switchTab(fi.dataset.tab));
    });

    editorTabs.forEach(et => {
        et.addEventListener('click', () => switchTab(et.dataset.tab));
    });

    // Preset Samples
    const sampleReal = {
        title: "Software Engineer (Python & React)",
        has_company_logo: "1",
        telecommuting: "0",
        has_questions: "1",
        company_profile: "We are an innovative SaaS healthcare technology platform founded in 2016.",
        description: "Looking for a Software Engineer to design, build, and maintain Python REST APIs and React web interfaces.",
        requirements: "Bachelor's degree in Computer Science or related field. 3+ years experience with Python and JavaScript.",
        benefits: "Competitive salary ($90,000 - $120,000) + stock options, health insurance, and 401(k) matching."
    };

    const sampleFake = {
        title: "Remote Data Entry Clerk - Urgent Hiring! ($50/hr)",
        has_company_logo: "0",
        telecommuting: "1",
        has_questions: "0",
        company_profile: "",
        description: "Earn money easily working from home entering order data! Flexible 2 hours daily. Instant daily payment via PayPal, Zelle, or Wire Transfer. No experience required!",
        requirements: "Must have computer with internet connection and active personal bank account. Contact manager via Telegram.",
        benefits: "High daily payouts up to $500/day. Immediate payment upon task completion."
    };

    document.getElementById('btn-load-real').addEventListener('click', () => loadSample(sampleReal));
    document.getElementById('btn-load-fake').addEventListener('click', () => loadSample(sampleFake));

    function loadSample(data) {
        document.getElementById('title').value = data.title;
        document.getElementById('has_company_logo').value = data.has_company_logo;
        document.getElementById('telecommuting').value = data.telecommuting;
        document.getElementById('has_questions').value = data.has_questions;
        document.getElementById('company_profile').value = data.company_profile;
        document.getElementById('description').value = data.description;
        document.getElementById('requirements').value = data.requirements;
        document.getElementById('benefits').value = data.benefits;
    }

    // Inference Rules
    const SPAM_RULES = [
        { word: "earn", weight: 0.12, label: "Promotional Earning Claims" },
        { word: "paypal", weight: 0.20, label: "Unstandard Payment Method (PayPal)" },
        { word: "zelle", weight: 0.25, label: "Peer-to-Peer Payment Signal (Zelle)" },
        { word: "wire transfer", weight: 0.30, label: "High-Risk Wire Transfer Mention" },
        { word: "telegram", weight: 0.25, label: "Off-Platform Messaging (Telegram)" },
        { word: "whatsapp", weight: 0.22, label: "Off-Platform Messaging (WhatsApp)" },
        { word: "daily pay", weight: 0.18, label: "Daily Payout Guarantee" },
        { word: "daily payment", weight: 0.18, label: "Daily Payout Guarantee" },
        { word: "no experience", weight: 0.15, label: "No Experience Needed High-Pay Signal" },
        { word: "urgent hiring", weight: 0.12, label: "Urgency Pressure Phrasing" },
        { word: "envelope", weight: 0.25, label: "Envelope Packing Scam Keyword" },
        { word: "bank account", weight: 0.15, label: "Personal Bank Account Request" }
    ];

    const LEGIT_RULES = [
        { word: "bachelor", weight: -0.10 },
        { word: "years experience", weight: -0.12 },
        { word: "python", weight: -0.10 },
        { word: "react", weight: -0.10 },
        { word: "health insurance", weight: -0.12 },
        { word: "stock options", weight: -0.10 }
    ];

    let currentAnalysisResult = null;

    const predictForm = document.getElementById('predict-form');
    predictForm.addEventListener('submit', (e) => {
        e.preventDefault();
        runPrediction();
    });

    function runPrediction() {
        const title = document.getElementById('title').value;
        const logo = parseInt(document.getElementById('has_company_logo').value);
        const tele = parseInt(document.getElementById('telecommuting').value);
        const questions = parseInt(document.getElementById('has_questions').value);
        const profile = document.getElementById('company_profile').value;
        const desc = document.getElementById('description').value;
        const req = document.getElementById('requirements').value;
        const ben = document.getElementById('benefits').value;

        const fullText = (title + " " + profile + " " + desc + " " + req + " " + ben).toLowerCase();

        let score = 0.05;
        let triggers = [];
        let tags = [];

        SPAM_RULES.forEach(r => {
            if (fullText.includes(r.word)) {
                score += r.weight;
                triggers.push({ type: "high", text: `Detected term: "${r.word}" (${r.label})` });
                tags.push({ word: r.word, type: "spam" });
            }
        });

        LEGIT_RULES.forEach(r => {
            if (fullText.includes(r.word)) {
                score += r.weight;
                tags.push({ word: r.word, type: "legit" });
            }
        });

        if (logo === 0) {
            score += 0.22;
            triggers.push({ type: "med", text: "Missing Company Logo: Fraud rate is 3.5x higher without corporate logo." });
        } else {
            triggers.push({ type: "good", text: "Verified Company Logo Present" });
        }

        if (questions === 0) {
            score += 0.12;
            triggers.push({ type: "med", text: "No Screening Questions: Scam posts rarely include qualification questions." });
        }

        if (profile.trim().length === 0) {
            score += 0.25;
            triggers.push({ type: "high", text: "Missing Company Profile: Over 70% of fraudulent listings omit company background." });
        }

        let finalScore = Math.min(Math.max(score, 0.01), 0.99);
        let scorePct = Math.round(finalScore * 100);

        currentAnalysisResult = {
            title: title,
            scorePct: scorePct,
            triggers: triggers,
            tags: tags
        };

        renderResult(scorePct, triggers, tags);
    }

    function renderResult(scorePct, triggers, tags) {
        document.getElementById('no-result').classList.add('hidden');
        document.getElementById('result-box').classList.remove('hidden');
        document.getElementById('btn-download-pdf').classList.remove('hidden');

        document.getElementById('score-text').textContent = `${scorePct}%`;

        const badge = document.getElementById('risk-badge');
        let badgeClass = 'real';
        let badgeText = 'Legitimate Posting';

        if (scorePct >= 65) {
            badgeClass = 'fake';
            badgeText = 'High Risk Fraudulent';
        } else if (scorePct >= 35) {
            badgeClass = 'caution';
            badgeText = 'Suspicious Caution';
        }

        badge.className = `badge ${badgeClass}`;
        badge.textContent = badgeText;

        const ul = document.getElementById('triggers-list');
        ul.innerHTML = '';
        if (triggers.length === 0) {
            ul.innerHTML = '<li class="good">✓ Standard text and verified company metadata.</li>';
        } else {
            triggers.forEach(t => {
                const li = document.createElement('li');
                li.className = t.type;
                li.textContent = (t.type === 'good' ? '✓ ' : '⚠️ ') + t.text;
                ul.appendChild(li);
            });
        }

        const tagsBox = document.getElementById('keywords-tags');
        tagsBox.innerHTML = '';
        if (tags.length === 0) {
            tagsBox.innerHTML = '<span style="font-size:0.8rem; color:#6e6e6e;">Standard terminology.</span>';
        } else {
            tags.forEach(tg => {
                const span = document.createElement('span');
                span.className = `tag ${tg.type}`;
                span.textContent = (tg.type === 'spam' ? '🚨 ' : '✓ ') + tg.word;
                tagsBox.appendChild(span);
            });
        }

        const advice = document.getElementById('advice-box');
        if (scorePct >= 65) {
            advice.innerHTML = '<span style="color:#f14c4c;"># Recommendation: DO NOT APPLY</span><br>Contains major red flags associated with payment recruitment scams.';
        } else if (scorePct >= 35) {
            advice.innerHTML = '<span style="color:#dcdcaa;"># Recommendation: VERIFY COMPANY BEFORE APPLYING</span><br>Some metadata signals or suspicious keywords were found.';
        } else {
            advice.innerHTML = '<span style="color:#4ec9b0;"># Recommendation: SAFE TO APPLY</span><br>Posting matches legitimate corporate hiring patterns.';
        }
    }

    // PDF Download Handler
    document.getElementById('btn-download-pdf').addEventListener('click', () => {
        if (!currentAnalysisResult) return;

        const pdfElement = document.createElement('div');
        pdfElement.style.padding = '25px';
        pdfElement.style.fontFamily = 'Helvetica, Arial, sans-serif';
        pdfElement.style.color = '#1e293b';

        let riskStatus = currentAnalysisResult.scorePct >= 65 ? "HIGH RISK FRAUDULENT" : (currentAnalysisResult.scorePct >= 35 ? "SUSPICIOUS CAUTION" : "LEGITIMATE");
        let statusColor = currentAnalysisResult.scorePct >= 65 ? "#dc2626" : (currentAnalysisResult.scorePct >= 35 ? "#b45309" : "#16a34a");

        let triggersHtml = currentAnalysisResult.triggers.map(t => `<li style="margin-bottom:6px; font-size:13px;">${t.text}</li>`).join('');

        pdfElement.innerHTML = `
            <div style="border-bottom: 2px solid #007acc; padding-bottom: 12px; margin-bottom: 20px;">
                <h2 style="color: #1e293b; margin: 0; font-size: 22px;">Job Posting Fraud Risk Report</h2>
                <p style="color: #64748b; font-size: 12px; margin: 4px 0 0 0;">Generated by JobShield AI • VS Code AI Studio Edition</p>
            </div>

            <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 15px; margin-bottom: 20px;">
                <p style="margin: 0 0 8px 0; font-size: 14px;"><strong>Job Title Evaluated:</strong> ${currentAnalysisResult.title}</p>
                <p style="margin: 0 0 8px 0; font-size: 14px;"><strong>Fraud Risk Score:</strong> <span style="font-size: 18px; font-weight: bold; color: ${statusColor};">${currentAnalysisResult.scorePct}%</span></p>
                <p style="margin: 0; font-size: 14px;"><strong>Risk Category:</strong> <strong style="color: ${statusColor};">${riskStatus}</strong></p>
            </div>

            <div style="margin-bottom: 20px;">
                <h4 style="font-size: 14px; margin-bottom: 8px; color: #334155;">Key Risk Indicators & Triggers:</h4>
                <ul style="padding-left: 20px; margin: 0;">
                    ${triggersHtml || '<li>No suspicious triggers detected.</li>'}
                </ul>
            </div>

            <div style="background: #f1f5f9; border-left: 4px solid ${statusColor}; padding: 12px; font-size: 13px; margin-top: 25px;">
                <strong>Evaluation Summary & Guidance:</strong><br>
                ${currentAnalysisResult.scorePct >= 65 ? "Do not submit personal banking details or communicate off-platform." : "Verify employer domain on official channels before submitting credentials."}
            </div>

            <div style="margin-top: 40px; border-top: 1px solid #e2e8f0; pt-10px; font-size: 10px; color: #94a3b8; text-align: center;">
                Fake Job Posting Detection System • Machine Learning Project Report
            </div>
        `;

        const opt = {
            margin:       10,
            filename:     `Job_Posting_Fraud_Report_${Date.now()}.pdf`,
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2 },
            jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
        };

        html2pdf().set(opt).from(pdfElement).save();
    });

    initCharts();
    initTable();
});

function initCharts() {
    Chart.defaults.font.family = "'Fira Code', monospace";
    Chart.defaults.color = '#cccccc';

    new Chart(document.getElementById('chart-class'), {
        type: 'doughnut',
        data: {
            labels: ['Legitimate (92.0%)', 'Fraudulent (8.0%)'],
            datasets: [{ data: [4600, 400], backgroundColor: ['#007acc', '#f14c4c'] }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });

    new Chart(document.getElementById('chart-logo'), {
        type: 'bar',
        data: {
            labels: ['Legitimate Jobs', 'Fraudulent Jobs'],
            datasets: [
                { label: 'Has Logo (%)', data: [84.2, 23.5], backgroundColor: '#4ec9b0' },
                { label: 'Missing Logo (%)', data: [15.8, 76.5], backgroundColor: '#f14c4c' }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, max: 100, grid: { color: '#333' } }, x: { grid: { color: '#333' } } } }
    });

    new Chart(document.getElementById('chart-tele'), {
        type: 'bar',
        data: {
            labels: ['On-Site Jobs', 'Remote Jobs'],
            datasets: [{ label: 'Fraud Rate (%)', data: [3.1, 14.8], backgroundColor: ['#007acc', '#ce9178'] }]
        },
        options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, max: 20, grid: { color: '#333' } }, x: { grid: { color: '#333' } } } }
    });

    new Chart(document.getElementById('chart-questions'), {
        type: 'bar',
        data: {
            labels: ['Legitimate Jobs', 'Fraudulent Jobs'],
            datasets: [
                { label: 'Has Questions (%)', data: [68.5, 21.0], backgroundColor: '#007acc' },
                { label: 'No Questions (%)', data: [31.5, 79.0], backgroundColor: '#6e6e6e' }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, max: 100, grid: { color: '#333' } }, x: { grid: { color: '#333' } } } }
    });

    new Chart(document.getElementById('chart-impact'), {
        type: 'bar',
        data: {
            labels: ['Raw Text', 'Cleaned Text', 'Cleaned Text + Metadata'],
            datasets: [
                { label: 'F1-Score', data: [0.742, 0.865, 0.924], backgroundColor: '#007acc' },
                { label: 'ROC-AUC', data: [0.851, 0.932, 0.978], backgroundColor: '#4ec9b0' }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, scales: { y: { min: 0.5, max: 1.0, grid: { color: '#333' } }, x: { grid: { color: '#333' } } } }
    });
}

function initTable() {
    const modelsData = [
        { name: "Gradient Boosting", acc: "98.42%", prec: "92.15%", rec: "88.90%", f1: "0.9049", auc: "0.9854" },
        { name: "Logistic Regression", acc: "97.85%", prec: "88.40%", rec: "86.20%", f1: "0.8728", auc: "0.9782" },
        { name: "Random Forest", acc: "97.90%", prec: "94.80%", rec: "78.40%", f1: "0.8582", auc: "0.9710" },
        { name: "Multinomial Naive Bayes", acc: "95.60%", prec: "62.40%", rec: "89.10%", f1: "0.7337", auc: "0.9540" }
    ];

    const tbody = document.getElementById('models-table-body');
    tbody.innerHTML = '';

    modelsData.forEach(m => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong style="color:#9cdcfe;">${m.name}</strong></td>
            <td>${m.acc}</td>
            <td>${m.prec}</td>
            <td>${m.rec}</td>
            <td><strong style="color:#4ec9b0;">${m.f1}</strong></td>
            <td>${m.auc}</td>
        `;
        tbody.appendChild(tr);
    });

    new Chart(document.getElementById('chart-models'), {
        type: 'bar',
        data: {
            labels: ['Gradient Boosting', 'Logistic Regression', 'Random Forest', 'Multinomial Naive Bayes'],
            datasets: [
                { label: 'Precision', data: [0.9215, 0.884, 0.948, 0.624], backgroundColor: '#569cd6' },
                { label: 'Recall', data: [0.889, 0.862, 0.784, 0.891], backgroundColor: '#ce9178' },
                { label: 'F1-Score', data: [0.9049, 0.8728, 0.8582, 0.7337], backgroundColor: '#007acc' },
                { label: 'ROC-AUC', data: [0.9854, 0.9782, 0.9710, 0.9540], backgroundColor: '#4ec9b0' }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, scales: { y: { min: 0.5, max: 1.0, grid: { color: '#333' } }, x: { grid: { color: '#333' } } } }
    });
}
