# Сервер для обробки повідомлень клієнтів

from twisted.internet import reactor
from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet.protocol import ServerFactory, connectionDone


class Client(LineOnlyReceiver):
    """Клас для обробки з'єднання з клієнтом сервера"""

    delimiter = "\r\n".encode()

    # Вказуємо фабрику для обробки повідомлень
    factory: 'Server'

    # Інформація про клієнта
    ip: str
    login: str = None

    def connectionMade(self):
        """
        Обробляємо нового клієнта:

        - записуємо IP
        - вносимо в список клієнтів
        - відправляємо повідомлення привітання
        """

        self.ip = self.transport.getPeer().host  # получаємо і записуємо адрес
        self.factory.clients.append(self)  # добавляємо в список клієнтів фабрики(сервера)

        self.sendLine("[Server] - Welcome to the chat!".encode())  # відправляємо повідомлення клієнту(encode для розуміння сервером відправленої інформації)

        print(f"[Server] - Client {self.ip} connected")  # відображаємо повідомлення в консоль сервера

    def connectionLost(self, reason=connectionDone):
        """
        обробляємо закриття з'єднання

        - видаляємо зі списку клієнта
        - виводимо повідомлення про відключення
        """

        self.factory.clients.remove(self)  # видаляємо клієна зі списку у фабриці

        print(f"[Server] - Client {self.ip} disconnected")  # відображаємо повідомлення в консоль сервера

    def lineReceived(self, line: bytes):
        """
        Обробляємо нове повідомлення від клієнта

        - зареєструвати, якщо це перший вхід, повідомити в чат
        - переслати повідомлення в чат, якщо вже зареєстрований
        """

        message = line.decode()  # декодуємо повідомлення в строку

        # якщо логін не зареєстрований
        if self.login is None:
            if message.startswith("login:"):  # перевіряємо чи в початку йде login:
                user_login = message.replace("login:", "")  # вирізаємо частин перед : і зберігаємо

                # перевіряємо на колізію
                for user in self.factory.clients:
                    if user_login == user.login:
                        error = f"[Server] - Login {user_login} already exists!"

                        self.sendLine(error.encode())
                        return

                self.login = user_login

                # відправляємо 10 попередніх повідомлень клієнту
                self.send_history()

                notification = f"[Server] - New user: {self.login}"  # формуємо повідомлення про нового клієнта
                self.factory.notify_all_users(notification)  # і відправляємо всім в чат
            else:
                self.sendLine("[Server] - Invalid login".encode())  # повідомляємо що в повідомленні клієнта помилка
        # якщо логін зареєстрований
        else:
            format_message = f"{self.login}: {message}"  # формуємо повідомлення від клієнта

            # зберігаємо повідомлення в список(історію)
            self.factory.messages.append(format_message)

            # відправляємо всім в чат і в консоль сервера
            self.factory.notify_all_users(format_message)
            print(format_message)

    def send_history(self):
        """віправляємо клієнту останні 10 повідомлень"""
        last_messages = self.factory.messages[-10:]

        for message in last_messages:
            self.sendLine(message.encode())


class Server(ServerFactory):
    """Клас для керування сервером"""

    clients: list  # список клієнтів
    messages: list
    protocol = Client  # протокол обробки клієнтів

    def __init__(self):
        """
        Старт сервера

        - ініціалізуємо список клієнтів
        - виводимо повідомлення в консоль
        """

        self.clients = []  # створюємо пустий список клієнтів
        self.messages = [] # створюємо пустий список повідомлень

        print("[Server] - Server started - OK")  # сповіщення у консоль сервера про початок роботи

    def startFactory(self):
        """запуск прослуховування клієнтів"""

        print("[Server] - Start listening ...") #консольне сповіщення

    def notify_all_users(self, message: str):
        """відправка повідомлення всім користувачам чату"""

        data = message.encode()  # кодуємо стрінгу в двійкову систему

        # відправляємо всім користувачам зі списку
        for user in self.clients:
            user.sendLine(data)


if __name__ == '__main__':
    # параметри прослуховування
    reactor.listenTCP(
        7410,
        Server()
    )

    # запускаємо реактор
    reactor.run()
