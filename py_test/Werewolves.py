from Enemy import Enemy


class Werewolf(Enemy):
    def __init__(self, health, damage):
        super().__init__(enemy_type="Werewolf", health=health, damage=damage)

    def get_enemy_type(self):
        return self._Enemy__enemy_type

    def set_enemy_type(self, enemy_type):
        self._Enemy__enemy_type = enemy_type

    def talk(self):
        print("I'm a werewolf")
