# Chat Application Backend

## Overview
This backend powers a **full-featured chat application**, built by **Daniel Prince** and **Jack Tsui**. It replicates the functionality of platforms like Discord, offering a complete messaging experience with robust backend support.  

The project includes **two versions**:

- **Java Spring Boot version:** Fully functional and demo-ready, with complete PostgreSQL integration and all chat features working.  
- **Python version:** Present in the codebase but **does not currently work yet**; we are actively working to make it fully operational.  

### Key Features
The backend supports **all features of a modern chat platform**, including real-time messaging, channels, roles, media support, and notifications. On top of that, it includes cutting-edge **ML-powered features**:

| **Feature**              | **ML Type**                        |
| ------------------------ | ---------------------------------- |
| Toxicity Detection       | NLP (Supervised Learning)          |
| Sentiment Analysis       | NLP (Supervised)                   |
| Summarization Bot        | LLM / NLP                          |
| AI Avatar Generation     | Diffusion models                   |
| Voice-to-Text            | ASR (Automatic Speech Recognition) |
| Speech Emotion Detection | Audio ML                            |

Other backend highlights:

- **User Authentication:** Secure registration, login, and profile management.  
- **Real-Time Messaging:** Instant messaging across channels and direct messages.  
- **Channels & Groups:** Multiple chat channels, private groups, and DMs fully supported.  
- **Roles & Permissions:** Fine-grained control for users and moderators.  
- **PostgreSQL Database:** Fully integrated for storing users, messages, channels, and app data.  
- **Scalable Architecture:** Modular design for future features and easy maintenance.  
- **Clean Codebase:** Well-organized Java packages and structured components.  

This backend demonstrates a **professional-grade, scalable, and secure chat platform**, handling complex workflows with advanced AI and ML features.

## Quick Start (Working Demo)
To see the backend in action:

1. Ensure the Spring Boot folder is named `backend`.
2. Open the project in your IDE (IntelliJ IDEA, Eclipse, or VS Code with Java support).
3. Click **Run** on the main application class. No terminal commands are needed.

> ⚠️ Renaming the folder from `backend` can break Spring Boot’s package scanning.

## Features
- REST API endpoints for authentication, messaging, and channel management.
- PostgreSQL integration with ready-to-use schemas.
- Fully functional Discord-like chat backend.
- Advanced ML-powered features (see table above).
- Single-click demo inside an IDE.

## About the Developers
- **Daniel Prince** – Backend architecture, database design, and API implementation.
- **Jack Tsui** – System integration, Spring Boot development, and testing.
- Built to demonstrate a fully functional, scalable, and maintainable chat backend.

## Notes
- Java packages are tied to the `backend` folder. Renaming it will break Spring Boot scanning.
- Python backend **does not work yet**, but we are actively working to make it fully operational.
- PostgreSQL configuration is ready; ensure your local database matches `application.properties`.

## Project Status
- **Java Spring Boot:** Fully working, demo-ready.
- **Python backend:** Present but currently non-functional; actively in development.
