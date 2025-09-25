# EphemeralBin 📝

EphemeralBin is a simple, secure web application for creating self-destructing notes. Share temporary secrets, links, or messages that are automatically deleted after being viewed or after a set time limit.

!

***

## ✨ Features

* **Create Secret Notes:** Write and submit any text-based content.
* **Set Expiration:** Choose when the note should expire:
    * After the first view.
    * After 10 minutes.
    * After 1 hour.
* **Unique, Shareable Links:** A random, unguessable URL is generated for every note.
* **Automatic Deletion:** Once an expiration condition is met, the note is permanently deleted from the database.

***

## 🛠️ Tech Stack

* **Backend:** Python, Flask, Flask-SQLAlchemy
* **Database:** SQLite
* **Frontend:** HTML, Bootstrap 5
* **JavaScript:** jQuery for simple DOM manipulation (e.g., "Copy to Clipboard").

***

## 🚀 Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/kpt10x/ephemeral-bin.git](https://github.com/kpt10x/ephemeral-bin.git)
    cd ephemeral-bin
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Initialize the database:**
    *The database will be created automatically when you first run the app.*

5.  **Run the Flask application:**
    ```sh
    flask run
    ```

    The application will be available at `http://127.0.0.1:5000`.

***

## Usage

1.  Navigate to the home page.
2.  Type or paste your text into the text area.
3.  Select an expiration option from the dropdown menu.
4.  Click "Create Note".
5.  You will be redirected to a success page containing the unique link to your note. Copy and share it!