# 📘 Physify

**Physify** is a Flask-based web app that helps learners understand physics by uploading a question — either as an image or text — and receiving community answers that can be upvoted. It supports math OCR via Pix2Text and is designed for accessible learning and contribution.

---

## 🚀 Tech Stack

- **Backend:** Flask (REST API)
- **Database:** SQLite (in-memory, can be switched to PostgreSQL/MySQL)
- **Auth:** JWT (JSON Web Token)
- **Math OCR:** [Pix2Text](https://github.com/Belval/pix2text) – open-source image-to-LaTeX converter for math equations

---

## 📦 Prerequisites

- Python 3.10+
- Pip 22+
- Relational database (SQLite used for development)

---

## ⚙️ Getting Started

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/physify.git](https://github.com/Shamimgardobuya/Pyhysify_app.git)
   cd physify
2. Install Required Packages
     pip install -r requirements.txt
3. Run Migrations
     flask db upgrade
4. Start the App
     flask --app api.py run

   
🧠 Features
Upload physics questions via image or text

OCR math recognition using Pix2Text

Community answers with upvoting

Tag-based topic organization (e.g., Kinematics, Forces)

Clean API structure with room for frontend/mobile clients

🔒 Authentication
JWT-based auth

Users can register/login and post questions or answers

Optional guest contributions (coming soon)

📚 Roadmap
 Frontend client for interacting with the API

 Admin dashboard to manage content

 OCR fallback to Tesseract for non-math images

 Study/flashcard mode for learners

🤝 Contributing
Contributions welcome! Feel free to open issues, suggest features, or submit pull requests.


License 
 MIT
