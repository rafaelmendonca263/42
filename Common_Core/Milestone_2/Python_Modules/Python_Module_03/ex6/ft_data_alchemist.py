
if __name__ == "__main__":
    print("=== Game Data Alchemist ===")

    players = ['Alice',
               'bob',
               'Charlie',
               'dylan',
               'Emma',
               'Gregory',
               'john',
               'kevin',
               'Liam']

    scores = [263, 666, 907, 170, 568, 446, 90, 527, 54]

    print(f"Initial list of players: {players}")

    new_list = []
    for player in players:
        new_list.append(player.capitalize())

    print(f"New list with all names capitalized: {new_list}")

    new_list = []
    for player in players:
        if player == player.capitalize():
            new_list.append(player)

    print(f"New list of capitalized names only: {new_list}")

    score_dict = []
    for player in players:
        score_dict.append({player for scores in zip(players, scores)})
    print(f"Score dict: {score_dict}")
