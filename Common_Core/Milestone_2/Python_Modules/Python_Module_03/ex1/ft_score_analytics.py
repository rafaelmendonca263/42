
import sys

if __name__ == "__main__":
    print("=== Player Score Analytics ===")

    user_args = sys.argv[1:]
    scores = []
    for arg in user_args:
        try:
            score = int(arg)
            scores.append(score)
        except ValueError:
            print(f"Warning: '{arg}' is not a valid score "
                  "and will be ignored.")
    if len(scores) == 0:
        print("No scores provided. Usage: python3 ft_score_analytics.py "
              "<score1> <score2> ...")
    else:
        print(f"Scores procced: {scores}")
        print(f"Total Players: {len(scores)}")
        print(f"Total Score: {sum(scores)}")
        print(f"High Score: {max(scores)}")
        print(f"Low Score: {min(scores)}")
        print(f"Average Score: {sum(scores) / len(scores):.2f}")
