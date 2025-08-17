# Chat Application - Full Stack

## Overview
This is a **full-stack chat application**, built by **Daniel Prince** and **Jack Tsui**, designed to replicate the functionality of platforms like Discord. It provides a complete messaging experience with a modern frontend and a robust backend.

- **Frontend:** React with NextJS, providing a responsive and interactive user interface.  

The project includes **two backend versions**:

- **Java Spring Boot version:** Fully functional and demo-ready, with complete PostgreSQL integration and all chat features working.  
- **Python FastAPI version:** Present in the codebase but **does not currently work yet**; we are actively working to make it fully operational.  

### Key Features
The application supports **all features of a modern chat platform**, including real-time messaging, channels, roles, media support, notifications, and advanced AI/ML functionality:

| **Feature**              | **ML Type**                        |
| ------------------------ | ---------------------------------- |
| Toxicity Detection       | NLP (Supervised Learning)          |
| Sentiment Analysis       | NLP (Supervised)                   |
| Summarization Bot        | LLM / NLP                          |
| AI Avatar Generation     | Diffusion models                   |
| Voice-to-Text            | ASR (Automatic Speech Recognition) |
| Speech Emotion Detection | Audio ML                            |

Other highlights:

- **User Authentication:** Secure registration, login, and profile management.  
- **Real-Time Messaging:** Instant messaging across channels and direct messages.  
- **Channels & Groups:** Multiple chat channels, private groups, and DMs fully supported.  
- **Roles & Permissions:** Fine-grained control for users and moderators.  
- **PostgreSQL Database:** Fully integrated for storing users, messages, channels, and app data.  
- **Scalable Architecture:** Modular design for future features and easy maintenance.  
- **Clean Codebase:** Well-organized frontend and backend packages with structured components.  

This project is a **professional-grade, scalable, and secure full-stack chat platform**, handling complex workflows with advanced AI/ML features.

## Quick Start (Working Demo)
To see the backend in action:

1. Ensure the Spring Boot folder is named `backend`.
2. Open the project in your IDE (IntelliJ IDEA, Eclipse, or VS Code with Java support for backend; VS Code or WebStorm for frontend).
3. Click **Run** on the main application class (backend) and start the frontend. No terminal commands are required.

> ⚠️ Renaming the backend folder from `backend` can break Spring Boot’s package scanning.

## Features
- Full-stack REST API endpoints for authentication, messaging, and channel management.
- PostgreSQL integration with ready-to-use schemas.
- React/NextJS frontend providing a dynamic chat interface.
- Fully functional Discord-like chat backend.
- Advanced ML-powered features (see table above).
- Single-click demo in IDEs.

## About the Developers
- **Daniel Prince** – Backend architecture, database design, API implementation, and frontend integration.  
- **Jack Tsui** – System integration, Spring Boot/FastAPI development, testing, and frontend collaboration.  
- Built to demonstrate a fully functional, scalable, and maintainable full-stack chat application.

## Notes
- Java packages are tied to the `backend` folder. Renaming it will break Spring Boot scanning.  
- Python backend **does not work yet**, but we are actively working to make it fully operational.  
- PostgreSQL configuration is ready; ensure your local database matches `application.properties`.  
- Frontend and backend are fully integrated and ready to run together in an IDE.

## Project Status
- **Java Spring Boot + React/NextJS:** Fully working, demo-ready.  
- **Python FastAPI + React/NextJS:** Present but currently non-functional; actively in development.
