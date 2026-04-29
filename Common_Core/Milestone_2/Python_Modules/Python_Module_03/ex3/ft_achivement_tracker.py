
import random


def gen_player_achivements():
    all_achievements = {'Crafting Genius',
                        'Collector Supreme',
                        'Untouchable',
                        'Speed Runner',
                        'Sharp Mind',
                        'First Steps',
                        'Treasure Hunter',
                        'Survivor',
                        'Boss Slayer',
                        'Master Explorer',
                        'Strategist',
                        'World Savior',
                        'Unstoppable'}

    quantity = random.randint(1, len(all_achievements))

    chosen_items = random.sample(list(all_achievements), quantity)

    return set(chosen_items)


if __name__ == "__main__":
    print("=== Achievement Tracker System ===\n")

    names = {'Alice': gen_player_achivements(),
             'Bob': gen_player_achivements(),
             'Charlie': gen_player_achivements(),
             'Dylan': gen_player_achivements()}

    for name in names:
        print(f"Player {name}: {names[name]}")

    all_achievements = {'Crafting Genius',
                        'Collector Supreme',
                        'Untouchable',
                        'Speed Runner',
                        'Sharp Mind',
                        'First Steps',
                        'Treasure Hunter',
                        'Survivor',
                        'Boss Slayer',
                        'Master Explorer',
                        'Strategist',
                        'World Savior',
                        'Unstoppable'}

    print(f"\nAll distinct achievements: {all_achievements}\n")

    common = names['Alice'] & names['Bob'] & names['Charlie'] & names['Dylan']

    print(f"\nCommon achievements: {common}\n")

    only_Alice = names['Alice'] - names['Bob'] & names['Charlie'] & names['Dylan']
    only_Bob = names['Bob'] - names['Alice'] & names['Charlie'] & names['Dylan']
    only_Charlie = names['Charlie'] - names['Bob'] & names['Alice'] & names['Dylan']
    only_Dylan = names['Dylan'] - names['Bob'] & names['Charlie'] & names['Alice']

    print(f"Only Alice has: {only_Alice}")
    print(f"Only Bob has: {only_Bob}")
    print(f"Only Charlie has: {only_Charlie}")
    print(f"Only Dylan has: {only_Dylan}\n")

    miss_Alice = all_achievements - names['Alice']
    miss_Bob = all_achievements - names['Bob']
    miss_Charlie = all_achievements - names['Charlie']
    miss_Dylan = all_achievements - names['Dylan']

    print(f"Alice is missing: {miss_Alice}")
    print(f"Bob is missing: {miss_Bob}")
    print(f"Charlie is missing: {miss_Charlie}")
    print(f"Dylan is missing: {miss_Dylan}")
