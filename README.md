Todo App
Overview
This project is a comprehensive Todo application developed using Flask for the backend, React for the frontend, and PostgreSQL for data storage. It allows users to create, delete, and manage their tasks efficiently while also providing reminders for upcoming tasks. The application also includes user account management features.

Features
User Authentication: Users can sign up and log in to manage their tasks.
Task Management: Users can create, delete, and view their tasks.
Reminders: The application provides reminders for tasks that are due within the next hour.
User Account Management: Users can update their account information.
Responsive UI: The frontend is built using React, ensuring a dynamic and user-friendly interface.
Secure Data Storage: All user data and tasks are stored securely in a PostgreSQL database.
Technologies Used
Backend: Flask
Frontend: React
Database: PostgreSQL
API Requests: Axios
State Management: React Hooks (useState, useEffect)
Styling: Custom CSS
Cross-Origin Resource Sharing (CORS): Enabled using Flask-CORS
Setup Instructions
Prerequisites
Python 3.8+
Node.js 14+
PostgreSQL
Backend Setup
Clone the Repository:


git clone https://github.com/Riya79hp/TODO.git
cd todo-app/backend
Install Dependencies:

pip install -r requirements.txt
Database Configuration:

Ensure PostgreSQL is installed and running.
Create a database named Todo.
Update the database connection details in app.config['SQLALCHEMY_DATABASE_URI'].
Run the Application:


flask run
Frontend Setup
Navigate to the Frontend Directory:


cd ../frontend
Install Dependencies:


npm install
Start the React Application:


npm start
Usage
Sign Up: Create a new account.
Log In: Access your account.
Create Task: Add new tasks with descriptions and times.
Delete Task: Remove tasks you no longer need.
View Reminders: Get alerted about tasks due within the next hour.
Code Overview
Backend
app.py: Main application file, defines routes and application logic.
models.py: Defines the SQLAlchemy models for users and tasks.
check_user_reminders function: Checks and returns tasks that are due within the next hour.
Frontend
SignUp.js: Component for user registration.
Login.js: Component for user login.
TodoList.js: Component to display and manage tasks.
useEffect hook: Fetches and alerts users of upcoming reminders.
Contribution
Contributions are welcome! Please fork the repository and submit a pull request with your changes.
