# Page Replacement Algorithm Simulator (FIFO, LRU, CLOCK)

## Description
This project is a Python 3 simulation of three page replacement algorithms used in operating systems: FIFO (First-In First-Out), LRU (Least Recently Used), and CLOCK (Second-Chance Algorithm).

The program reads an input JSON file, runs the selected algorithm, and outputs a JSON result containing the number of hits, faults, and the final state of memory frames.

## How to Run
python3 main.py input.json > output.json

## Input Format
The program expects a JSON file in the following format:

{
  "algorithm": "FIFO",
  "frames": 3,
  "references": [1, 2, 3, 4, 1, 2, 5]
}

Fields:
- algorithm: FIFO, LRU, or CLOCK / SECOND-CHANCE
- frames: number of available memory frames (must be > 0)
- references: list of page numbers to process

## Output Format
The program outputs a JSON object in the following format:

{
  "algorithm": "FIFO",
  "frames": 3,
  "faults": 5,
  "hits": 2,
  "final_frames": [1, 2, 5]
}

## Design Decisions
- FIFO uses a queue (deque) to maintain insertion order.
- LRU uses an OrderedDict to track page usage recency.
- CLOCK uses a circular buffer with reference bits to approximate LRU behavior.
- Each algorithm is implemented as a separate function for modularity and clarity.
- All algorithms return consistent outputs: hits, faults, and final frame state.

## Algorithm Details

### FIFO (First-In First-Out)
Maintains a queue of pages in arrival order. On a page fault, the oldest page (front of the queue) is removed and the new page is added to the back.

### LRU (Least Recently Used)
Uses an OrderedDict to track usage order. When a page is accessed, it is moved to the most recent position. On a page fault, the least recently used page (oldest entry) is evicted.

### CLOCK (Second-Chance Algorithm)
Uses a circular buffer with a “hand” pointer and a reference bit for each frame.

- On a hit: the page’s reference bit is set to 1.
- On a fault: the hand moves through frames.
  - If reference bit is 1, it is cleared and the page is skipped.
  - The first page with reference bit 0 is evicted.

## AI Usage Statement
AI tools were used in a limited way to help understand page replacement algorithms and to assist in structuring and formatting documentation.