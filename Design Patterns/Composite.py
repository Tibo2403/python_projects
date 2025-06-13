class Equipment:
    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price

class Composite:
    def __init__(self, name: str):
        self.name = name
        self.item = []

    def add(self, equipment: Equipment):
        self.item.append(equipment)
        return self

    @property
    def price(self):
        return sum(x.price for x in self.item)

    @price.setter
    def price(self, value):
        self.price = value

if __name__ == '__main__':
    computer = Composite('PC')
    processor = Equipment("Processor", 1000)
    hard_drive = Equipment("Hard drive", 250)
    memory = Composite("Memory")
    rom = Equipment("ROM", 100)
    ram = Equipment("RAM", 75)

    mem = memory.add(rom).add(ram)
    pc = computer.add(processor).add(hard_drive).add(memory)

    print(pc.price)
