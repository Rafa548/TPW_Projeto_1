# Functionalities Implemented

## API
- Receives all news data
- Utilizes functions to change the API key upon reaching request limits

## Login
- Blocks multiple incorrect login attempts (3 attempts lead to a 10-minute timeout)

## Register
- Requires a strong password with alerts for password strength

## Profile
- Edit profile with security verifications (unique email, confirmation of the current password)

## Custom Search/Categories
- Custom search/categories with save/remove functionalities for articles
- Searches based on news titles (no cache used due to specificity)
- Categories include latest and popular general news

## Interests Modal
- Displays only if the user hasn't selected any interests yet

## Django Cache
- Reduces API usage through caching
- Each user has their own cache/pages

## Home Page
- Changes with/without login (updated every 30 seconds based on cache)

## Notifications
- Updated every 30 seconds based on cache and user interests

## Commands
- Adding interests, adding admin, clearing database data, adding users (with/without interests)

## Websockets for Chat
- Allows message exchange between users (not functional on PythonAnywhere)

## Viewing News
- Clicking on any news item adds it to the user's history and redirects to the original site

## Usage of Endpoints
- Calls views without page reloads using POST's AJAX in HTML files

## Data Integrity Verification
- Possible through the /admin page provided by Django by default

## How to Use:

### General Usage:
- Results and notifications are updated every 30 seconds

### Local Setup:
1. Install necessary dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate (Ubuntu)
    pip install -r requirements.txt
    python3 manage.py createcachetable
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py add_interests
    python3 manage.py runserver
    ```

2. Optional Commands:
    - `python3 manage.py create_admin` (creates admin credentials)
    - `python3 manage.py clean_db` (cleans the database)
    - `python3 manage.py add_users_with_interests` (adds users with interests)
    - `python3 manage.py add_users` (adds users)

### Usage:
- Register, login, choose interests, and use the site normally
- For testing chat between users, open a new incognito window with a different user

### PythonAnywhere:
- Configured but doesn't support user chat functionality
- Use register/login/choose interests to use the site

# Project Links

- [GitHub Repository](https://github.com/Rafa548/TPW_Projeto): Link to the project's GitHub page.
- [PythonAnywhere Deployment](http://rafa548.pythonanywhere.com/): Link to the deployed application on PythonAnywhere.

