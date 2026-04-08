from typing import Any, Dict, Optional

from ex0.Card import Card
from ex2.Magical import Magical
from ex2.Combatable import Combatable


class EliteCard(Card, Magical, Combatable):
    def __init__(self, name: str, cost: int, rarity: str,
                 mana: int, spell_power: int,
                 attack_power: int, defense_power: int):

        super().__init__(name, cost, rarity)
        self.mana = mana
        self.spell_power = spell_power
        self.attack_power = attack_power
        self.defense_power = defense_power

        self.health = defense_power

    def play(self, game_state: Optional[Dict[str, Any]] = None) -> dict:
        return {
            "card_played": self.name,
            "cost": self.cost,
            "rarity": self.rarity,
            "status": "Elite card deployed"
        }
    # ========================
    # COMBATABLE
    # ========================

    def attack(self, target) -> dict:
        damage = self.attack_power

        return {
            "attacker": self.name,
            "target": target,
            "damage": damage,
            "combat_type": "melee"
        }

    def defend(self, incoming_damage: int) -> dict:
        damage_taken = max(0, incoming_damage - self.defense_power)
        self.health -= damage_taken

        return {
            "defender": self.name,
            "damage_taken": damage_taken,
            "damage_blocked": self.defense_power,
            "still_alive": self.health > 0
        }

    def get_combat_stats(self) -> dict:
        return {
            "attack": self.attack_power,
            "defense": self.defense_power,
            "health": self.health
        }

    # ========================
    # MAGICAL
    # ========================

    def cast_spell(self, spell_name: str, targets: list) -> dict:
        if self.mana <= 0:
            return {"error": "Not enough mana"}

        return {
            "caster": self.name,
            "spell": spell_name,
            "targets": targets,
            "mana_used": self.mana,
        }

    def channel_mana(self, amount: int) -> dict:
        self.mana += amount
        return {
            "card": self.name,
            "mana_after_channel": self.mana
        }

    def get_magic_stats(self) -> dict:
        return {
            "mana": self.mana,
            "spell_power": self.spell_power
        }
