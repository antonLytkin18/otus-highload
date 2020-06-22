import click
from app.auth.services import RegistrationService
from app.db.models import User
from faker import Faker
from flask import Blueprint, current_app

user_cmd = Blueprint('user', __name__)


@user_cmd.cli.command('generate')
@click.argument('count')
def generate(count: int):
    service = current_app.injector.get(RegistrationService)
    with click.progressbar(range(int(count))) as bar:
        for _ in bar:
            fake = Faker()
            user = User()
            user.name = fake.first_name()
            user.last_name = fake.last_name()
            user.email = fake.email()
            user.birth_date = fake.date_time().date().__str__()
            user.password = fake.password()
            user.city = fake.city()
            service.register(user)
