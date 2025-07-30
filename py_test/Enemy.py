class Enemy:
    def __init__(self, enemy_type, health, damage):
        self.__enemy_type = enemy_type
        self.health = health
        self.damage = damage

    def talk(self):
        print("I am an enemy")

    def attack(self):
        print(f"{self.__enemy_type} attacks with {self.damage} damage")
