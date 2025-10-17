# 🎮 Game Reviews API

Django REST Framework project for reviewing and rating games.  
Users can register, add games, write reviews, and view average ratings.

---

## 🚀 Run Locally
```bash
python manage.py runserver
```
**With Docker:**
```bash
docker-compose build
docker-compose up
```

---

## 🌐 Endpoints

### 🎮 Games
- `GET /api/games/` — List all games
- `POST /api/games/` — Create game *(admin)*
- `GET /api/games/<id>/` — Game details
- `PUT/PATCH/DELETE /api/games/<id>/` — Update/Delete *(admin)*

### 💬 Reviews
- `GET /api/reviews/` — List reviews
- `POST /api/reviews/` — Create *(auth)*
- `GET /api/reviews/<id>/` — Review details
- `PUT/PATCH/DELETE /api/reviews/<id>/` — Edit/Delete own review

### 👤 Users
- `POST /api/accounts/register/` — Register
- `POST /api/accounts/login/` — JWT token
- `GET/PUT /api/accounts/profile/` — View/Update profile

---

## 🔑 Permissions
- **Public:** view games/reviews, register
- **Authenticated:** manage own reviews/profile
- **Admin:** manage games, all reviews

---

## ⚙️ .env Example
```ini
DB_NAME=gamereviews
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your_secret_key_here
DEBUG=1
```

---

## 🐳 Docker Commands
```bash
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
```
🧑‍💻 Author

Created by: Pasha Ismailovi
Built with ❤️ using Django REST