# 🎓 Attendance Tracker — BML Munjal University

> Student Attendance Management System  
> Built with Python (Flask) + SQLite + HTML/CSS

---

## 📌 About

This is a web-based **Attendance Tracker** application developed for **BML Munjal University**.  
It allows teachers to manage student attendance digitally — mark present/absent, view reports, and export data as CSV.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏠 Dashboard | Mark today's attendance for all students |
| ➕ Add Students | Add students with Name, Roll No, Class |
| 📊 Reports | View attendance % for each student |
| 🚨 Alerts | Highlights students below 75% attendance |
| 📥 Export CSV | Download attendance data for Excel/Sheets |
| 🗑️ Delete | Remove students from the system |

---

## 🛠️ Tech Stack

- **Backend:** Python 3 + Flask
- **Database:** SQLite (auto-created on first run)
- **Frontend:** HTML5 + CSS3 + Vanilla JavaScript
- **Theme:** BML Munjal University (Navy Blue + Gold)

---

## 🚀 How to Run Locally

### Step 1 — Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/attendance-tracker.git
cd attendance-tracker
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run the app
```bash
python app.py
```

### Step 4 — Open in browser
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
attendance-tracker/
│
├── app.py                  # Flask backend (routes + DB logic)
├── attendance.db           # SQLite database (auto-created)
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── templates/
│   ├── index.html          # Dashboard / Home page
│   └── report.html         # Attendance Reports page
│
└── static/
    └── css/
        └── style.css       # Styling (BML Munjal theme)
```

---

## 📸 Pages

- **`/`** — Dashboard (mark attendance)
- **`/report`** — Attendance report with % bar
- **`/export_csv`** — Download CSV file

---

## 👨‍💻 Developer

Made by a student of **BML Munjal University**  
Department of Computer Science & Engineering

---

## 📄 License

This project is for educational purposes only.  
© 2025 BML Munjal University
