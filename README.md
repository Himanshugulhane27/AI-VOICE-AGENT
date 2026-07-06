# 🦷 AI Voice Receptionist for Dental Clinic

An AI-powered Voice Receptionist built using **FastAPI** and **Retell AI** for QuensultingAI Dental Clinic.

The assistant can answer patient queries, book appointments, reschedule appointments, cancel appointments, provide clinic information, and transfer urgent calls to a human receptionist.

---

# 🚀 Live Demo

### Backend API

https://ai-voice-agent-n9qs.onrender.com

### Swagger Documentation

https://ai-voice-agent-n9qs.onrender.com/docs

### GitHub Repository

https://github.com/Himanshugulhane27/AI-VOICE-AGENT

---

# ✨ Features

- AI-powered Dental Receptionist
- Appointment Booking
- Appointment Cancellation
- Appointment Rescheduling
- FAQ Handling
- Human Receptionist Transfer
- Appointment Availability Check
- Clinic Service Information
- REST API with FastAPI
- OpenAPI / Swagger Documentation
- Production Deployment on Render
- Retell AI Conversation Flow Integration

---

# 🏗️ Tech Stack

### Backend

- FastAPI
- Python
- Uvicorn
- Pydantic
- Pydantic Settings

### Voice AI

- Retell AI

### Deployment

- Render

### Integrations

- Google Sheets (Optional)
- SMTP Email Service (Optional)

---

# 📁 Project Structure

```text
AI-VOICE-AGENT/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── schemas/
│   │   ├── models/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── docs/
│   ├── requirements.txt
│   ├── README.md
│   ├── TESTING.md
│   ├── postman_collection.json
│   └── .env.example
│
└── openapi.json
```

---

# 🏛️ Architecture

```text
                     Caller
                        │
                        ▼
              Retell AI Voice Agent
                        │
                        ▼
                 Intent Detection
                        │
 ┌──────────────┬──────────────┬──────────────┬──────────────┐
 │              │              │              │              │
 ▼              ▼              ▼              ▼              ▼
Booking     Cancel      Reschedule        FAQ      Human Transfer
 │              │              │              │              │
 └──────────────┴──────────────┴──────────────┴──────────────┘
                        │
                        ▼
                 FastAPI Backend
                        │
                        ▼
             Business Logic Layer
                        │
                        ▼
 Google Sheets / Email (Optional)
```

---

# 📡 API Endpoints

## Health

| Method | Endpoint |
|---------|----------|
| GET | `/health` |

## Appointment APIs

| Method | Endpoint |
|---------|----------|
| POST | `/appointments/book` |
| POST | `/appointments/cancel` |
| POST | `/appointments/reschedule` |

## FAQ

| Method | Endpoint |
|---------|----------|
| POST | `/faq` |

## Human Transfer

| Method | Endpoint |
|---------|----------|
| POST | `/human-transfer` |

## Clinic APIs

| Method | Endpoint |
|---------|----------|
| GET | `/services` |
| GET | `/availability` |

---

# 🤖 Retell AI Integration

The backend exposes webhook endpoints that integrate with Retell AI Custom Functions.

Conversation capabilities include:

- Welcome Greeting
- Intent Detection
- Book Appointment
- Cancel Appointment
- Reschedule Appointment
- FAQ Handling
- Human Transfer

---

# 📷 Screenshots

## Swagger UI

> Add screenshot here

---

## Retell AI Flow

> Add screenshot here

---

## Render Deployment

> Add screenshot here

---

# ⚙️ Running Locally

## Clone Repository

```bash
git clone https://github.com/Himanshugulhane27/AI-VOICE-AGENT.git
```

```bash
cd AI-VOICE-AGENT/backend
```

## Create Virtual Environment

```bash
python3 -m venv .venv
```

## Activate Environment

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Server

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

# 🧪 Testing

Use Swagger:

```
/docs
```

Or import:

```
postman_collection.json
```

into Postman.

---

# 🌐 Deployment

### Backend

https://ai-voice-agent-n9qs.onrender.com

### Swagger

https://ai-voice-agent-n9qs.onrender.com/docs

### OpenAPI

https://ai-voice-agent-n9qs.onrender.com/openapi.json

---

# 📌 Future Improvements

- Google Calendar Integration
- PostgreSQL Database
- Twilio Voice Integration
- Authentication & API Keys
- Appointment Reminders
- Production-grade Monitoring
- Analytics Dashboard

---

# 👨‍💻 Author

**Himanshu Gulhane**

GitHub: https://github.com/Himanshugulhane27

Built as part of the **AI Voice Receptionist Internship Assignment**.
