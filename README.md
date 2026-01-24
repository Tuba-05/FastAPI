# Online Examination System

A full-stack **Online Examination Platform** designed to support secure, real-time, and scalable online exams.  
The system is being developed using **FastAPI** for the backend and **React.js** for the frontend.

> **Project Status:**  
> Backend core logic is largely implemented.  
> Frontend currently supports Authentication (Login/Signup) and Student Exam Room.  
> The project is under active development.

---

## Tech Stack

### Backend
- **FastAPI** (Python 3.12)
- **Uvicorn** (ASGI Server)
- **PostgreSQL / MySQL** (via SQLAlchemy)
- **JWT Authentication**
- **WebSockets** (for real-time exam rooms)
- **Pydantic** (data validation)
- **Rate Limiting & Security Middleware**

### Frontend
- **React.js**
- **Axios** (API communication)
- **React Router**
- **Modern component-based UI**

---


The backend handles:
- Authentication
- Session management
- Exam creation and validation
- Real-time exam communication
- Security enforcement

The frontend provides:
- User login and signup
- Student exam room interface
- API-driven interaction with backend services

---

## Implemented Features

### Backend (Mostly Implemented)

#### Authentication & User Management
- User registration (Signup)
- User login
- JWT-based authentication
- Secure password handling
- Token-based session validation

#### Exam Management (Core Logic Implemented)
- Exam data models
- Question structures
- Answer validation logic
- Exam session tracking

#### Real-Time Exam Room
- WebSocket-based exam room
- Real-time student connection
- Live exam session handling
- Server-side session state management

#### Security
- Rate limiting on sensitive endpoints (OTP, login, etc.)
- Token verification for protected routes
- CORS and request validation

---

### Frontend (Partially Implemented)

#### Authentication
- Login page
- Signup page
- Token-based authentication flow
- API integration with backend

#### Student Exam Room
- Dedicated exam interface for students
- API-driven exam loading
- WebSocket connection to backend exam room
- Real-time exam environment

---

## What Is Not Completed Yet

- Teacher / Admin dashboard
- Exam creation UI
- Result analytics and reports
- Proctoring and advanced monitoring
- Full UI for exam management
- Deployment & production configuration

---

## Project Goal

The goal of this project is to build a secure, scalable, and real-time online examination system that can support:
- Multiple students
- Live exam sessions
- Secure authentication
- Exam integrity
- Real-time communication

This system is designed to be suitable for academic institutions and online testing platforms.

---

## Current Status

The foundation of the system — authentication, exam logic, and real-time communication — has been successfully implemented.
The remaining work mainly involves UI completion, admin features, and production hardening.

---

## License

This project is for academic and educational use.

---
