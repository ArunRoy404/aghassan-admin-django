# 🎁 Gift-khana Customization Tool Server

Welcome to the backend server for **Gift-khana**! This Django-based server manages user accounts and runs the core image processing engine handling high-resolution PSD assets for customizable products.

---

## 🛠️ Quick Start Guide

Follow these steps to get the server running on your local machine:

1. **Create Virtual Environment** (First time only):
   ```bash
   python -m venv venv
   ```
2. **Activate Virtual Environment**:
   ```bash
   venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply Database Migrations**:
   ```bash
   python manage.py migrate
   ```
5. **Start Developer Server**:
   ```bash
   python manage.py runserver
   ```

**Access the Admin Dashboard**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔐 Default Credentials

- **Username**: `admin`
- **Password**: `adminpassword`

---

## 🚀 Key Features

### 👥 User & Access Management
- **Role-Based Access**: Differentiate between `Superusers` and `Staff` members.
- **Member Dashboard**: View, add, or toggle staff status for system users.

### 📦 Product Inventory
- **Smart Catalog**: Manage all your customizable gift items in one place.
- **Bulk Actions**: Select multiple products to delete them simultaneously. 
- **Advanced PSD Uploader**: 
  - Upload `Preview PSDs` for general product visualization.
  - Upload named `Mockup Sections` (e.g., *front_side*, *back_side*) for mapped customization.
  - Automatically extracts and saves web-friendly thumbnails (transparent backgrounds without wrap distortions).

---

## 🔌 API Endpoints (Integration)

The backend provides a robust and structured RESTful API for the frontend portal:

### 🛍️ Products
- `GET /products/api/products/`
  - Retrieves a list of all products, including their base thumbnails and basic details.
- `GET /products/api/products/<id>/`
  - Retrieves full configuration details for a single product.
  - **Includes the `mockup` array**, returning `width`/`height` (aspect ratios calculated exactly from internal smart objects) and the clean absolute `thumbnail` URLs for each customizable section.

### 🎨 Image Generation Engine
- `POST /products/api/products/<id>/preview/`
  - Body: `image` (File)
  - Evaluates user uploaded images mathematically across **all** preview-type PSD templates.
  - Returns: An array of fully composited preview image URLs for the requested product. 

- `POST /products/api/products/<id>/mockup/`
  - Body: `image` (File), `id` (Mockup Section ID)
  - Renders a specifically selected mockup side using the precision mesh-warping engine. 
  - Perfect for updating the exact element a user is tweaking in real-time.

---

## 🖥️ Tech Stack

- **Framework**: Django & Django REST Framework
- **Image Processing**: OpenCV (cv2), numpy, Pillow (PIL), psd-tools
- **Database**: SQLite3 (Portable `db.sqlite3`)

---

*Powering the future of personalized gifting @ Gift-khana*
