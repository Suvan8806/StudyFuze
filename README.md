# StudyFuze

StudyFuze is a web application designed to help students connect with each other based on their interests, classes, majors, and hobbies. Built with **Flask**, **SQLite**, and several essential libraries, this platform allows students to sign up, log in, update their profiles, and search for other users based on specific filters. Additionally, it uses **Werkzeug** for secure password hashing, ensuring that user credentials are kept safe.

## Table of Contents
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [How to Use](#how-to-use)
- [License](#license)

## Technologies Used

- **Flask**: A micro web framework for Python, used to build the server-side logic and render templates.
- **SQLite**: A lightweight database engine used to store user data.
- **Werkzeug**: A library that provides utilities for secure password hashing.
- **HTML/CSS**: Frontend technologies used to create the user interface.
- **JavaScript (AJAX)**: For asynchronous requests to fetch data from the server.
- **SMTP**: For sending emails from the contact form.

## Features

- **User Signup & Login**: Users can create accounts, securely log in, and manage their profile information.
- **Profile Management**: Users can update their personal information, including age, college, major, classes, and hobbies.
- **Search Functionality**: Users can search for others based on their college, classes, or major.
- **Email Contact Form**: Users can contact the admin via an integrated email form.
- **Session Tracking**: User sessions are stored and managed to maintain logged-in status.
- **Password Hashing**: Passwords are hashed using **Werkzeug**'s security features to ensure data protection.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Suvan8806/StudyFuze.git
   cd StudyFuze
