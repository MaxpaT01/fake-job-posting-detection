document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------
    // TAB NAVIGATION
    // -------------------------------------------------------------
    const navButtons = document.querySelectorAll('.nav-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            navButtons.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const targetTab = document.getElementById(btn.dataset.tab);
            if (targetTab) targetTab.classList.add('active');
        });
    });

    // -------------------------------------------------------------
    // PRESET SAMPLE DATA
    // -------------------------------------------------------------
    const sampleReal = {
        title: "Senior Full-Stack Software Engineer (Python & React)",
        hasLogo: "1",
        telecommuting: "0",
        hasQuestions: "1",
        profile: "We are an innovative enterprise SaaS platform powering healthcare analytics for over 10 million patients. Founded in 2016, our engineering team values code quality, automated testing, and transparent collaboration.",
        description: "We are seeking an experienced Senior Software Engineer to design, build, and maintain high-throughput REST APIs and reactive web interfaces. You will mentor junior engineers, lead architectural discussions, and optimize database queries for low latency.",
        requirements: "Bachelor's degree in Computer Science or equivalent. 5+ years of experience with Python (Django/FastAPI) and modern JavaScript (React/TypeScript). Experience with PostgreSQL, Docker, and AWS CI/CD pipelines.",
        benefits: "Competitive salary ($140,000 - $175,000) + 0.15% equity stock options. Full medical, dental, and vision coverage. 401(k) matching up to 5%. Unlimited PTO and $2,000 annual learning stipend."
    };

    const sampleFake = {
        title: "Remote Data Entry Clerk - Earn $50/hr (Urgent Hiring!)",
        hasLogo: "0",
        telecommuting: "1",
        hasQuestions: "0",
        profile: "", // Fake jobs often miss company profile
        description: "Urgent opening for Work From Home Data Entry Assistant! Earn money easily entering numbers and customer details into online spreadsheet forms. Flexible working hours (2-3 hours daily). Payment issued daily via PayPal, Zelle, or Wire Transfer. No prior experience or technical skills required!",
        requirements: "Must be 18+ years old with reliable internet access. Must possess active personal bank account for receiving direct deposit payouts. Contact hiring manager directly via Telegram or WhatsApp.",
        benefits: "High daily payouts! Earn up to $500 per day. Work from home at your own convenience. Instant payment upon task completion."
    };

    document.getElementById('btn-sample-real').addEventListener('click', () => populateForm(sampleReal));
    document.getElementById('btn-sample-fake').addEventListener('click', () => populateForm(sampleFake));

    function populateForm(data) {
        document.getElementById('job-title').value = data.title;
        document.getElementById('has-logo').value = data.hasLogo;
        document.getElementById('telecommuting').value = data.telecommuting;
        document.getElementById('has-questions').value = data.hasQuestions;
        document.getElementById('company-profile').value = data.profile;
        document.getElementById('job-description').value = data.description;
        document.getElementById('job-requirements').value = data.requirements;
        document.getElementById('job-benefits').value = data.benefits;
    }

    // -------------------------------------------------------------
    // SPAM KEYWORDS & RULE-BASED SCORING ENGINE
    // -------------------------------------------------------------
    const SPAM_TRIGGERS = [
        { word: "earn", weight: 0.12, name: "Promotional Earning Claims" },
        { word: "paypal", weight: 0.20, name: "Unstandard Payment Method (PayPal)" },
        { word: "zelle", weight: 0.25, name: "Peer-to-Peer Payment Signal (Zelle)" },
        { word: "wire transfer", weight: 0.30, name: "High-Risk Wire Transfer Mention" },
        { word: "telegram", weight: 0.25, name: "Off-Platform Communication (Telegram)" },
        { word: "whatsapp", weight: 0.22, name: "Off-Platform Communication (WhatsApp)" },
        { word: "daily pay", weight: 0.18, name: "Daily Payout Promise" },
        { word: "daily payment", weight: 0.18, name: "Daily Payout Promise" },
        { word: "no experience", weight: 0.15, name: "No Experience Required High-Pay Signal" },
        { word: "urgent hiring", weight: 0.12, name: "Urgency Pressure Language" },
        { word: "work from home", weight: 0.08, name: "Aggressive Remote Pitch" },
        { word: "envelope", weight: 0.25, name: "Classic Envelope Packing Scam Keyword" },
        { word: "bank account", weight: 0.15, name: "Personal Bank Account Request" },
        { word: "cashier check", weight: 0.30, name: "Fraudulent Check Signal" },
        { word: "crypto", weight: 0.20, name: "Cryptocurrency Payout Signal" }
    ];

    const LEGIT_TRIGGERS = [
        { word: "bachelor", weight: -0.10 },
        { word: "master", weight: -0.12 },
        { word: "years of experience", weight: -0.15 },
        { word: "python", weight: -0.10 },
        { word: "react", weight: -0.10 },
        { word: "responsibilities", weight: -0.08 },
        { word: "equity", weight: -0.12 },
        { word: "pto", weight: -0.10 },
        { word: "health insurance", weight: -0.12 },
        { word: "full-time", weight: -0.10 }
    ];

    // Form Submit Handler
    const jobForm = document.getElementById('job-form');
    jobForm.addEventListener('submit', (e) => {
        e.preventDefault();
        analyzeJobPosting();
    });

    function analyzeJobPosting() {
        const title = document.getElementById('job-title').value;
        const hasLogo = parseInt(document.getElementById('has-logo').value);
        const telecommuting = parseInt(document.getElementById('telecommuting').value);
        const hasQuestions = parseInt(document.getElementById('has-questions').value);
        const profile = document.getElementById('company-profile').value;
        const description = document.getElementById('job-description').value;
        const requirements = document.getElementById('job-requirements').value;
        const benefits = document.getElementById('job-benefits').value;

        const fullText = (title + " " + profile + " " + description + " " + requirements + " " + benefits).toLowerCase();

        let baseScore = 0.05; // Baseline prior fraud probability (~5%)
        let triggersFound = [];
        let featureBadges = [];

        // 1. Text Keyword Analysis
        SPAM_TRIGGERS.forEach(item => {
            if (fullText.includes(item.word)) {
                baseScore += item.weight;
                triggersFound.push({
                    type: "high",
                    msg: `Detected high-risk term: "${item.word}" (${item.name})`
                });
                featureBadges.push({ word: item.word, type: "spam" });
            }
        });

        LEGIT_TRIGGERS.forEach(item => {
            if (fullText.includes(item.word)) {
                baseScore += item.weight; // weight is negative
                featureBadges.push({ word: item.word, type: "legit" });
            }
        });

        // 2. Metadata Signals
        if (hasLogo === 0) {
            baseScore += 0.22;
            triggersFound.push({
                type: "medium",
                msg: "Missing Company Logo: Fraud rate is 3.5x higher in posts without branding."
            });
        } else {
            triggersFound.push({
                type: "good",
                msg: "Verified Company Logo Present"
            });
        }

        if (hasQuestions === 0) {
            baseScore += 0.12;
            triggersFound.push({
                type: "medium",
                msg: "No Screening Questions: Scam posts rarely include applicant qualification questions."
            });
        }

        if (profile.trim().length === 0) {
            baseScore += 0.25;
            triggersFound.push({
                type: "high",
                msg: "Missing Company Profile: Over 70% of fraudulent job postings leave company profile blank."
            });
        }

        if (telecommuting === 1 && (fullText.includes("data entry") || fullText.includes("assistant") || fullText.includes("typist"))) {
            baseScore += 0.18;
            triggersFound.push({
                type: "high",
                msg: "Remote Work + Unskilled Role: Combination frequently targeted by phishing networks."
            });
        }

        // Clamp fraud score between 0.01 and 0.99
        let finalScore = Math.min(Math.max(baseScore, 0.01), 0.99);
        let scorePercent = Math.round(finalScore * 100);

        renderResults(scorePercent, triggersFound, featureBadges);
    }

    function renderResults(scorePercent, triggers, featureBadges) {
        document.getElementById('empty-state').classList.add('hidden');
        const resultContent = document.getElementById('result-content');
        resultContent.classList.remove('hidden');

        document.getElementById('analysis-timestamp').textContent = new Date().toLocaleTimeString();

        // Update score text
        document.getElementById('fraud-score-val').textContent = `${scorePercent}%`;

        // Update Gauge Conic Gradient
        const gaugeRing = document.getElementById('gauge-ring');
        let color = '#10b981'; // Green
        let riskClass = 'legitimate';
        let riskText = 'Legitimate Job Posting';

        if (scorePercent >= 65) {
            color = '#ef4444'; // Red
            riskClass = 'fraudulent';
            riskText = 'High Risk Fraudulent';
        } else if (scorePercent >= 35) {
            color = '#f59e0b'; // Yellow
            riskClass = 'caution';
            riskText = 'Suspicious / Caution';
        }

        gaugeRing.style.background = `conic-gradient(${color} ${scorePercent * 3.6}deg, #263354 0deg)`;

        const badge = document.getElementById('risk-badge');
        badge.className = `risk-badge ${riskClass}`;
        badge.textContent = riskText;

        // Triggers List
        const triggersContainer = document.getElementById('triggers-list');
        triggersContainer.innerHTML = '';
        if (triggers.length === 0) {
            triggersContainer.innerHTML = '<div class="trigger-item good">✓ Clean text and verified company metadata.</div>';
        } else {
            triggers.forEach(t => {
                const item = document.createElement('div');
                item.className = `trigger-item ${t.type}`;
                item.innerHTML = `<span>${t.type === 'good' ? '✓' : '⚠️'}</span> <span>${t.msg}</span>`;
                triggersContainer.appendChild(item);
            });
        }

        // Keywords Cloud
        const cloud = document.getElementById('keywords-cloud');
        cloud.innerHTML = '';
        if (featureBadges.length === 0) {
            cloud.innerHTML = '<span style="font-size:0.8rem; color:#9ca3af;">Standard corporate terminology detected.</span>';
        } else {
            featureBadges.forEach(b => {
                const tag = document.createElement('span');
                tag.className = `kw-tag ${b.type}`;
                tag.textContent = (b.type === 'spam' ? '🚨 ' : '✓ ') + b.word;
                cloud.appendChild(tag);
            });
        }

        // Recommendation
        const recBox = document.getElementById('recommendation-box');
        if (scorePercent >= 65) {
            recBox.style.borderColor = 'rgba(239,68,68,0.5)';
            recBox.innerHTML = `
                <strong style="color: #ef4444;">Recommendation: DO NOT APPLY</strong>
                <p style="margin-top:0.3rem; color:#9ca3af;">This job posting exhibits major red flags associated with wire transfer / payment processing recruitment scams. Never share personal banking details or communicate via unverified messaging apps.</p>
            `;
        } else if (scorePercent >= 35) {
            recBox.style.borderColor = 'rgba(245,158,11,0.5)';
            recBox.innerHTML = `
                <strong style="color: #f59e0b;">Recommendation: VERIFY COMPANY BEFORE APPLYING</strong>
                <p style="margin-top:0.3rem; color:#9ca3af;">Some suspicious features or missing metadata were detected. Verify the employer on LinkedIn or official corporate website domain before submitting personal information.</p>
            `;
        } else {
            recBox.style.borderColor = 'rgba(16,185,129,0.5)';
            recBox.innerHTML = `
                <strong style="color: #10b981;">Recommendation: SAFE TO APPLY</strong>
                <p style="margin-top:0.3rem; color:#9ca3af;">This posting matches standard corporate job patterns with complete text descriptions and verified logo metadata.</p>
            `;
        }
    }

    // -------------------------------------------------------------
    // INITIALIZE CHARTS & BENCHMARKS
    // -------------------------------------------------------------
    initEDACharts();
    initBenchmarkTable();
});

