
if __name__ == "__main__":
    print("=== Achievement Tracker System ===\n")
    
    alice = {"first_kill", "level_10", "treasure_hunter", "speed_demon"}
    bob = {"first_kill", "level_10", "boss_slayer", "collector"}
    charlie = {
    "level_10",
    "treasure_hunter",
    "boss_slayer",
    "speed_demon",
    "perfectionist"
    }

    print(f"Player Alice achievements: {alice}")
    print(f"Player Bob achievements: {bob}")
    print(f"Player Charlie achievements: {charlie}\n")
    
    print("=== Achievement Analytics ===")

    all_achievements = alice | bob | charlie
    print(f"All unique achievements: {all_achievements}")
    print(f"Total unique achievements: {len(all_achievements)}\n")

    common_achievements = alice & bob & charlie
    print(f"Common to all players: {common_achievements}")
    unique_to_all = all_achievements - (alice & bob) - (bob & charlie) - (alice & charlie)
    print(f"Rare achievements (1 player): {unique_to_all}\n")

    alice_and_bob = alice & bob
    print(f"Alice vs Bob common: {alice_and_bob}")
    bob_and_charlie = bob & charlie
    print(f"Bob vs Charlie common: {bob_and_charlie}")
    alice_and_charlie = alice & charlie
    print(f"Alice vs Charlie common: {alice_and_charlie}\n")
    alice_unique = alice - bob - charlie
    print(f"Alice unique: {alice_unique}")
    bob_unique = bob - alice - charlie
    print(f"Bob unique: {bob_unique}")
    charlie_unique = charlie - alice - bob
    print(f"Charlie unique: {charlie_unique}\n")