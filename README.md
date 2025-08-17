# Chat Application Backend

## Overview
This backend powers a **full-featured chat application**, created by **Daniel Prince** and **Jack Tsui**. It is designed to replicate the functionality of popular platforms like Discord, offering a complete messaging experience with robust backend support.

Key features include:

- **User Authentication:** Register, log in, manage profiles, and handle permissions securely.
- **Real-Time Messaging:** Send and receive messages instantly across multiple channels.
- **Channels & Groups:** Support for multiple chat channels, private groups, and direct messages.
- **Roles & Permissions:** Fine-grained control over user roles, channel access, and moderation.
- **PostgreSQL Database:** Fully integrated for storing users, messages, channels, and other app data.
- **Media Support:** Handle attachments, images, and other file types in messages.
- **Notifications:** Manage alerts and notifications for users based on activity.
- **Scalable Architecture:** Structured for easy expansion and additional features.
- **Clean Codebase:** Organized Java packages, modular components, and maintainable design.

This project also includes a Python version, but it is **not currently functional**. The working demo is the **Java Spring Boot version**, which integrates all features above, including a fully operational PostgreSQL database.

This backend is built as a showcase of a professional-grade chat platform, demonstrating how a robust, scalable, and secure messaging system can be implemented. From managing users to handling complex messaging workflows, it’s designed to cover every aspect of a modern chat service.

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
- Python backend included for reference or future development.
- PostgreSQL configuration is ready; ensure your local database matches `application.properties`.

## Project Status
- **Java Spring Boot:** Fully working, demo-ready.
- **Python backend:** Experimental, not operational yet.
