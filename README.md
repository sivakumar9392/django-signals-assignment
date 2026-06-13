# Django Signal Assignment

This project demonstrates the behavior of Django signals regarding synchronicity, threading, and database transactions.

## Answers to Questions

### Question 1: By default are Django signals executed synchronously or asynchronously?
**Answer:** Synchronously.
**Proof:** When the `sync/` endpoint is accessed, the view prints "Before Save", then calls `save()`. The signal handler is triggered immediately, prints "Signal Started", sleeps for 5 seconds, and prints "Signal Finished". Only after the signal handler completes does the control return to the view to print "After Save".

### Question 2: Do Django signals run in the same thread as the caller?
**Answer:** Yes.
**Proof:** The `thread/` endpoint prints the current thread ID in the view and another in the signal handler. Both IDs match exactly, proving they run in the same execution thread.

### Question 3: By default do Django signals run in the same database transaction as the caller?
**Answer:** Yes.
**Proof:** The `transaction/` endpoint wraps the creation of a `TestModel` in a `transaction.atomic()` block. The signal handler for `TestModel` creation then attempts to create a `SignalLog` entry. When an exception is raised in the view, both the `TestModel` record and the `SignalLog` record are rolled back, proving they share the same transaction.

## Setup Instructions

1.  **Install requirements:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3.  **Run the server:**
    ```bash
    python manage.py runserver
    ```

## Testing the Proofs

### 1. Synchronous Execution (/sync/)
- **Endpoint:** `http://127.0.0.1:8000/sync/`
- **Expected Terminal Output:**
  ```text
  Before Save
  Signal Started
  (5 second pause)
  Signal Thread ID: ...
  Signal Finished
  After Save
  ```

### 2. Same Thread (/thread/)
- **Endpoint:** `http://127.0.0.1:8000/thread/`
- **Expected Terminal Output:**
  ```text
  View Thread ID: 12345
  Signal Started
  Signal Thread ID: 12345
  Signal Finished
  ```

### 3. Same Database Transaction (/transaction/)
- **Endpoint:** `http://127.0.0.1:8000/transaction/`
- **Expected Terminal Output:**
  ```text
  Starting transaction proof...
  Creating TestModel instance...
  Signal Started
  Signal Thread ID: ...
  Signal Finished
  Raising exception to rollback...
  Caught expected exception: Forced Rollback
  ```
- **Browser Output:**
  ```text
  TestModel count: 0
  SignalLog count: 0
  ```

## Git Commands for Submission
```bash
git init
git add .
git commit -m "Complete Django Signal Assignment"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```
