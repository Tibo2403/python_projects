class FrenchSpeaker:
    def bonjour(self) -> str:
        return "Bonjour"


class EnglishSpeaker:
    def hello(self) -> str:
        return "Hello"


class FrenchToEnglishAdapter:
    def __init__(self, speaker: FrenchSpeaker):
        self.speaker = speaker

    def hello(self) -> str:
        return self.speaker.bonjour()


if __name__ == "__main__":
    french = FrenchSpeaker()
    adapter = FrenchToEnglishAdapter(french)
    english = EnglishSpeaker()

    print(english.hello())
    print(adapter.hello())
