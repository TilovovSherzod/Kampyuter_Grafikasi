# Mukammal Python Backend Websayt (FastAPI)

Ushbu loyiha — FastAPI asosida kichik veb-sayt skeleti. Unda:

- Asosiy FastAPI server (`main.py`)
- Jinja2 shablonlari (`templates/`)
- Statik fayllar (`static/`)
- Testlar (`tests/`)


Tez boshlash (Windows PowerShell, Django):

```powershell
# 1) Virtual muhit yarating va faollashtiring
python -m venv .venv
. .venv\Scripts\Activate.ps1

# 2) Kutubxonalarni o'rnating
pip install -r requirements.txt

# 3) Lokal serverni ishga tushiring
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

# 4) Brauzerda oching: http://127.0.0.1:8000
```

Testlarni ishga tushirish (agar kerak bo'lsa):

```powershell
pip install -r requirements.txt
pytest -q
```

E'tibor: PowerShell-da skriptlarni ishga tushirishda ExecutionPolicy cheklovlari bo'lishi mumkin. Agar `Activate.ps1` ishlamasa, quyidagi buyruqni administrator huquqi bilan ishga tushiring:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Keyingi qadamlar (takliflar): autentifikatsiya, ma'lumotlar bazasi (Postgres), foydalanuvchi paneli, REST API kengaytmalari.

Muallif: Siz (loyiha boshlang'ich skeleti)
