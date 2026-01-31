# 🎓 Oracle Student Payment System  
### A Modern Database-Driven Student Payment Management Platform

![Oracle](https://img.shields.io/badge/Database-Oracle-red)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b)
![PLSQL](https://img.shields.io/badge/PL%2FSQL-Advanced-green)

---

## 🚀 Overview

**Oracle Student Payment System** is a full-stack academic payment management platform designed to handle **student registration, payment tracking, financial risk analysis, and automated workflows** using **Oracle Database** and **PL/SQL**, with a modern **Streamlit-based Python interface**.

This project demonstrates **advanced database design**, **business logic automation**, and **real-world ERP-style architecture**, making it ideal for academic, enterprise, or portfolio use.

---

## ✨ Key Features

### 👨‍🎓 Student Management
- Register and manage student profiles
- Track academic and financial information
- Secure relational data modeling

### 💳 Payment Processing
- Record and validate student payments
- Automatic payment status updates (PAID / PENDING)
- Receipt generation logic

### ⚙️ Business Logic Automation (PL/SQL)
- Triggers to enforce data integrity
- Stored procedures for payment workflows
- Scheduled jobs for periodic financial checks

### 📊 Risk & Monitoring Dashboard
- Identify unpaid or late payments
- Financial risk indicators
- Real-time data visualization using Streamlit

### 🐳 Dockerized Oracle Environment
- Oracle 19c container for easy setup
- Reproducible local development environment

---

## 🏗️ Architecture

```
Frontend (Streamlit - Python)
        │
        ▼
Oracle Database (19c)
        │
        ├── Tables & Constraints
        ├── Triggers
        ├── Stored Procedures
        └── Scheduled Jobs
```

---

## 🛠️ Tech Stack

| Layer        | Technology |
|--------------|------------|
| Database     | Oracle 19c |
| Backend Logic| PL/SQL |
| Frontend     | Streamlit (Python) |
| DB Connector | python-oracledb |
| DevOps       | Docker |
| Language     | Python 3 |

---

## 📂 Project Structure

```
Oracle-Student-Payment-System/
├── app/
│   ├── app.py
│   └── fix_data.py
│
├── database/
│   └── setup_database.sql
│
├── docs/
│   └── Rapport_Projet.pdf
│
├── requirements.txt
└── README.md
```

---

## ⚡ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Adilchagri/Oracle-Student-Payment-System.git
cd Oracle-Student-Payment-System
```

### 2️⃣ Setup Oracle Database
- Run Oracle 19c using Docker
- Execute `setup_database.sql` to initialize schema and logic

### 3️⃣ Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application
```bash
streamlit run app/app.py
```

---

## 🎯 Use Cases

- University or school payment management
- ERP / academic system prototypes
- Learning advanced PL/SQL & Oracle
- Database-driven application demos
- Backend / database portfolio project

---

## 📈 Future Enhancements

- 🔐 Authentication & role-based access
- 📄 PDF invoice generation
- 📊 Advanced BI dashboards
- 🌐 REST API layer
- ☁️ Cloud deployment (OCI / AWS)

---

## 📄 Documentation

Detailed technical documentation is available in:

📘 `docs/Rapport_Projet.pdf`

---

## 👨‍💻 Author

**Adil Chagri**  
Database & Backend Enthusiast  
Oracle • PL/SQL • Python  

---

⭐ If you like this project, don’t forget to **star the repository**!
