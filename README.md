# Football Eye ⚽

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-ultralytics-orange?logo=github&logoColor=white)
![Supervision](https://img.shields.io/badge/Supervision-ultralytics-yellow?logo=github&logoColor=black)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.x-purple?logo=pandas&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-black?logo=flask&logoColor=white)
![numpy](https://img.shields.io/badge/numpy-1.x-blue?logo=numpy&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript&logoColor=black)
![MariaDB](https://img.shields.io/badge/MariaDB-10.x-lightblue?logo=mariadb&logoColor=white)
![React](https://img.shields.io/badge/React-18.x-61DAFB?logo=react&logoColor=black)

> An web app based on Computer Vision for extracting statistics based on football matches video input 📊

---

# Repo Structure 🗂️

🗂️ **frontend** – All the code for the user interface and event handling (e.g., button clicks, login, logout).
├── 🗂️ **requests** – Handles all requests made to the backend.
├── 🗂️ **components** – Reusable React components used in this app.
└── 🗂️ **pages** – JavaScript code for rendering the main pages:
    ├── Login
    ├── Register
    └── VideoDownload

🗂️ **backend** – Implemented in Python using Flask for route creation and database management.
├── 🗂️ **routes** – Contains all Flask routes for client-server communication.
├── 🗂️ **prediction** – Responsible for:
│   ├── Detection and tracking of objects (players, keepers, ball, referees) in the video.
│   └── Estimating statistics from the uploaded video.
└── 🗂️ **models** – Class models for representing and interacting with the database.

---

