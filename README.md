# Favorite Books - Flask Web Application

This is a full-stack web application built with Flask that allows users to register, log in, and manage a personal collection of their favorite books. Users can add, view, edit, and delete book entries, including uploading cover images.

## Project Overview

This application serves as an end-term project demonstrating various web development concepts, including:

*   User authentication and authorization
*   CRUD (Create, Read, Update, Delete) operations
*   Database interaction with SQLite and SQLAlchemy
*   Form handling and validation with Flask-WTF
*   Session management for user login state
*   File uploads for book cover images
*   Object-Oriented Programming (OOP) principles
*   Modular design using Flask Blueprints
*   Templating with Jinja2 and UI styling with Bootstrap

## Features

*   **User Authentication:**
    *   User registration with username, email, and password.
    *   Secure password hashing.
    *   User login and logout.
    *   Session management with expiration and "Remember Me" functionality.
    *   Access control: Only logged-in users can manage their books.
*   **Book Management (CRUD):**
    *   **Create:** Add new books with details like title, author, genre, publication year, and description.
    *   **Read:** View a list of all personal books, with pagination. View detailed information for a single book.
    *   **Update:** Edit existing book details.
    *   **Delete:** Remove books from the collection.
*   **File Uploads:**
    *   Upload cover images for books (PNG, JPG, JPEG, GIF allowed).
    *   Securely store uploaded files.
    *   Display cover images on book listings and detail pages.
*   **Search Functionality:**
    *   Search personal book collection by title, author, or genre.
*   **User Interface:**
    *   Responsive design using Bootstrap.
    *   User-friendly forms and navigation.
    *   Flash messages for user feedback.
*   **Database:**
    *   SQLite database for simplicity.
    *   SQLAlchemy ORM for database interactions.
    *   Normalized tables: `User` and `Book` with a one-to-many relationship.

## Technical Stack

*   **Backend:** Python, Flask
*   **Database:** SQLite, SQLAlchemy (ORM)
*   **Forms:** Flask-WTF, WTForms
*   **Templating:** Jinja2
*   **Frontend:** HTML5, CSS3, Bootstrap 5
*   **Authentication:** Werkzeug (password hashing)
*   **File Handling:** Pillow (optional, for image processing if uncommented)

## Project Structure
```plaintext
favorite_books/
├── app/
│ ├── init.py # App factory, DB setup, Blueprints registration
│ ├── auth/ # Authentication Blueprint
│ │ ├── init.py
│ │ ├── routes.py # Auth routes (login, register, logout)
│ │ └── forms.py # Auth forms (LoginForm, RegistrationForm)
│ ├── main/ # Main application Blueprint
│ │ ├── init.py
│ │ ├── routes.py # Book CRUD routes, index, search
│ │ └── forms.py # Book forms (BookForm, SearchForm)
│ ├── models.py # SQLAlchemy models (User, Book)
│ ├── static/
│ │ ├── css/
│ │ │ └── style.css
│ │ └── uploads/ # Storage for uploaded book cover images
│ ├── templates/
│ │ ├── auth/ # Auth-related templates
│ │ ├── main/ # Main app templates (book management)
│ │ ├── base.html # Base template for site layout
│ │ ├── _form_helpers.html # Jinja macro for form rendering
│ │ ├── 404.html # Custom 404 error page
│ │ └── 500.html # Custom 500 error page
│ └── utils.py # Utility functions (e.g., save_picture)
├── instance/ # Instance-specific files (e.g., site.db)
│ └── site.db # SQLite database file
├── requirements.txt # Python dependencies
├── run.py # Script to run the Flask development server
├── config.py # Configuration settings (secret key, DB URI, etc.)
└── README.md # This file
```

## Setup and Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <your-repository-url>
    cd favorite_books
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    This will install Flask, SQLAlchemy, Flask-WTF, Werkzeug, python-dotenv, Pillow, and email-validator.

4.  **Set up Environment Variables (Optional but Recommended for SECRET_KEY):**
    Create a `.env` file in the root directory (`favorite_books/`) for sensitive configurations like `SECRET_KEY`:
    ```
    SECRET_KEY='your_very_secret_random_key_here'
    # DATABASE_URL='sqlite:///instance/site.db' # Already defaulted in config.py
    ```
    If you don't use a `.env` file, ensure the `SECRET_KEY` in `config.py` is strong and unique.

5.  **Run the application:**
    ```bash
    python run.py
    ```
    The application will start, and `run.py` will automatically:
    *   Create the `instance/` folder if it doesn't exist.
    *   Create the `app/static/uploads/` folder if it doesn't exist.
    *   Create the SQLite database and tables (`instance/site.db`) if they don't exist.

6.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

1.  **Register:** Create a new user account.
2.  **Login:** Sign in with your credentials.
3.  **Add Books:** Navigate to "Add Book", fill in the details, and optionally upload a cover image.
4.  **View Books:** Your books will be listed on the homepage. Click "View" for more details.
5.  **Search Books:** Use the search bar on the homepage to find books.
6.  **Edit Books:** From the book detail page or list, click "Edit" to modify book information.
7.  **Delete Books:** From the book detail page, click "Delete" to remove a book.
8.  **Logout:** End your session.

