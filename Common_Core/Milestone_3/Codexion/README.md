*This project has been created as part of the 42 curriculum by rmedonca.*

# Codexion - Concurrency & Resource Synchronization Challenge

![Language](https://img.shields.io/badge/Language-C-blue.svg)
![Build](https://img.shields.io/badge/Build-Makefile-orange.svg)
![Threads](https://img.shields.io/badge/Concurrency-POSIX_Threads-green.svg)
![Norminette](https://img.shields.io/badge/Norminette-OK-brightgreen.svg)
![OS](https://img.shields.io/badge/OS-Linux%20%7C%20macOS-black.svg)
![42 Project](https://img.shields.io/badge/42-Project-000000?style=flat&logo=42)

## Overview & Visual Representation

`Codexion` is a multithreaded simulation in C that models a circular co-working hub where programmers (**coders**) compete for a limited set of hardware **USB dongles** required to compile quantum code on a shared central compiler.

### Circular Hub Layout (4-Coder Example)

```text
               +---------------------------+
               |   Shared Quantum Compiler |
               +---------------------------+
                             |
                     +---------------+
                     |    Coder 1    |
                     +---------------+
                    /                 \
         (Dongle 1)                   (Dongle 2)
                  /                      \
        +---------------+              +---------------+
        |    Coder 4    |              |    Coder 2    |
        +---------------+              +---------------+
                  \                      /
         (Dongle 4)                   (Dongle 3)
                    \                 /
                     +---------------+
                     |    Coder 3    |
                     +---------------+
```

Each coder N sits between dongle N-1 and dongle N. To start compiling, a coder must simultaneously acquire both adjacent dongles (left and right).

## Description

The simulation runs concurrently with POSIX threads. Each coder operates as an independent thread executing a continuous lifecycle:

Compiling -> Debugging -> Refactoring -> Request Dongles

- **Compiling:** Requires exclusive access to both the left and right dongles for `time_to_compile` ms.
- **Debugging & Refactoring:** Non-resource-intensive tasks executed for `time_to_debug` ms and `time_to_refactor` ms respectively.
- **Burnout Condition:** If a coder does not start compiling within `time_to_burnout` ms since the start of their last compilation (or simulation start), they suffer a burnout, and the simulation halts immediately.
- **Dongle Cooldown:** Upon release, a dongle enters a mandatory cooldown period (`dongle_cooldown` ms) during which no coder can pick it up.
- **Arbitration Policy (`scheduler`):**
  - `fifo` (First-In, First-Out): Requests are granted based on arrival time.
  - `edf` (Earliest Deadline First): Grants dongles to the coder with the most urgent burnout deadline (last_compile_start + time_to_burnout).

## Instructions

### Compilation

Compile the binary using the mandatory flags (`-Wall -Wextra -Werror -pthread`):
```bash
make
```
### Execution Syntax
```bash
./codexion <number_of_coders> <time_to_burnout> <time_to_compile> <time_to_debug> <time_to_refactor> <number_of_compiles_required> <dongle_cooldown> <scheduler>
```

### Example Commands

Run simulation with FIFO scheduling:
```bash
./codexion 5 800 200 200 200 5 50 fifo
```
Run simulation with EDF scheduling:
```bash
./codexion 4 600 150 150 150 3 30 edf
```

## Resources

- **POSIX Threads & Concurrency:** IEEE Std 1003.1 documentation for `pthread_create`, `pthread_mutex_t`, `pthread_cond_t`.
- **High-Precision Timing:** POSIX `clock_gettime(CLOCK_MONOTONIC)` specifications.
- **Scheduling Algorithms:** Real-time scheduling theory (Earliest Deadline First & Min-Heap priority queues).

### AI Usage Disclosure
- **Documentation & Review:** Assisting in formatting guidelines and cross-checking requirements against 42 Norm and evaluation standards. All AI-generated logic was rigorously tested, peer-reviewed, and verified manually.

## Blocking Cases Handled

- **Deadlock Prevention (Coffman's Conditions):**
To break the Circular Wait condition, dongle acquisition always follows a strict lock-ordering strategy: a coder always attempts to lock the lowest-indexed dongle mutex first (min(left, right)) before requesting the higher-indexed one (max(left, right)).

- **Starvation Prevention:**
Under `edf` scheduling, requests are ordered in a per-dongle binary heap priority queue. In the event of identical deadlines, a deterministic tie-breaker evaluates arrival time followed by coder ID.

- **Dongle Cooldown Handling:**
Every dongle structure tracks `last_release_ts`. State checks enforce that t_now - t_release >= cooldown before granting ownership.

- **Precise Burnout Detection (<= 10ms Accuracy):**
A dedicated monitor thread polls coder timestamps at microsecond intervals (200 us). Upon detecting an overdue compilation start, it immediately flips the simulation state and prints `"burned out"` within the mandatory 10ms threshold.

- **Log Serialization:**
All terminal output is protected by a dedicated `print_mutex`, ensuring log messages from parallel threads are atomic and never interleave on the same line.

- **Single Coder Edge Case:**
Handles cases where `number_of_coders = 1` by preventing circular self-locking on the same dongle index.

## Thread Synchronization Mechanisms

- `pthread_mutex_t` (Per Dongle): Encapsulates and protects access to dongle state (`available`, `last_release_ts`) and its associated scheduling priority queue.
- `pthread_mutex_t` (`print_mutex`): Serializes output operations across all threads to prevent log corruption.
- `pthread_mutex_t` (`state_mutex`): Protects global simulation flags (`stop`, total compile count) to ensure data-race-free state reads and updates.
- Custom Min-Heap Priority Queue: Implemented natively in `src/scheduler.c` to maintain FIFO/EDF order without relying on unauthorized standard libraries.