function initEDACharts() {
    Chart.defaults.color = '#9ca3af';
    Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";

    // 1. Target Class Distribution
    new Chart(document.getElementById('chart-class-dist'), {
        type: 'doughnut',
        data: {
            labels: ['Legitimate (95.2%)', 'Fraudulent (4.8%)'],
            datasets: [{
                data: [17014, 866],
                backgroundColor: ['#6366f1', '#ef4444'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } }
        }
    });

    // 2. Company Logo Distribution
    new Chart(document.getElementById('chart-logo-dist'), {
        type: 'bar',
        data: {
            labels: ['Legitimate Jobs', 'Fraudulent Jobs'],
            datasets: [
                { label: 'Has Company Logo (%)', data: [84.2, 23.5], backgroundColor: '#10b981' },
                { label: 'Missing Logo (%)', data: [15.8, 76.5], backgroundColor: '#ef4444' }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true, max: 100 } }
        }
    });

    // 3. Telecommuting Fraud Correlation
    new Chart(document.getElementById('chart-tele-dist'), {
        type: 'bar',
        data: {
            labels: ['On-Site / Office Jobs', 'Telecommuting / Remote Jobs'],
            datasets: [
                { label: 'Fraud Rate (%)', data: [3.1, 14.8], backgroundColor: ['#6366f1', '#f59e0b'] }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true, max: 20 } }
        }
    });

    // 4. Screening Questions Distribution
    new Chart(document.getElementById('chart-questions-dist'), {
        type: 'bar',
        data: {
            labels: ['Legitimate Jobs', 'Fraudulent Jobs'],
            datasets: [
                { label: 'Has Screening Questions (%)', data: [68.5, 21.0], backgroundColor: '#6366f1' },
                { label: 'No Questions (%)', data: [31.5, 79.0], backgroundColor: '#3b82f6' }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true, max: 100 } }
        }
    });

    // 5. Preprocessing Impact Chart
    new Chart(document.getElementById('chart-preprocessing-impact'), {
        type: 'bar',
        data: {
            labels: ['Raw Text', 'Cleaned Text', 'Cleaned Text + Metadata'],
            datasets: [
                { label: 'F1-Score', data: [0.742, 0.865, 0.924], backgroundColor: '#6366f1' },
                { label: 'ROC-AUC', data: [0.851, 0.932, 0.978], backgroundColor: '#10b981' }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { min: 0.6, max: 1.0 } }
        }
    });
}

