# 🚀 The Absolute Beginner's Guide to Deploying Django to CloudPanel 
*(Tailored exactly for your project and your server: 159.198.77.123)*

Deploying a project for the first time can seem terrifying, but it's actually just copying files to a new computer and telling that computer how to run them. Every single command you need is listed here. Do not skip any steps!

---

## 🛠️ Phase 1: Preparing Your Local Computer (Windows)

We need to prepare your code to be sent to GitHub safely. You **never** want to send your local test database, your test images, or your personal Windows Python environment (`venv`) to your production server.

### 1. What I have already done for you:
*   **Disabled Debug Mode**: I set `DEBUG = False` in `core/settings.py` so your users don't see error code pages if something breaks.
*   **Added Allowed Hosts**: I added `aghasan.softvencealpha.com` and `159.198.77.123` to `ALLOWED_HOSTS` in `settings.py` so the server allows internet traffic.
*   **Added Static Settings**: I added `STATIC_ROOT` in `settings.py`. This is mandatory for your website's CSS and JS to load on a live server.
*   **Generated Dependencies**: I created the `requirements.txt` file which tells the server exactly what Python libraries (like Django, OpenCV) need to be downloaded.
*   **.gitignore setup**: Your project already has a `.gitignore` file that ensures `db.sqlite3` (database), `media/` (test images), and `venv/` (Python tools) are **NOT** uploaded to GitHub. This is perfect and means you won't accidentally break your server!

### 2. Push Your Code to GitHub
Open your **Local Command Prompt** (in the `C:\Users\ROY\Desktop\test\server-test` folder) and run these commands to send your code to GitHub:

```cmd
git add .
git commit -m "Ready for first deployment"
git push origin main
```
*(Note: If your branch is named `master`, use `git push origin master` instead).*

---

## 💻 Phase 2: Pulling the Code on Your Server (CloudPanel)

Now, switch to your server's SSH terminal (where you connect via `ssh root@159.198.77.123`).

### 1. Go to your Website's Folder
CloudPanel created a specific folder for your domain. Go there now:
```bash
cd /home/softvencealpha-aghasan/htdocs/aghasan.softvencealpha.com/
```

### 2. Download Your Code from GitHub
If this folder is empty, you will clone your repository. If it already has code, you will pull the latest updates. I assume it is empty for the first time:
```bash
# Don't forget the dot (.) at the end of the line! It tells git to download files into this exact folder.
git clone <YOUR_GITHUB_REPOSITORY_URL_HERE> .
```

---

## ⚙️ Phase 3: Setting up the Python Backend

Your code is on the server! But the server doesn't have Python or your database configured for this specific website yet.

### 1. Create the Server's Python Environment
Linux needs its own "virtual environment" so its Python packages don't crash other websites on the server.
```bash
python3 -m venv venv
```

### 2. Activate the Environment
You must **always** do this before running any `pip` or `python manage.py` commands on the server:
```bash
source venv/bin/activate
```
*(You will know it worked because `(venv)` will appear at the start of your terminal prompt).*

### 3. Install the Tools Using Your List
This reads the `requirements.txt` I made and downloads everything. It will also install `gunicorn`, which is the strong engine that runs Django in the real world (unlike the weak `runserver` you use on Windows).
```bash
pip install -r requirements.txt
pip install gunicorn
```

### 4. Build the Database (Crucial Step!)
Since you did not upload your local `db.sqlite3` (which is correct!), your server has NO database right now. We must instruct Django to build a brand new, empty database structure.
```bash
python manage.py migrate
```

### 5. Create Your Live Admin Account
Since the database is brand new, your old Windows admin login does not exist here. Create the first Production Admin now:
```bash
python manage.py createsuperuser
```
*(It will ask for a username, email, and password. The password will be invisible when you type it. Just type and press Enter).*

### 6. Collect Static Files (CSS/JS)
Django needs to copy all admin panel styles and your styles into one central folder so the server can serve them fast.
```bash
python manage.py collectstatic --noinput
```

---

## 🔄 Phase 4: Keeping the Server On 24/7

If you run the server now and close your terminal window, the website will shut down. We must make a background "Service" that runs automatically forever.

### 1. Open the File Editor
```bash
nano /etc/systemd/system/aghasan.service
```

### 2. Copy & Paste this Configuration:
*Don't change anything, just paste this straight in.*
```ini
[Unit]
Description=Gunicorn process for Aghasan Django
After=network.target

[Service]
User=softvencealpha-aghasan
Group=softvencealpha-aghasan
WorkingDirectory=/home/softvencealpha-aghasan/htdocs/aghasan.softvencealpha.com
Environment="PATH=/home/softvencealpha-aghasan/htdocs/aghasan.softvencealpha.com/venv/bin"
ExecStart=/home/softvencealpha-aghasan/htdocs/aghasan.softvencealpha.com/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 core.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 3. Save the File
1. Press `CTRL + O` (Letter O, not zero) to Save.
2. Press `Enter` to confirm the file name.
3. Press `CTRL + X` to Exit the editor.

### 4. Turn the Service On
Run these 3 commands to start it and ensure it auto-starts if your server restarts:
```bash
systemctl daemon-reload
systemctl start aghasan
systemctl enable aghasan
```

---

## 🌐 Phase 5: Connecting CloudPanel to Your App

Your Python app is running perfectly in the dark. Now we must tell CloudPanel's web server (Nginx) to connect internet traffic to your Python app!

1. Open your **CloudPanel Web Dashboard** via browser (`https://cp.softvencealpha.com/`).
2. Go to **Sites** -> Click on `aghasan.softvencealpha.com`.
3. Click the **Vhost** tab at the top.
4. Scroll exactly to the section that looks like `location / { ... }`.
5. **REPLACE** that entire `location /` section with this exact code:

```nginx
# This tells Cloudpanel where the CSS/JS files are
location /static/ {
    alias /home/softvencealpha-aghasan/htdocs/aghasan.softvencealpha.com/staticfiles/;
}

# This tells Cloudpanel where user-uploaded PSDs/Images are saved
location /media/ {
    alias /home/softvencealpha-aghasan/htdocs/aghasan.softvencealpha.com/media/;
}

# This sends all normal website clicks back to your Python App
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

6. Click **Save** in CloudPanel.

### 🎉 DONE!
Go to [http://aghasan.softvencealpha.com](http://aghasan.softvencealpha.com) and you will see your live Store! Upload a fake product to verify the database and media folder are working.

---

## 💡 How to Update Code in the Future
Once your site is live, pushing updates is very easy. You do not need to repeat everything!
When you make changes on Windows:
1. (Local) `git add .` -> `git commit -m "fixed bug"` -> `git push origin main`
2. (Server SSH) `cd /home/softvencealpha-aghasan/htdocs/aghasan.softvencealpha.com/`
3. (Server SSH) `git pull origin main`
4. (Server SSH) `systemctl restart aghasan` 
*(Restarting tells Gunicorn to scan for the new code!)*
