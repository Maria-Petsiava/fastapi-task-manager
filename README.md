# FastAPI Task Manager API

Ένα ολοκληρωμένο RESTful API χτισμένο με **FastAPI**, **SQLModel** και **JWT Authentication**.

## Δυνατότητες
- Πλήρες CRUD για διαχείριση εργασιών (Tasks)
- Εγγραφή και σύνδεση χρηστών με κρυπτογράφηση κωδικών (Argon2) και JWT Tokens
- Αυτόματο Data Validation με Pydantic
- Ρυθμίσεις περιβάλλοντος μέσω `.env` και υποστήριξη CORS
- Αυτοματοποιημένα tests με `pytest`

## Εγκατάσταση & Εκτέλεση
1. Δημιουργία εικονικού περιβάλλοντος: `python -m venv venv`
2. Εγκατάσταση βιβλιοθηκών: `pip install -r requirements.txt`
3. Εκκίνηση server: `fastapi dev main.py`