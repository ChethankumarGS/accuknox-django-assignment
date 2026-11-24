# Django assignment: signals and a custom Rectangle class

A Django project (`config`) with two apps:

- `signals_demo`: answers the three Django Signals questions with runnable code.
- `shapes`: the `Rectangle` class.

## Run

```bash
pip install -r requirements.txt
python manage.py test -v 2      # each test proves one answer
python manage.py migrate --run-syncdb
python manage.py demo           # prints the evidence in plain text
```

## Topic: Django Signals

The receivers are in `signals_demo/signals.py`. A `post_save` handler sleeps for 2 seconds, records its thread id and whether a transaction is open, and a second handler writes an `AuditLog` row.

**Q1. Synchronous or asynchronous?** Synchronous. `Item.objects.create()` takes 2 seconds, because it blocks until the handler's `time.sleep(2)` finishes. The handler's finish time is earlier than the time `save()` returned.
Proof: `Q1SynchronousTest`.

**Q2. Same thread as the caller?** Yes. The thread id recorded inside the handler equals the caller's `threading.get_ident()`.
Proof: `Q2SameThreadTest`.

**Q3. Same database transaction as the caller?** Yes, by default. Inside `transaction.atomic()` the handler sees `connection.in_atomic_block == True`, and when the caller's transaction is rolled back, the `AuditLog` row written by the handler is rolled back too.
Proof: `Q3SameTransactionTest`.

## Topic: Custom classes in Python

`shapes/rectangle.py`: `Rectangle(length: int, width: int)` is iterable. Iterating yields `{'length': <length>}` first, then `{'width': <width>}`.

```python
>>> list(Rectangle(5, 3))
[{'length': 5}, {'width': 3}]
```

Tests: `shapes/tests.py`.
