
import random
from typing import List
from ex0.Card import Card
from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard

class Deck():
    def __init__(self):
        self.cards: List[Card] = []
    
    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def remove_card(self, card_name: str) -> bool:
        for card in self.cards:
            if card.name == card_name:
                self.cards.remove(card)
                return True
        return False        

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw_card(self) -> Card:
        if not self.cards:
            return None
        return self.cards.pop(0)

    def get_deck_stats(self) -> dict:
        spells = 0
        artifacts = 0
        creatures = 0
        total_cost = 0

        for card in self.cards:
            total_cost += card.cost
            if isinstance(card, SpellCard):
                spells += 1
            elif isinstance(card, ArtifactCard):
                artifacts += 1
            elif isinstance(card, CreatureCard):
                creatures += 1
        
        avg_cost = total_cost / len(self.cards) if self.cards else 0

        return {
                "total_cards": len(self.cards),
                "creatures": creatures,
                "spells": spells,
                "artifacts": artifacts,
                "avg_cost": avg_cost
                }