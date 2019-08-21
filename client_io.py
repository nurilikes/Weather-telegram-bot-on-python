#  Консольный клиент для подключения к серверу

from twisted.internet import reactor, stdio
from twisted.internet.protocol import Protocol, ClientFactory

class MessageHandler(Protocol):
    """Клас для роботи паралельного вводу/виводу"""

    output = None  # шлях для виводу повідомлень з консолі

    def dataReceived(self, data: bytes):
        """обробляє нове повідомлення від серверу/вводу користувача"""

        if self.output:
            self.output.write(data)  # перенаправяємо повідомлення на сервер


class User(MessageHandler):
    """Клас для відправки/обробки повідомлень сервера"""

    factory: 'Connector'

    def wrap(self):
        """обробка вводу/виводу в терміналі"""

        handler = MessageHandler()  # створюємо проміжний об'єкт для роботи з введенням / виведенням в консолі
        handler.output = self.transport  # призначаємо шлях для виведення повідомлень (на сервер)

        wrapper = stdio.StandardIO(handler)  # запускаємо модуль Twisted для паралельного введення і отримання даних

        self.output = wrapper  # підставляємо в поточний протокол (буде перехоплювати після натискання на Enter)

    def connectionMade(self):
        """
        Обробляємо вдале підкулючення

        - поилаємо логін на сервер
        - запускаємо ввід/вивід
        """

        login_message = f"login:{self.factory.login}"  # формуємо строку реєстрації логіну
        self.send_message(login_message)  # відправляємо на сервер

        self.wrap()  # включаємо режим введення / виводу в консолі (щоб відправляти повідомлення натисканням Enter)

    def send_message(self, content: str):
        """обробляємо відправку повідомлення на сервер"""

        data = f"{content}\n".encode()  # кодуємо текст в двійкове подання
        self.transport.write(data)  # відправляємо на сервер


class Connector(ClientFactory):
    """клас для створення підключення до сервера"""

    protocol = User
    login: str

    def __init__(self, login: str):
        """створення менеджера підключення(зберігаємо логін)"""

        self.login = login  # записуємо логін для реєстрації

    def startedConnecting(self, connector):
        """обробляємо встановлення з'єднання"""

        print("Connecting to the server...")  # сповіщення в консолі клієнта

    def clientConnectionFailed(self, connector, reason):
        """Обработчик неудачного соединения (отключаем reactor)"""

        print("Connection failed")  # уведомление в консоли клиента
        reactor.callFromThread(reactor.stop)  # остановка реактора

    def clientConnectionLost(self, connector, reason):
        """Обработчик отключения соединения (отключаем reactor)"""

        print("Disconnected from the server")  # уведомление в консоли клиента
        reactor.callFromThread(reactor.stop)  # остановка реактора


if __name__ == '__main__':
    # запрашиваем имя пользователя для подключения
    user_login = input("Your login: ")

    # параметры соединения
    reactor.connectTCP(
        "localhost",
        7410,
        Connector(user_login)
    )

    # запускаем реактор
    reactor.run()
