from typing import NoReturn

from src.contexts.backoffice.users.application.createone.CreateUserCommand import CreatePhotoCommand
from src.contexts.backoffice.users.application.createone.UserCreator import UserCreator
from src.contexts.backoffice.users.domain.entities.UserId import UserId
from src.contexts.backoffice.users.domain.entities.UserName import UserName
from src.contexts.shared.domain.BaseObject import BaseObject
from src.contexts.shared.domain.CommandHandler import CommandHandler


class CreateUserCommandHandler(BaseObject, CommandHandler):

    __subscription: str = CreatePhotoCommand.COMMAND_TYPE

    def __init__(self, creator: UserCreator):
        self.__creator = creator

    def subscribed_to(self) -> str:
        return self.__subscription

    async def handle(self, command: CreatePhotoCommand) -> NoReturn:
        user_id: UserId = UserId(command.id)
        user_name: UserName = UserName(command.name)
        await self.__creator.run(user_id, user_name)


