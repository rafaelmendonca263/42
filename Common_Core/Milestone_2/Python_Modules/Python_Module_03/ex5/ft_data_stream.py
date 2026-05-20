import random


def gen_event():
    players = ["alice", "bob", "charlie", "dylan"]
    actions = ["killed monster", "found treasure", "leveled up"]

    while True:
        player = random.choice(players)
        action = random.choice(actions)
        event = (player, action)
        yield event


def consume_event():
    for i in range(1000):
        event = next(generator)
        print(f"Event {i}: " f"Player {event[0]} " f"{event[1]}")


if __name__ == "__main__":
    try:
        print("=== Game Data Stream Processor ===")

        print("\nProcessing 1000 game events...\n")

        generator = gen_event()

        consume_event()
        a = []
        for i in range(10):
            event = next(generator)
            a.append(event)
        print(f"Built list of 10 events: {a}")

        while a:
            b = random.choice(a)
            print(f"Got event from list: {b}")

            a.remove(b)
            print(f"Remains in list: {a}")

    except Exception as e:
        print(e)
        exit(1)
