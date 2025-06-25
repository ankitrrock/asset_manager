# 🛠️ Asset Management API

A Django REST API project to manage assets with service and expiration times. The system sends reminders, logs notifications, and tracks violations for expired or unserviced assets.

---

## 📌 Features

- Create, update, and delete assets.
- Set **service time** and **expiration time** for each asset.
- `/run-checks/` endpoint to:
  - Send reminders 15 minutes before service or expiration.
  - Log violations if asset is expired or not serviced.
- Swagger API documentation.
- SQLite used as the database.
- Unit test included.
- Admin panel support.
- Bonus: Custom endpoint to mark an asset as serviced.

---

## ⚙️ Tech Stack

- Django
- Django REST Framework
- SQLite
- drf-yasg (Swagger for API docs)

---

## 🚀 Getting Started

### 1. Clone the Repo

    git clone https://github.com/YOUR_USERNAME/asset-management-api.git
    cd asset-management-api


2. Create and Activate a Virtual Environment
    python -m venv env
    source env/bin/activate  # On Windows: env\\Scripts\\activate
3. Install Dependencies
    pip install -r requirements.txt
    You can create this file using:
    pip freeze > requirements.txt
4. Run Migrations
    python manage.py makemigrations
    python manage.py migrate
5. Start the Server
    python manage.py runserver


📬 API Endpoints
    Method	    Endpoint     	        Description
    GET     	/api/assets/	        List all assets
    POST	    /api/assets/	        Create an asset
    GET	        /api/assets/{id}/	    Retrieve asset by ID
    PUT	        /api/assets/{id}/	    Update asset
    DELETE	    /api/assets/{id}/	    Delete asset
    POST	    /api/assets/{id}/       mark_serviced/	Mark asset as serviced
    POST	    /api/run-checks/	    Run reminder and violation check
    GET	        /swagger/	            API documentation (Swagger)

🔐 Admin Panel
    python manage.py createsuperuser
    Then access: http://127.0.0.1:8000/admin/

✅ Run Unit Tests
    python manage.py test

📂 Folder Structure
    asset_manager/
    ├── asset_manager/        # Django project settings
    ├── assets/               # Django app with models, views, serializers
    ├── db.sqlite3            # SQLite database
    ├── manage.py
💡 Notes
    You can automate /run-checks/ using:

    A cronjob with python manage.py check_assets

    Or Celery if required in the future

📄 License
MIT - feel free to use and modify this project.

🤝 Author
    Your Name- Ankit Anand
    Email: ankitnnd@outlook.com
    GitHub: @ankitrrock


