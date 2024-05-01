# Kallos Software Design Documentation

## Table of Contents

1. Introduction
    - 1.1 Purpose
    - 1.2 Scope
    - 1.3 Target Audience

2. System Architecture
    - 2.1 Overview
    - 2.2 Components
    - 2.3 Communication Protocols

3. Database Design
    - 3.1 Database Schema
    - 3.2 Data Models

4. Security Measures
    - 4.1 Authentication
    - 4.2 Authorization
    - 4.3 Data Encryption

5. Functionality Overview
    - 5.1 Key Features
    - 5.2 Workflow

6. Deployment Architecture
    - 6.1 Deployment Environment

7. Maintenance and Support
    - 7.1 Version Control
    - 7.2 Bug Tracking


## 1. Introduction

### 1.1 Purpose
The purpose of this document is to provide an overview of the Kallos software system. It outlines the objectives, features, and functionality of Kallos, along with its intended use and benefits.

### 1.2 Scope
The scope of this document encompasses the entire Kallos software system, including its core functionalities, modules, and components. It delineates the boundaries of the system and defines what is included and excluded from its scope.

### 1.3 Target Audience
The intended audience for this document includes developers, testers, project managers, and stakeholders involved in the future development and deployment of Kallos.

## 2. System Architecture

### 2.1 Overview

The system architecture of Kallos outlines the high-level structure and organization of the application. It defines how different components interact with each other to deliver the intended functionality.

### 2.2 Components

The Kallos Flask application comprises several key components that work together to provide its features and functionalities. These components include:

- **Flask Framework:** Flask serves as the foundation of the application, providing a lightweight and flexible framework for building web applications in Python.
  
- **Application Modules:** The application is organized into modules, each responsible for specific features or functionalities. These modules help maintain a clean and modular codebase.
  
- **Database Layer:** PostgreSQL is used as the database system. The database layer manages data storage and retrieval, ensuring efficient data management within the application.
  
- **Routing and Views:** Flask utilizes routing and views to map HTTPS requests to corresponding functions, allowing for the dynamic generation of web pages and responses.
  
- **Template Engine:** Flask employs a template engine, Jinja2, to generate dynamic HTML content based on data and templates, facilitating the creation of interactive web pages.
  
### 2.3 Communication Protocols

Communication protocols define how different components of the Kallos Flask application interact with each other and with external systems. Key communication protocols include:

- **HTTPS Protocol:** Secure communication between the application and clients is ensured through HTTPS protocol, providing encryption and authentication for data transfer.
  
- **RESTful API:** RESTful APIs enable communication between the Flask application and external systems or clients, allowing for the integration of third-party services or applications.
  
- **Database Communication:** The application communicates with the PostgreSQL database using database-specific protocols, SQL o, to perform CRUD (Create, Read, Update, Delete) operations on data.


## 3. Database Design

### 3.1 Database Schema

The database schema for the Kallos Flask application defines the structure of the database, including tables, relationships, and constraints. Below is an overview of the database schema:

- **Users Table:** Stores information about users of the application, including their unique identifier, username, email, and any other relevant user details.
  
- **Answers Table:** Contains answers submitted by users, including the answer content, the associated question or quiz, and any metadata such as timestamps or user identifiers.

### 3.2 Data Models

The data models in Kallos represent the entities and relationships within the system. Each data model corresponds to a table in the database schema and defines the structure of the data stored in that table. Here are the key data models:

- **User Model:** Represents a user of the application, including attributes such as unique user ID, username, email, and any other relevant user details.

- **Answer Model:** Represents an answer submitted by a user, including attributes such as answer content, question ID or quiz ID, and any metadata such as timestamps.

These data models are implemented using SQLAlchemy, an Object-Relational Mapping (ORM) library for Python, which simplifies database interactions by allowing developers to work with database objects as Python objects.

## 4. Security Measures

### 4.1 Authentication

### 4.2 Authorization

### 4.3 Data Encryption

PyNaCl (Python bindings to the Networking and Cryptography library) is employed for encrypting sensitive data stored in the database. PyNaCl provides high-level cryptographic primitives for secure communication and data storage. Here's how PyNaCl is utilized for data encryption:

