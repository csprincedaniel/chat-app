# Chat Application Backend

## Overview
This backend powers a **full-featured chat application**, built by **Daniel Prince** and **Jack Tsui**. It is designed to replicate the functionality of popular platforms like Discord, offering a complete messaging experience with robust backend support.

The project includes **two versions** of the backend:

- **Java Spring Boot version:** Fully functional and demo-ready, with complete PostgreSQL integration and all chat features working.  
- **Python version:** Present in the codebase but **does not currently work**.

Key features of the chat backend:

- **User Authentication:** Secure registration, login, and profile management.  
- **Real-Time Messaging:** Instant messaging across multiple channels and direct messages.  
- **Channels & Groups:** Multiple chat channels, private groups, and DMs fully supported.  
- **Roles & Permissions:** Fine-grained control for users and moderators.  
- **Media Support:** Handles attachments, images, and files in messages.  
- **Notifications:** Alerts users based on activity and messages.  
- **PostgreSQL Database:** Fully integrated to store users, messages, channels, and other data.  
- **Scalable Architecture:** Modular design for future features and easy maintenance.  
- **Clean Codebase:** Well-organized Java packages and structured components.

This backend is built as a showcase of a professional-grade chat platform, demonstrating how to implement a robust, scalable, and secure messaging system. From managing users to handling complex messaging workflows, it covers every aspect of a modern chat service.

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
- Single-click demo inside an IDE.

## About the Developers
- **Daniel Prince** – Backend architecture, database design, and API implementation.
- **Jack Tsui** – System integration, Spring Boot development, and testing.
- Built to demonstrate a fully functional, scalable, and maintainable chat backend.

## Notes
- Java packages are tied to the `backend` folder. Renaming it will break Spring Boot scanning.
- PostgreSQL configuration is ready; ensure your local database matches `application.properties`.

## Project Status
- **Java Spring Boot:** Fully working, demo-ready.
- **Python backend:** Included but **currently does not work**.
