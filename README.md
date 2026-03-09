# 🎓 Oracle Student Payment System

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Oracle](https://img.shields.io/badge/Oracle_DB-F80000?style=for-the-badge&logo=oracle&logoColor=white)
![cx_Oracle](https://img.shields.io/badge/cx__Oracle-Python_Driver-F80000?style=for-the-badge)

> A Python-based student payment and enrollment management system powered by Oracle Database — designed for academic institutions to track tuition fees, payments, and enrollment status.

---

## 🎯 Overview

This system provides a complete backend for managing student financial records in a university context. It demonstrates integration between Python and Oracle DB using stored procedures, triggers, and complex query optimization.

---

## ✨ Features

- 📋 **Student Registration** — Enroll students with complete academic and financial profiles
- 💰 **Payment Tracking** — Record, validate, and query tuition and fee payments
- 📊 **Financial Reporting** — Generate summaries of paid/unpaid accounts per semester
- 🔔 **Automated Alerts** — Oracle triggers for overdue payment notifications
- 🔍 **Advanced Queries** — Complex SQL with joins, aggregations, and stored procedures
- 📤 **Data Export** — Export reports to CSV for administrative use

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.9+ |
| Database | Oracle Database (11g+) |
| ORM/Driver | cx_Oracle / python-oracledb |
| Reporting | Pandas, CSV export |

---

## 📁 Project Structure

```
Oracle-Student-Payment-System/
├── main.py                 # CLI entry point
├── config.py               # DB connection config
├── models/
│   ├── student.py          # Student model & CRUD
│   ├── payment.py          # Payment model & logic
│   └── enrollment.py       # Enrollment management
├── queries/
│   ├── reports.sql         # Pre-built reporting queries
│   └── procedures.sql      # Stored procedures & triggers
├── utils/
│   ├── db_connection.py    # Oracle connection pool
│   └── exporter.py         # CSV/report export
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites

```bash
# Python dependencies
pip install cx_Oracle pandas python-dotenv

# Oracle Instant Client required
# Download from: https://www.oracle.com/database/technologies/instant-client.html
```

### Configuration

```python
# config.py
DB_USER = "your_user"
DB_PASSWORD = "your_password"
DB_DSN = "localhost:1521/XEPDB1"  # or your Oracle DSN
```

### Run

```bash
python main.py
```

---

## 🗄️ Key Database Objects

```sql
-- Example: Payment status trigger
CREATE OR REPLACE TRIGGER check_payment_deadline
AFTER INSERT ON PAYMENTS
FOR EACH ROW
BEGIN
  IF :NEW.amount < :NEW.required_amount THEN
    -- Insert notification record
    INSERT INTO ALERTS (student_id, message, created_at)
    VALUES (:NEW.student_id, 'Partial payment detected', SYSDATE);
  END IF;
END;
```

---

## 📊 Sample Queries

```python
# Get all students with overdue payments
query = """
    SELECT s.name, s.student_id, p.due_date, p.amount_due - p.amount_paid AS balance
    FROM STUDENTS s
    JOIN PAYMENTS p ON s.student_id = p.student_id
    WHERE p.due_date < SYSDATE AND p.amount_paid < p.amount_due
    ORDER BY balance DESC
"""
```

---

## 👤 Author

**Adil Chagri** — [github.com/Adilchagri](https://github.com/Adilchagri)
**Jbel Chouaib** — [github.com/Adilchagri](https://github.com/choua1b)

---

## 📄 License

MIT License
