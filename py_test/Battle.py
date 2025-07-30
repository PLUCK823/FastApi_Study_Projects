from Enemy import Enemy


def battle(player01: Enemy, player02: Enemy):
    player01.talk()
    player02.talk()
    while player01.health > 0 and player02.health > 0:
        player01.attack()
        player02.health -= player01.damage
        # 检查player02是否还有生命值
        if player02.health <= 0:
            print(f"{player02.get_enemy_type()} 死亡")
            print(f"{player01.get_enemy_type()} 击杀了 {player02.get_enemy_type()}")
            break
        player02.attack()
        player01.health -= player02.damage
        # 检查player01是否还有生命值
        if player01.health <= 0:
            print(f"{player01.get_enemy_type()} 死亡")
            print(f"{player02.get_enemy_type()} 击杀了 {player01.get_enemy_type()}")
            break
