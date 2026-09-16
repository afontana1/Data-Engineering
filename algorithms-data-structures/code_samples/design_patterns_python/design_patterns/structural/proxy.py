from abc import ABC, abstractmethod


class Subject(ABC):
    """Abstract subject"""

    @abstractmethod
    def get_user(self, user: str) -> int:
        ...


class PaymentAPI(Subject):
    """External services like payment gateways can be good example"""

    def __init__(self, call_limit: int = 10) -> None:
        self._users: dict[str, int] = {}
        self._call_limit = call_limit

    def _user_call(self, user: str) -> int:
        if user in self._users.keys():
            self._users[user] = max(0, self._users[user] - 1)
            return self._users[user]
        else:
            self._users[user] = self._call_limit - 1
            return self._users[user]

    def get_user(self, user: str) -> int:
        calls = self._user_call(user)
        print(f'[log] User {user} has {calls} call(s) left')
        return calls


class Proxy(Subject):
    """Proxy class"""

    def __init__(self, call_limit: int = 10) -> None:
        self._subject = PaymentAPI(call_limit=call_limit)

    def get_user(self, user: str) -> int:
        """Get user info from API"""

        print(f'[log] Requesting info for {user}.')
        calls = self._subject.get_user(user)
        if not calls:
            print(f'[WARNING!] User has {calls} call(s) left!')
        else:
            print(f'[log] User has {calls} call(s) left.')
        return calls


def proxy_call(interface: PaymentAPI | Proxy, user: str) -> int:
    return interface.get_user(user)
