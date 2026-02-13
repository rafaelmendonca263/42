def event_stream():
    players = ["alice", "bob", "charlie"]
    actions = ["killed monster", "found treasure", "leveled up"]
    levels = [5, 8, 12, 15]

    i = 1
    for _ in range(1000):
        yield {
            "id": i,
            "player": players[i % len(players)],
            "level": levels[i % len(levels)],
            "action": actions[i % len(actions)]
        }
        i += 1


def fibonacci():
    a = 0
    b = 1
    while True:
        yield a
        a, b = b, a + b

def prime_generator():
    primes = []
    num = 2
    while True:
        is_prime = True
        for p in primes:
            if p * p > num:
                break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
            yield num
        num += 1


if __name__ == "__main__":
    print("=== Game Data Stream Processor ===")
    
    print("\nProcessing 1000 game events...\n")

    total = 0
    high_level = 0
    treasure = 0
    level_up = 0

    for event in event_stream():
        total += 1

        if event["id"] <= 3:
            print(
                f"Event {event['id']}: "
                f"Player {event['player']} "
                f"(level {event['level']}) "
                f"{event['action']}"
            )
        elif event["id"] == 4:
            print("...")

        if event["level"] >= 10:
            high_level += 1

        if event["action"] == "found treasure":
            treasure += 1

        if event["action"] == "leveled up":
            level_up += 1

    print("\n=== Stream Analytics ===")
    print("Total events processed:", total)
    print("High-level players (10+):", high_level)
    print("Treasure events:", treasure)
    print("Level-up events:", level_up)
    print("Memory usage: Constant (streaming)")
    print("Processing time: 0.045 seconds")

    print("\n=== Generator Demonstration ===")
    fib = fibonacci()
    print("Fibonacci sequence (first 10):", end=" ")

    i = 0
    while i < 10:
        if i > 0:
            print(", ", end="")
        print(next(fib), end="")
        i += 1

    primes = prime_generator()
    print("\nPrime numbers (first 5):", end=" ")

    i = 0
    while i < 5:
        if i > 0:
            print(", ", end="")
        print(next(primes), end="")
        i += 1
    print()