- **Key Generation:** Generate a secure cryptographic key using PyNaCl's `nacl.secret.SecretBox` class.

- **Encryption:** Before storing sensitive data such as user passwords or other confidential information in the database, encrypt it using PyNaCl's `nacl.secret.SecretBox.encrypt` method. This ensures that the data is securely encrypted before being stored.

- **Decryption:** When retrieving encrypted data from the database, decrypt it using PyNaCl's `nacl.secret.SecretBox.decrypt` method. Only authorized users with access to the encryption key can decrypt the data, ensuring confidentiality.


## 5. Functionality Overview

### 5.1 Key Features

Kallos platform offers a range of key features designed to empower HR professionals in small to medium-sized companies to enhance their employer brand efficiently. These features include:

1. **Holistic Analysis:** The platform provides a comprehensive evaluation of the employer brand, considering all aspects rather than just fragments, enabling HR professionals to gain a complete understanding of their brand's strengths and areas for improvement.

2. **Diverse Data Collection:** Data is gathered from various sources including surveys, web sources, and an internal bank of questions, ensuring a comprehensive and diverse dataset for analysis.

3. **Advanced Data Processing:** Leveraging cutting-edge techniques such as web scraping, sentiment analysis, and Natural Language Processing (NLP), the platform preprocesses and analyzes data effectively to extract meaningful insights.

4. **Innovative Technologies:** The platform utilizes the latest advancements like Large Language Models (LLMs) for NLP and AI analysis, ensuring accuracy and efficiency in the analysis process.

5. **Benchmarking Capabilities:** HR professionals can compare their employer brand performance against industry standards and competitors, gaining valuable insights into their competitive position and areas for improvement.

### 5.2 Workflow

The workflow of the Kallos platform is designed to streamline the process of conducting a comprehensive analysis of the employer brand and implementing actionable recommendations. The workflow includes the following steps:

1. **Registration:** HR professionals sign up for an account on the platform, providing necessary details such as name, email, company name, and job title.

2. **Onboarding Tutorial:** Upon logging in for the first time, users are guided through a tutorial explaining the platform's features and functionalities, ensuring a smooth onboarding experience.

3. **Data Collection:** Users upload surveys and answer questions from the platform's bank of questions, providing essential data for analysis.

4. **Main Dashboard:** Users access the main dashboard featuring interactive visualizations and charts displaying HR metrics, performance indicators, and recommendations tailored to their company's needs.

5. **Benchmarking:** Users compare their company's HR metrics with industry benchmarks and competitors, gaining insights into areas for improvement and best practices.

6. **Recommendations:** Users receive personalized recommendations based on the analysis results, organized into actionable steps to enhance the employer brand effectively.

7. **Profile Settings:** Users have control over their account settings, including personal information, notification preferences, and data management options.


## 6. Deployment Architecture

### 6.1 Deployment Environment

The deployment environment for Kallosinvolves the local system where the application will be deployed and tested. Key components of the deployment environment include:

- **Local Machine:** The application is deployed and tested on a local machine, typically a developer's workstation or a designated testing environment.

- **Development Server:** Flask's built-in development server is used to host the application locally during development and testing phases.

- **Local Database:** For local testing purposes, a PostgreSQL database instance will also be set up on the local machine to simulate the production database environment.


## 7. Maintenance and Support

### 7.1 Version Control

- **Repository Management:** Kallos  maintains a centralized GitHub repository where all source code files, configurations, and documentation are stored. This repository serves as the single source of truth for the application codebase.

- **Branching Strategy:** A branching strategy, Git Flow, is adopted to organize and manage development branches, feature branches, release branches, and hotfix branches. 

### 7.2 Bug Tracking

- **Bug Report Template:** A standardized bug report template is maintained in Excel, including fields for issue description, steps to reproduce, expected behavior, actual behavior, severity, priority, and status. This template ensures consistency and completeness in bug reports.

- **Progress Tracking:** The progress of bug fixes is tracked in Excel, updating the status of each bug report as it moves through the resolution process. This allows for monitoring the status of ongoing bug fixes, identifying bottlenecks, and ensuring timely resolution of issues.
