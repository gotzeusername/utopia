import time
import random



class Character:
    def __init__(self, name, char_class, hp, strength, defense, magic, weapon=None):
        self.name = name
        self.char_class = char_class
        self.hp = hp
        self.max_hp = hp
        self.strength = strength
        self.defense = defense
        self.magic = magic
        self.weapon = weapon
        self.inventory = []
        self.score = 0
        self.xp = 0
        self.level = 1
        self.xp_to_next_level = 20

    def attack(self, target):
        if not self.is_alive():
            print(f"{self.name} can't attack because they are defeated!")
            return

        weapon_damage = self.weapon.damage() if self.weapon else 0
        base_damage = self.strength + weapon_damage
        actual_damage = max(base_damage - target.defense, 0)

        target.hp = max(target.hp - actual_damage, 0)

        weapon_name = self.weapon.name if self.weapon else "bare hands"
        print(f"{self.name} attacks {target.name} with {weapon_name} "
              f"for {actual_damage} damage! (Str {self.strength} + Weapon {weapon_damage} - Def {target.defense})")
        print(f"{target.name}'s HP is now {target.hp}/{target.max_hp}")

        if not target.is_alive():
            print(f"{target.name} has been defeated!")

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)
        print(f"{self.name} heals for {amount}. HP is now {self.hp}/{self.max_hp}")

    def is_alive(self):
        return self.hp > 0

    def add_to_inventory(self, item):
        self.inventory.append(item)
        print(f"{item} added to inventory.")

    def display_stats(self):
        print(f"Name: {self.name}")
        print(f"Class: {self.char_class}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Strength: {self.strength}")
        print(f"Defense: {self.defense}")
        print(f"Magic: {self.magic}")
        print(f"Weapon: {self.weapon if self.weapon else 'None'}")
        print(f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")
        print(f"Level: {self.level}")
        print(f"XP: {self.xp}/{self.xp_to_next_level}")

    def check_level_up(self):
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level += 10  # Optionally increase requirement for next level
            self.hp += 1
            self.max_hp += 1
            self.strength += 0
            # self.hp = self.max_hp  # Heal on level up
            print(f"\n⬆️ {self.name} leveled up to level {self.level}!")
            print(f"💪 Stats increased! HP: {self.hp}/{self.max_hp}, Strength: {self.strength}")

class Weapon:
    def __init__(self, name, min_damage, max_damage):
        self.name = name
        self.min_damage = min_damage
        self.max_damage = max_damage

    def damage(self):
        return random.randint(self.min_damage, self.max_damage)

    def __str__(self):
        return f"{self.name} ({self.min_damage}-{self.max_damage} dmg)"


def battle(character1, character2):
    print(f"\n--- Battle Start: {character1.name} vs {character2.name} ---\n")

    turn = random.choice([character1, character2])

    while character1.is_alive() and character2.is_alive():
        attacker = turn
        defender = character2 if turn == character1 else character1

        attacker.attack(defender)
        time.sleep(1)

        turn = defender

    winner = character1 if character1.is_alive() else character2

    print(f"\n🏁 {winner.name} wins the battle!")

    # Award score and XP if the hero wins
    if character1.is_alive():  # Assuming character1 is always the hero
        character1.score += 1
        character1.xp += 10
        print(f"🏆 {character1.name}'s score is now {character1.score}")
        print(f"✨ {character1.name} gained 10 XP! Total XP: {character1.xp}/{character1.xp_to_next_level}")
        character1.check_level_up()


    print("\n--- Battle Over ---\n")


    
def random_event(hero):
    event = random.choice(["travel", "enemy", "treasure"])

    if event == "travel":
        print("\nYou travel down a winding path... The scenery changes, but nothing happens.")
    
    elif event == "enemy":
        print("\nAn enemy appears!")
        enemy = Character(
            name="Goblin", 
            char_class="Monster", 
            hp=random.randint(2, 5), 
            strength=1, 
            defense=0, 
            magic=0,
            weapon=Weapon("Rusty Dagger", 1, 2)
        )
        battle(hero, enemy)

    elif event == "treasure":
        print("\nYou find a treasure chest!")
        loot = random.choice(["Gold Coin", "Health Potion", "Magic Ring", "Old Scroll"])
        hero.add_to_inventory(loot)


def the_end(hero):
    print(f"\n💀 You died. Final score: {hero.score}")


def main():
    sword = Weapon("Iron Sword", 4, 8)
    hero = Character(name="Aria", char_class="Knight", hp=9, strength=1, defense=0, magic=0, weapon=sword)

    print("🎮 Welcome to the Adventure RPG!")
    hero.display_stats()

    while hero.is_alive():
        # input("\nPress Enter to continue your journey...")
        random_event(hero)

    the_end(hero)

# Run the game
main()
