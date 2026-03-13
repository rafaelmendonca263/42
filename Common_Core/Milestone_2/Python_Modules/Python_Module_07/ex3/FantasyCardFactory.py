
import random
from ex0.Card import Card
from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard
from ex3.CardFactory import CardFactory


class FantasyCardFactory(CardFactory):
    def __init__(self):
        self._creature_templates = {
            "dragon": {"name": "Fire Dragon", "power": 5, "cost": 5},
            "goblin": {"name": "Goblin Warrior", "power": 2, "cost": 2}
        }

        self._spell_templates = {
            "fireball": {"name": "Fireball", "power": 3, "cost": 3},
            "lightning": {"name": "Lightning Bolt", "power": 4, "cost": 3}
        }

        self._artifact_templates = {
            "mana_ring": {"name": "Mana Ring", "power": 1, "cost": 1},
            "crystal": {"name": "Magic Crystal", "power": 2, "cost": 2}
        }

    def create_creature(self, name_or_power=None):
        if name_or_power == "dragon":
            return CreatureCard(
                "Fire Dragon",
                5,
                "Legendary",
                7,
                5
            )

        if name_or_power == "goblin":
            return CreatureCard(
                "Goblin Warrior",
                2,
                "Common",
                2,
                2
            )

        return CreatureCard(
            "Goblin Warrior",
            2,
            "Common",
            2,
            2
        )

    def create_spell(self, name_or_power: str | int | None = None) -> Card:
        if name_or_power == "lightning":
            return SpellCard(
                "Lightning Bolt",
                3,
                "Rare",
                "damage"
            )

        return SpellCard(
            "Fireball",
            3,
            "Common",
            "damage"
        )

    def create_artifact(self, name_or_power: str | int | None = None) -> Card:
        if name_or_power == "crystal":
            return ArtifactCard(
                "Crystal",
                2,
                "Rare",
                5,
                "Permanent: +1 mana per turn"
            )

        return ArtifactCard(
            "Mana Ring",
            2,
            "Common",
            3,
            "Permanent: +1 mana per turn"
        )

    def create_themed_deck(self, size: int) -> dict:
        deck = {
            "creatures": [],
            "spells": [],
            "artifacts": []
        }

        for _ in range(size):
            card_type = random.choice(["creature", "spell", "artifact"])

            if card_type == "creature":
                deck["creatures"].append(self.create_creature())

            elif card_type == "spell":
                deck["spells"].append(self.create_spell())

            else:
                deck["artifacts"].append(self.create_artifact())

        return deck

    def get_supported_types(self) -> dict:
        return {
            "creatures": list(self._creature_templates.keys()),
            "spells": list(self._spell_templates.keys()),
            "artifacts": list(self._artifact_templates.keys())
        }
