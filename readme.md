# 🌸 Mamacare API – Women’s Personal Health Records System

Mamacare is a lightweight health record system designed to help women track, understand and manage their menstrual health. It provides a secure way to log, analyze, and generate a standardized medical report that can be shared with a doctor for better care.

This project is built with **Flask + Python** and designed to work both as a **standalone API** and as a **backend for a mobile/web app**.

---

## 🚨 The Problem

Many women:
- Don’t track their cycle consistently
- Forget important symptoms or events
- Have no **standardized document** to share with doctors
- Rely on inaccurate memory during medical visits

This leads to:
- Poor diagnosis
- Miscommunication with healthcare providers
- Delayed or inaccurate treatment

**Mamacare turns monthly experiences into structured medical history.**

---

## ✅ The Solution

Mamacare provides:
- Period & ovulation tracking
- Symptom logging (cramps, mood, headaches, etc.)
- Smart pattern detection
- **Doctor-ready PDF medical report**
- Safe and reusable health history

Users can request a **clinical-style PDF** containing:
- Cycle summary
- Symptom history
- Irregularities & risk signals
- Doctor notes section

This PDF can be shared directly with a healthcare professional.

---

## 🧠 Key Features

✅ Track period start and end dates  
✅ Log daily symptoms  
✅ Predict next cycle/ovulation  
✅ Generate standardized medical PDF  
✅ Secure, private, user-controlled data  
✅ Works offline-first (future feature)  
✅ Built for scalability (API architecture)

---

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **PDF Generation**: ReportLab
- **Database**: SQLite / PostgreSQL (Ready)
- **Hosting**: Render
- **Auth (optional)**: JWT
- **Environment**: Docker-ready

---

## 📁 Project Structure

```

mamacare/
│
├── app/
│   ├── app.py
│   ├── pdf_generator.py
│   ├── models.py
│   ├── routes/
│   └── utils/
│
├── reports/
│   └── sample_report.pdf
│
├── requirements.txt
├── render.yaml
└── README.md

````

---

## 🚀 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/mamacare.git
cd mamacare
````

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate          # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Locally

```bash
python app/app.py
```

App will start on:

```
http://127.0.0.1:5000
```

---

## ⚡ Key API Endpoints

| Method | Endpoint                  | Description             |
| ------ | ------------------------- | ----------------------- |
| POST   | `/log-cycle`              | Log period/cycle data   |
| POST   | `/log-symptoms`           | Log symptoms            |
| GET    | `/predict`                | Predict next cycle      |
| GET    | `/generate-pdf/<user_id>` | Generate medical PDF    |
| GET    | `/health`                 | Health check for Render |

---

## 📄 PDF Report Format (Doctor-Ready)

Each PDF contains:

**Patient Information**
**Cycle History**
**Symptom Trends**
**Irregular Pattern Alerts**
**Hormonal Flag Indicators**
**Physician Notes Section**

Designed for:

* OB/GYNs
* Midwives
* Fertility specialists
* General practitioners

---

## 🌍 Hosting on Render

**Start Command:**

```bash
gunicorn app.app:app
```

**Build Command:**

```bash
pip install -r requirements.txt
```

Render automatically sets the PORT (no need to specify it manually).

---

## 🧪 Demo Flow

1. User logs cycle
2. User logs symptoms
3. User requests report
4. Mamacare generates standardized medical PDF
5. Report is delivered + saved

This gives health professionals **actual usable data**.

---

## 🔮 Future Plans

* Mobile app (Flutter/React Native)
* AI-powered pattern recognition
* Fertility insights
* Mental health tracking
* Doctor portal access
* Email delivery of reports
* Offline local storage

---

## 🏆 Why Mamacare Will Win

This is not just another “period tracker”.

Mamacare is:
✅ Medical-grade
✅ Doctor-usable
✅ Data-structured
✅ Emotionally intuitive
✅ Built by empathy + engineering

> “Mamacare turns memory into medical insight.”

---

## 👨🏽‍💻 Author

**Oladosu Larinde**
Backend | Systems | ML/AI | HealthTech Innovator
Lagos, Nigeria 🇳🇬

GitHub: @Dosu333

---

## 📜 License

This project is licensed under the MIT License.

---

## ⭐ Support

If you believe in this mission, give this repo a ⭐️
Let’s improve women’s healthcare together.
```
