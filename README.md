# Library Management System API

A FastAPI + Pydantic library management system built with OOP and a layered architecture.
Data is stored **in memory** for now (it resets on restart). The storage layer is isolated so a real database can be plugged in later.

## Quick start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

The app starts with 5 sample books and 2 sample members (ids 1 and 2), so you can borrow right away from Swagger.

Run the tests:

```bash
pytest
```

## Project structure

```
app/
├── main.py                  # App factory, lifespan (seeding), router registration
├── core/
│   ├── config.py            # Settings (env vars prefixed LIB_, or a .env file)
│   └── exceptions.py        # Domain errors: NotFound / Conflict / BusinessRule
├── models/                  # OOP domain classes with behaviour (no HTTP, no storage)
│   ├── base.py              # BaseEntity: id, created_at, updated_at
│   ├── book.py              # Book.check_out(), check_in(), set_total_copies()
│   ├── member.py            # Member.activate(), deactivate()
│   └── loan.py              # Loan.mark_returned(), renew(), fines, status
├── schemas/                 # Pydantic request/response models (API contracts)
├── database/
│   ├── in_memory.py         # InMemoryDatabase: tables, auto-increment ids, lock
│   ├── connection.py        # get_db(): the one place that hands out the store
│   └── seed.py              # Sample data
├── repositories/            # Data access only (CRUD + queries)
│   ├── base.py              # AbstractRepository interface + InMemoryRepository
│   └── book_ / member_ / loan_repository.py
├── services/                # Business logic (lending rules, validations)
│   └── book_ / member_ / loan_service.py
└── api/
    ├── dependencies.py      # Dependency injection: db -> repositories -> services
    ├── error_handlers.py    # Maps domain errors to HTTP status codes
    ├── router.py            # Combines all routers under /api/v1
    └── endpoints/           # Thin route handlers, one module per resource
        └── health.py, books.py, members.py, loans.py
tests/                       # pytest suite using TestClient and a fresh DB per test
```

Request flow: **endpoint → service → repository → database**. Each layer only talks to the one below it.

## Endpoints (`/api/v1`)

| Resource | Method & path | Description |
|---|---|---|
| Health | `GET /health` | Service status |
| Books | `POST /books` | Add a book |
| | `GET /books` | List/search (`search`, `author`, `genre`, `available_only`, `skip`, `limit`) |
| | `GET /books/{id}` | Get a book |
| | `PATCH /books/{id}` | Partial update |
| | `DELETE /books/{id}` | Delete (blocked while copies are on loan) |
| Members | `POST /members` | Register a member |
| | `GET /members` | List/search (`name`, `is_active`) |
| | `GET /members/{id}` | Get a member |
| | `PATCH /members/{id}` | Partial update, including `is_active` |
| | `DELETE /members/{id}` | Delete (blocked while they have books out) |
| | `GET /members/{id}/loans` | A member's loans (`status` filter) |
| Loans | `POST /loans` | Borrow a book |
| | `GET /loans` | List (`member_id`, `book_id`, `status`) |
| | `GET /loans/overdue` | Overdue loans |
| | `GET /loans/{id}` | Get a loan |
| | `POST /loans/{id}/return` | Return a book; a fine is calculated if late |
| | `POST /loans/{id}/renew` | Extend the due date |

## Lending rules

These are configurable in `app/core/config.py` or via env vars, e.g. `LIB_FINE_PER_DAY=2.5`:

- Standard members: up to 3 active loans. Premium members: up to 10.
- Default loan period: 14 days (maximum 60).
- A member can't borrow if they're inactive, have an overdue book, or already have the same title.
- Loans can be renewed up to 2 times, and not once they're overdue.
- Late fine: 1.0 per full day overdue, calculated on return.

Errors return `{"detail": "..."}` with **404** (not found), **409** (conflict, e.g. duplicate ISBN or no copies left), **400** (lending rule broken) or **422** (invalid input).

## Adding a real database later

1. Replace `app/database/connection.py` with a session factory, e.g. SQLAlchemy `SessionLocal`, and have `get_db()` yield a session.
2. Add ORM table models, or map the existing domain classes.
3. Write SQL versions of the repositories that implement the same methods as the in-memory ones (`AbstractRepository` + the query methods in each repository).
4. Update `app/api/dependencies.py` to build the new repositories.
5. Replace `InMemoryDatabase.transaction()` usage in `LoanService` with the session's transaction.

Services, schemas, models and endpoints stay unchanged.
