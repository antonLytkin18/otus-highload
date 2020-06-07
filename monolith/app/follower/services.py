from injector import inject

from app.db.models import Follower, User
from app.db.repositories import FollowerRepository
from app.follower.exceptions import FollowerAlreadyExistsException, FollowerDoesNotExistsException


class FollowerService:

    @inject
    def __init__(self, repository: FollowerRepository):
        self.repository = repository

    def send(self, current_user: User, user: User) -> bool:
        if self.repository.find_one(follower_user_id=current_user.id, followed_user_id=user.id):
            raise FollowerAlreadyExistsException('Request already sent')

        if self.repository.find_one(follower_user_id=user.id, followed_user_id=current_user.id):
            raise FollowerAlreadyExistsException('Request already received')

        return self.repository.save(Follower(
            follower_user_id=current_user.id,
            followed_user_id=user.id,
            status=Follower.STATUS_SENT
        ))

    def accept(self, current_user: User, user: User) -> bool:
        follower = self.repository.find_one(
            follower_user_id=user.id,
            followed_user_id=current_user.id,
            status=Follower.STATUS_SENT
        )
        if not follower:
            raise FollowerDoesNotExistsException('Request does not exists')
        follower.status = Follower.STATUS_ACCEPTED
        return self.repository.save(follower)
