from system.celerys import app


@app.task
def celery_value(a, b):
    c = a + b

    return c