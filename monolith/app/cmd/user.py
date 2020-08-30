import click
import random
from app.auth.services import RegistrationService
from app.db.models import User
from app.db.repositories import UserRepository
from datetime import date
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


@user_cmd.cli.command('update-gender')
def update_gender():
    gender_male = 1
    gender_female = 2
    repository: UserRepository = current_app.injector.get(UserRepository)
    with click.progressbar(repository.find_all()) as bar:
        for user in bar:
            user.gender = random.randint(gender_male, gender_female)
            repository.save(user)


@user_cmd.cli.command('update-age')
def update_age():
    repository: UserRepository = current_app.injector.get(UserRepository)
    today = date.today()
    with click.progressbar(repository.find_all()) as bar:
        for user in bar:
            incomplete_year = (today.month, today.day) < (user.birth_date.month, user.birth_date.day)
            age = today.year - user.birth_date.year - incomplete_year
            user.age = age
            repository.save(user)
