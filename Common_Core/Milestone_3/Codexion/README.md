# Codexion

_This project has been created as part of the 42 curriculum by <login1>[_ , <login2>][_]._

## Description

Codexion simulates coders competing for limited USB dongles required to compile.
Each coder is represented by a thread that must acquire two adjacent dongles to
compile. The program implements FIFO and EDF scheduling policies, enforces
dongle cooldowns, and stops when a coder burns out or when all coders have
completed the required number of compiles.

## Instructions

Build:

```sh
make
```

Run example:

```sh
./codexion 5 800 200 200 200 3 50 fifo
```

Arguments (all mandatory):
- `number_of_coders` `time_to_burnout` `time_to_compile` `time_to_debug` `time_to_refactor` `number_of_compiles_required` `dongle_cooldown` `scheduler`

The `scheduler` must be either `fifo` or `edf`.

## Resources

- Project subject and requirements (provided by 42 curriculum).
- POSIX threads documentation: pthreads (`pthread_create`, `pthread_mutex_t`, `pthread_cond_t`).
- `gettimeofday` / `clock_gettime` documentation for timing.

AI usage: I used AI assistance to scaffold the project, design data structures, and generate initial code templates. All code produced by AI was reviewed and adapted to meet the project constraints.

## Blocking cases handled

- Deadlock prevention: coders push requests into per-dongle queues and only acquire both dongles when they are at the head of both queues. This avoids circular wait.
- Starvation prevention: EDF policy is implemented with a deterministic tie-breaker (arrival time then coder id) to ensure liveness when parameters are feasible.
- Dongle cooldown: after release, a dongle remains unavailable until `dongle_cooldown` ms have elapsed; this is tracked per-dongle and enforced before granting access.
- Single-coder edge-case: when `number_of_coders` is 1, the program handles the single-dongle situation and allows the monitor to detect burnout appropriately.
- Log serialization: printing is serialized with a mutex and uses atomic writes to prevent interleaving.

## Thread synchronization mechanisms

- `pthread_mutex_t` per-dongle: protects dongle state (`available`, `last_release_ts`) and the per-dongle priority queue.
- `pthread_cond_t` per-dongle: signalled when a dongle becomes available (used to wake waiters).
- Global `print_mutex`: ensures log lines do not interleave.
- Global `state_mutex`: protects shared simulation state (`finished_count`, `stop`) to coordinate termination.
- Priority queue (binary heap): implemented in `src/scheduler.c`, supports FIFO and EDF ordering. Queues are allocated per-dongle and accessed under the dongle mutex.

## Tests

Run basic test scenarios:

```sh
make test
make test-pq
```

`test` runs simple functional scenarios; `test-pq` runs unit tests for the priority queue.

## Next steps / Notes

- Run memory checks (valgrind) and CI to verify leak-free behavior.
- Polish formatting to fully satisfy the Norm and add more exhaustive EDF stress tests.

