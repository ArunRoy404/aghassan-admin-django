# 🚀 Django User Management Admin Panel

Welcome! This is a simple, easy-to-use Django server designed for user management. It features a custom admin dashboard where you can add, remove, and manage user permissions.

---

## 🛠️ Prerequisites
Before starting, make sure you have **Python** installed on your computer.
- You can check by opening a Command Prompt and typing: `python --version`

---

## 🏃 How to Run the Server

If you just closed everything and want to start the server again, follow these simple steps:

1.  **Open Command Prompt** in this folder.
2.  **Activate the Environment**:
    Type this and press Enter:
    ```cmd
    venv\Scripts\activate
    ```
3.  **Start the Server**:
    Type this and press Enter:
    ```cmd
    python manage.py runserver
    ```
4.  **Open your Browser**:
    Go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔐 Login Credentials
I have pre-created an admin account for you:
- **Username**: `admin`
- **Password**: `adminpassword`

---

## 📖 What can you do?

### 1. The Dashboard (Home)
Once logged in, you will see a list of all users. 
- **Staff Status**: This shows if a user has admin rights.
- **Toggle Admin**: Click this to grant or remove admin rights from a user.
- **Delete**: Remove a user from the system permanently.

### 2. Adding Users
Click the **"Add New User"** button in the sidebar or top right.
- Fill in the username, email, and password.
- Check the **"Set as Staff"** box if you want them to have access to this dashboard.

---

## 🛠️ Troubleshooting (If something goes wrong)

- **"Module not found" error?** 
  Make sure you ran the `venv\Scripts\activate` command first.
- **Server won't start?** 
  Ensure no other program is using port 8000. You can try `python manage.py runserver 8080` to run it on a different port.
- **Forgot password?** 
  You can create a new admin by typing:
  ```cmd
  python manage.py createsuperuser
  ```

---

## 🔌 API Endpoints
You can also access the data via API for use in other apps:
- **Get all products**: `GET /products/api/products/`
- **Get single product**: `GET /products/api/products/<id>/` (Replace `<id>` with the product number)

---

*Made with ❤️ for a great start in Django!*
