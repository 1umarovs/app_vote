# 🗳️ AppVote – Developer Discussion & Voting Platform

**AppVote** is a community discussion platform tailored for developers to engage in technical conversations, share ideas, and vote on the most relevant topics. It supports real-time discussions, filtering, and voting mechanisms based on user interactions.

🔗 **Live Demo:** [appvote.up.railway.app](https://appvote.up.railway.app)

---

## 🚀 Features

- 🗨️ **Create Discussions**  
  Users can create discussions by entering a title, uploading an image, and writing content.

- 👥 **Conditional Form**  
  - **Registered users** only see inputs for `title`, `image`, and `content`.
  - **Guest users** are required to enter their `name` and `email` as well.

- 💬 **Discussion Details + Comments**  
  Each discussion has a detailed page with full content and a comment section.

- 📊 **Voting System**  
  Logged-in users can upvote discussions to support relevant ideas.

- 🔍 **Filtering Options**
  - `🕒 Recent`
  - `🔥 Most Voted`
  - `💬 Most Discussed`
  - `📁 Category-based` filtering

- 🧑‍💼 **My Posts**  
  Logged-in users can view all the discussions they have authored.

- 🗺️ **Roadmap Page**
  - Categorized display of ideas based on their status.
  - Logged-in users can view how many discussions they’ve posted in each category.

---

## 🛠 Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap
- **Hosting:** Railway.app  
  🔗 [appvote.up.railway.app](https://appvote.up.railway.app)

---

## ⚙️ Local Development Setup

```bash
git clone https://github.com/yourusername/appvote.git
cd appvote
pip install -r requirements.txt
```

Update the environment variable in `settings.py` for local development:

```python
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
```

Then run the project:

```bash
python manage.py runserver
```

---

## 🙋 Author

**Muhammadyusuf Umarov**  
🔗 GitHub: [@1umarovs](https://github.com/1umarovs)  
📬 Telegram: [@umarovs_17](https://t.me/umarovs_17)

---

## 📷 Screenshots (optional)

> You can add these later with screenshots from:
> - Homepage
> - Discussion detail page
> - Roadmap page


![home Screenshot](.appvote/staticfiles/image/home.png)

![home Screenshot](.appvote/staticfiles/image/login.png)

![home Screenshot](.appvote/staticfiles/image/roadmap.png)



---

## 📌 License

This project is open-source and free to use for educational and portfolio purposes.
