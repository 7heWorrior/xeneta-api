# Rates API

This project is a Flask-based API for querying shipping rates between ports. It uses PostgreSQL as the database and follows best practices for performance and scalability.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Activate the Virtual Environment](#3-activate-the-virtual-environment)
  - [4. Install Dependencies](#4-install-dependencies)
  - [5. Set Up the Database](#5-set-up-the-database)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Logging](#logging)
- [Performance Optimization](#performance-optimization)
- [API Endpoints](#api-endpoints)

## Requirements

- Python 3.8+
- PostgreSQL 12+
- `pip` (Python package installer)

## Setup

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/rates-api.git
cd rates-api
```

### 2. Create a Virtual Environment

Create a virtual environment to isolate your project’s dependencies:

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment:

- On **Windows**:
  
  ```bash
  .\venv\Scripts\activate
  ```

- On **macOS/Linux**:
  
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies

With the virtual environment activated, install the required dependencies:

```bash
pip install -r requirements.txt
```
## Creating .env file 
Create .env file for your DATABASE URI 

```bash
DATABASE=postgresql://user:password@localhost/your_database
```

## Running the Application

To start the Flask application, run:

```bash
flask run
```

The API will be available at `http://127.0.0.1:5000/`.

## Running Tests

You can run the test suite using `pytest`:

```bash
pytest
```

This will run all the unit tests to ensure your application is working as expected.

