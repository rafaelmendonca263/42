
import sys

if __name__ == "__main__":
    print("=== Game Data Alchemist ===\n")

    players = ['Alice', 'bob', 'Charlie', 'dylan', 'Emma',
               'Gregory', 'john', 'kevin', 'Liam']
    scores = [263, 666, 907, 170, 568, 446, 90, 527, 54]

    print(f"Initial list of players: {players}")

    all_capitalized: list[str] = [p.capitalize() for p in players]
    print(f"New list with all names capitalized: {all_capitalized}")

    only_initially_cap: list[str] = [p for p in players if p == p.capitalize()]
    print(f"New list of capitalized names only: {only_initially_cap}")

    score_dict: dict[str, int] = {name: score for name,
                                  score in zip(all_capitalized, scores)}
    print(f"Score dict: {score_dict}")

    score_average: float = round(sum(scores) / len(scores), 2)
    print(f"Score average is {score_average}")

    high_scores: dict[str, int] = {
        name: score for name, score in score_dict.items()
        if score > score_average
    }
    print(f"High scores: {high_scores}")
