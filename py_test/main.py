from Vampires import Vampire
from Werewolves import Werewolf
from Enemy import Enemy
from Battle import battle

if __name__ == '__main__':
    vampire = Vampire(100, 20)
    werewolf = Werewolf(150, 15)
    battle(vampire, werewolf)
