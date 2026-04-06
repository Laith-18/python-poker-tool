from dataclasses import dataclass, field
from typing import List

@dataclass
class GameState:
    username: str
    user_bank: int
    pot: int = 0
    recent_bet: int = 0
    ai_bet: int = 0
    small_blind: bool = False
    user_deck: List = field(default_factory=list)
    ai_deck: List = field(default_factory=list)
    community_deck: List = field(default_factory=list)
    ai_strength: int = 0
    user_strength: int = 0
    tutorial_mode: bool = False
    user_hand_strength: int = 0
