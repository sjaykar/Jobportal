# 🧠 Jobportal with Chatbot (Flask + MySQL)

This is a complete job portal system built with **Flask**, **MySQL**, **HTML/CSS/JS**. It includes:
- A chatbot interface to guide users to job listings
- Separate pages for Tech, Non-Tech, and Other roles
- Admin dashboard to post/delete jobs and view applicants
- Job application form with real-time openings tracking

---



## ✅ Features

- 🧑‍💻 Chatbot UI to guide users to job categories
- 🔍 View available job listings based on category
- 📤 Apply for jobs – name, email, and role saved
- 🔢 Opening count decreases after each application
- ❌ Jobs disappear if openings = 0
- 🛠 Admin page to:
  - Post new jobs
  - View all applicants
  - See total openings per category
    

---

## ⚙️ Requirements

- Python 3.8+
- MySQL 5.7+
- Flask
- `mysql-connector-python`

Install dependencies:

```bash
pip install Flask mysql-connector-python

└── README.md # Project documentation (this file)

Setup the Database
mysql -u yourusername -p < schema.sql

Configure the Database Connection

import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",        # or IP address of your DB
        user="yourusername",
        password="yourpassword",
        database="jobportal"
    )

