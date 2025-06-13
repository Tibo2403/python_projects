class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self, message):
        for obs in self._observers:
            obs.update(message)


class Observer:
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"{self.name} received {message}")


if __name__ == "__main__":
    subject = Subject()
    observer_a = Observer("A")
    observer_b = Observer("B")
    subject.attach(observer_a)
    subject.attach(observer_b)
    subject.notify("event")
