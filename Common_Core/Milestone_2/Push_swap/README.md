*This project has been created as part of the 42 curriculum by rmedonca.*

# push_swap
[![C Language](https://img.shields.io/badge/language-C-555555?style=flat-square&logo=c)](https://devdocs.io/c/)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)
![42 Project](https://img.shields.io/badge/42-push_swap-blue?style=flat-square)

## Description

`push_swap` is a 42 project that challenges students to sort a stack of integers using **two stacks only** and a **restricted set of operations**.  
The objective is to generate the **shortest sequence of operations** that sorts the numbers efficiently.  

**Skills developed:**

| Area | Description |
|------|------------|
| Data Structures | Linked lists, stacks |
| Algorithms | Design, optimization, problem-solving |
| Constraints | Solving under limited operations |

The program outputs a series of operations that, when applied, will sort the input stack from **smallest to largest**.

## Instructions

### Compilation

Compile the program with:

```bash
make
```
This produces the executable push_swap.

## Execution 

Run the program by passing integers as arguments:

```bash
./push_swap [numbers separated by space]
```
Example:
```bash
./push_swap 3 2 1 5 4
```

Output (example):
```bash
pb
sa
pa
ra
```
Each line corresponds to one stack operation.

## Counting Operations

To measure the number of operations for a random list:
```bash
# For 100 numbers
shuf -i 1-100 | xargs ./push_swap | wc -l

# For 500 numbers
shuf -i 1-500 | xargs ./push_swap | wc -l
```

The number returned by wc -l is the total number of operations executed.

## Performance (Example)
| List size | Avg. operations |
| --------- | --------------- |
| 100       | 700 (example)   |
| 500       | 5500 (example)  |
These numbers vary depending on the random list.

## Resources

[Push_Swap Subject – 42](https://projects.intra.42.fr/projects/push_swap)

[C Standard Library Documentation](https://devdocs.io/c/)

[Linked List Concepts](https://www.geeksforgeeks.org/dsa/linked-list-data-structure/)

[Stack Data Structure](https://www.geeksforgeeks.org/dsa/stack-data-structure/)

### AI Usage

AI was used only for drafting explanations, testing examples, and clarifying strategies.
All source code, logic, and implementation were written manually by the author.

## Strategies & Optimizations

### Chunking: 
Divide large lists into smaller segments for easier sorting

### Selective Pushing:
Move elements to stack B strategically

### Minimal Rotations:
Choose ra or rra to minimize moves

### Operation Combinations:
Use ss, rr, and rrr to reduce total operations

### Example
```bash
./push_swap 3 2 1
```
Output:
```bash
pb
sa
pa
```
This sequence sorts the stack efficiently with 3 operations.