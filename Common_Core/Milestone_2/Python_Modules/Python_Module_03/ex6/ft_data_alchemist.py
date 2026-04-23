
if __name__ == "__main__":
    print("=== Game Analytics Dashboard ===")

    players = [
        {
            "name": "alice",
            "score": 2300,
            "achievements": ["first_kill", "level_10"],
        },
        {
            "name": "bob",
            "score": 1800,
            "achievements": ["first_kill", "level_5"],
        },
        {
            "name": "charlie",
            "score": 2150,
            "achievements": ["first_kill", "level_10", "boss_slayer"],
        }
    ]

    print("\n=== List Comprehension Examples ===")
    high_scorers = [p["name"] for p in players if p["score"] > 2000]
    print(f"High scorers (>2000): {high_scorers}")

    doubled_scores = [p["score"] * 2 for p in players]
    print(f"Scores doubled: {doubled_scores}")

    active_players = [p["name"] for p in players]
    print(f"Active players: {active_players}")

    print("\n=== Dict Comprehension Examples ===")
    player_scores = {p["name"]: p["score"] for p in players}
    print(f"Player scores: {player_scores}")

    score_categories = {
        "high": sum(1 for p in players if p["score"] > 2000),
        "medium": sum(1 for p in players if 1800 <= p["score"] <= 2000),
        "low": sum(1 for p in players if p["score"] < 1800),
    }
    print(f"Score categories: {score_categories}")

    achievement_counts = {p["name"]: len(p["achievements"]) for p in players}
    print(f"Achievement counts: {achievement_counts}")

    print("\n=== Set Comprehension Examples ===")
    unique_players = {p["name"] for p in players}
    print(f"Unique players: {unique_players}")

    unique_achievements = {ach for p in players for ach in p["achievements"]}
    print(f"Unique achievements: {unique_achievements}")

    print("\n=== Combined Analysis ===")
    total_players = len(unique_players)
    print(f"Total players: {total_players}")

    total_unique_achievements = len(unique_achievements)
    print(f"Total unique achievements: {total_unique_achievements}")

    average_score = sum(p["score"] for p in players) / len(players)
    print(f"Average score: {average_score}")

    top_performer = max(players, key=lambda p: p["score"])
    print(
        f"Top performer: {top_performer['name']} "
        f"({top_performer['score']} points, "
        f"{len(top_performer['achievements'])} achievements)"
    )
