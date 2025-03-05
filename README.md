# Track (Real-time)

## Overview
This project is a real-time tab tracking application built with Flask. It allows users to start and stop meetings, update tabs, and view tab data.

## Features
- Start and stop meetings
- Update tabs during a meeting
- View tab data
- Admin and user pages

## Requirements
- Python 3.x
- Flask
- CSV

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/track-real-time.git
    ```
2. Navigate to the project directory:
    ```bash
    cd track-real-time
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the Flask application:
    ```bash
    python app.py
    ```
2. Open your web browser and navigate to `http://localhost:5000` for the user page or `http://localhost:5000/admin` for the admin page.

## Endpoints
- `/start_meeting` (POST): Start a meeting and open a Google Meet link.
- `/stop_meeting` (POST): Stop the meeting.
- `/is_meeting_active` (GET): Check if a meeting is active.
- `/update_tabs` (POST): Update the tabs data.
- `/get_tabs_data` (GET): Get the tabs data.
- `/admin_tabs` (GET): Get the current tabs data.

## License
This project is licensed under the MIT License.