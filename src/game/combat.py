import random
from typing import List, Dict, Any

class Combatant:
    def __init__(self, name: str, health: int, attack: int, defense: int, speed: int):
        self.name = name
        self.max_health = health
        self.current_health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.status_effects: List[Dict[str, Any]] = []

    def is_alive(self) -> bool:
        return self.current_health > 0

    def take_damage(self, amount: int) -> int:
        actual_damage = max(1, amount - self.defense)
        self.current_health = max(0, self.current_health - actual_damage)
        return actual_damage

    def heal(self, amount: int) -> int:
        heal_amount = min(amount, self.max_health - self.current_health)
        self.current_health += heal_amount
        return heal_amount

    def add_status_effect(self, effect: Dict[str, Any]):
        self.status_effects.append(effect)

    def remove_status_effect(self, effect_name: str):
        self.status_effects = [effect for effect in self.status_effects if effect['name'] != effect_name]

class CombatSystem:
    def __init__(self):
        self.combatants: List[Combatant] = []
        self.turn_order: List[Combatant] = []
        self.current_turn: int = 0
        self.combat_log: List[str] = []

    def start_combat(self, players: List[Combatant], npcs: List[Combatant]):
        self.combatants = players + npcs
        self.determine_initiative()
        self.combat_log.append("Combat started!")

    def determine_initiative(self):
        self.turn_order = sorted(self.combatants, key=lambda c: c.speed + random.randint(1, 20), reverse=True)
        self.combat_log.append("Initiative order: " + ", ".join([c.name for c in self.turn_order]))

    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.turn_order)
        current_combatant = self.turn_order[self.current_turn]
        self.combat_log.append(f"{current_combatant.name}'s turn")
        return current_combatant

    def process_action(self, actor: Combatant, action: str, target: Combatant):
        if action == "attack":
            damage = max(1, actor.attack - target.defense)
            actual_damage = target.take_damage(damage)
            self.combat_log.append(f"{actor.name} attacks {target.name} for {actual_damage} damage!")
        elif action == "defend":
            actor.defense += 2  # Temporary defense boost
            self.combat_log.append(f"{actor.name} takes a defensive stance!")
        # Add more actions as needed (use item, special ability, etc.)

    def check_combat_end(self) -> bool:
        players_alive = any(c.is_alive() for c in self.combatants if isinstance(c, PlayerCombatant))
        npcs_alive = any(c.is_alive() for c in self.combatants if isinstance(c, NPCCombatant))
        return not (players_alive and npcs_alive)

    def get_combat_summary(self) -> str:
        return "\n".join(self.combat_log[-5:])  # Return the last 5 log entries

class PlayerCombatant(Combatant):
    def __init__(self, name: str, health: int, attack: int, defense: int, speed: int):
        super().__init__(name, health, attack, defense, speed)

    def get_action(self) -> Dict[str, Any]:
        # This method would be called by the game engine to get player input
        # For now, we'll return a dummy action
        return {"action": "attack", "target": None}

class NPCCombatant(Combatant):
    def __init__(self, name: str, health: int, attack: int, defense: int, speed: int):
        super().__init__(name, health, attack, defense, speed)

    def get_action(self, combat_state: Dict[str, Any]) -> Dict[str, Any]:
        # Simple AI: always attack the player with the lowest health
        players = [c for c in combat_state['combatants'] if isinstance(c, PlayerCombatant) and c.is_alive()]
        if players:
            target = min(players, key=lambda p: p.current_health)
            return {"action": "attack", "target": target}
        return {"action": "defend", "target": None}
