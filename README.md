
# Collateral Management API

A REST API for managing loan collaterals built with Django REST Framework. Designed for ABD bank to track borrowers, loans, collateral assets, and LTV risk levels with automatic audit trails.
### Note: No data from any financial institution was used, the all data used the testing are fictional

**Live URL:** https://synk01.pythonanywhere.com  

---

## What It Does

- Register and login with JWT token authentication
- Manage Borrowers, Loans, and Collaterals
- Auto-calculates LTV ratio and risk level on every collateral
- Automatically logs every collateral change (audit trail)
- Filter by status, asset type, and LTV risk level
- Search borrowers and collaterals
- Sort by market value and date

---

## Tech Stack

- Python 3.10
- Django & Django REST Framework
- SimpleJWT for authentication
- django-filter for filtering
- SQLite database

---

## How to Run Locally

```bash
git clone https://github.com/Synk01/Collateral_Database.git
cd Collateral_Database
python3 -m venv venv
source venv/bin/activate
pip install django djangorestframework djangorestframework-simplejwt django-filter
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API runs at `http://127.0.0.1:8000`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login and get token |
| POST | `/api/auth/refresh/` | Refresh access token |
| GET/POST | `/api/borrowers/` | List / Create borrowers |
| GET/PUT/DELETE | `/api/borrowers/{id}/` | Get / Update / Delete borrower |
| GET/POST | `/api/loans/` | List / Create loans |
| GET/PUT/DELETE | `/api/loans/{id}/` | Get / Update / Delete loan |
| GET/POST | `/api/collaterals/` | List / Create collaterals |
| GET/PUT/DELETE | `/api/collaterals/{id}/` | Get / Update / Delete collateral |
| GET | `/api/changelogs/` | View full audit trail |

---

## Authentication

All endpoints require a JWT token in the request header:

```
Authorization: Bearer <access_token>
```

To get a token, POST to `/api/auth/login/` with your username and password.

---

## Filtering, Search & Sorting
 Sorting, filtering and search can also be performed depending on the criteria
 

---

## LTV Risk Levels

LTV (Loan-to-Value) ratio is automatically calculated:

```
LTV = (Loan Amount / Market Value) × 100
```

| LTV Ratio | Risk Level |
|-----------|------------|
| Below 60% | Low Risk |
| 60% – 80% | Medium Risk |
| Above 80% | High Risk |

---

##  Change Logging

Every time a collateral value is updated, the API save the records:
- Old and new market value
- Old and new status
- Who made the change
- When the change was made

---