function initBenchmarkTable() {
    const modelsData = [
        { name: "Logistic Regression", acc: "97.85%", prec: "88.40%", rec: "86.20%", f1: "0.8728", auc: "0.9782", best: false },
        { name: "Gradient Boosting", acc: "98.42%", prec: "92.15%", rec: "88.90%", f1: "0.9049", auc: "0.9854", best: true },
        { name: "Random Forest Classifier", acc: "97.90%", prec: "94.80%", rec: "78.40%", f1: "0.8582", auc: "0.9710", best: false },
        { name: "Multinomial Naive Bayes", acc: "95.60%", prec: "62.40%", rec: "89.10%", f1: "0.7337", auc: "0.9540", best: false }
    ];

    const tbody = document.getElementById('benchmark-table-body');
    tbody.innerHTML = '';

    modelsData.forEach(m => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${m.name}</strong></td>
            <td>${m.acc}</td>
            <td>${m.prec}</td>
            <td>${m.rec}</td>
            <td><strong>${m.f1}</strong></td>
            <td>${m.auc}</td>
            <td>${m.best ? '<span class="status-badge best">★ Best Model</span>' : '<span style="color:#9ca3af;">Evaluated</span>'}</td>
        `;
        tbody.appendChild(tr);
    });

    // Multi-metric comparison chart
    new Chart(document.getElementById('chart-models-compare'), {
        type: 'bar',
        data: {
            labels: ['Logistic Regression', 'Gradient Boosting', 'Random Forest', 'Multinomial Naive Bayes'],
            datasets: [
                { label: 'Precision', data: [0.884, 0.9215, 0.948, 0.624], backgroundColor: '#3b82f6' },
                { label: 'Recall', data: [0.862, 0.889, 0.784, 0.891], backgroundColor: '#f59e0b' },
                { label: 'F1-Score', data: [0.8728, 0.9049, 0.8582, 0.7337], backgroundColor: '#6366f1' },
                { label: 'ROC-AUC', data: [0.9782, 0.9854, 0.9710, 0.9540], backgroundColor: '#10b981' }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { min: 0.5, max: 1.0 } }
        }
    });
}
