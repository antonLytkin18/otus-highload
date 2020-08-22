from app import create_app
from task import celery

app = create_app()
app.app_context().push()
