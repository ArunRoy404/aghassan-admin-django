# 🎁 Gift-khana Customization Tool Server

Welcome to the backend server for **Gift-khana**! This server manages user accounts and handles the storage and retrieval of customizable products, including their high-resolution PSD assets.

---

## 🛠️ Quick Start (For Beginners)

If you are running this for the first time or restarting:

1.  **Open Command Prompt** in this folder.
2.  **Activate Environment**:
    ```cmd
    venv\Scripts\activate
    ```
3.  **Start Server**:
    ```cmd
    python manage.py runserver
    ```
4.  **Access the Dashboard**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔐 Login Credentials (Admin)
- **Username**: `admin`
- **Password**: `adminpassword`

---

## 📦 Features & Usage

### 1. User Management
- **Dashboard Home**: View all registered users and their staff status.
- **Manage Permissions**: Admins can toggle "Staff" status or delete users.
- **Add User**: Create new team members or admins.

### 2. Product Management (Store Section)
- **Products Inventory**: View all gift items currently in the system.
- **Upload Product**: 
    - Add product name, description, and a thumbnail.
    - **PSD Support**: Specifically designed for Gift-khana, you can upload **multiple .psd files** for a single product (used for the customization tool).

---

## 🔌 API Endpoints
Integration for the Gift-khana frontend:

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/products/api/products/` | `GET` | List all products with their thumbnails and PSD info. |
| `/products/api/products/<id>/` | `GET` | Get full details for a single product. |

---

## 🚀 Deployment & Backup
- **Dependencies**: All required packages are in `requirements.txt`.
- **Git**: A `.gitignore` is included to keep the server clean and secure.
- **Database**: Uses SQLite (`db.sqlite3`) for simple, zero-config portablity.

---

*Powering the future of personalized gifting @ Gift-khana*
