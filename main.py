import json
from collections import deque, OrderedDict

# ------------ FIFO --------------
def fifo(frames_count, refs):
    frames = deque()
    frames_set = set()

    hits = 0
    faults = 0

    for page in refs:
        if page in frames_set:
            hits += 1
        else:
            faults += 1

            if len(frames) == frames_count:
                removed = frames.popleft()
                frames_set.remove(removed)

            frames.append(page)
            frames_set.add(page)

    return hits, faults, list(frames)


# ---------- LRU ------------
def lru(frames_count, refs):
    frames = OrderedDict()

    hits = 0
    faults = 0

    for page in refs:
        if page in frames:
            hits += 1
            frames.move_to_end(page)
        else:
            faults += 1

            if len(frames) == frames_count:
                frames.popitem(last=False)

            frames[page] = True

    return hits, faults, list(frames.keys())


# ---------------- CLOCK (Second Chance) ----------------
def clock(frames_count, refs):
    frames = [None] * frames_count
    ref_bit = [0] * frames_count
    pointer = 0

    hits = 0
    faults = 0

    def find(page):
        return page in frames

    def index(page):
        return frames.index(page)

    for page in refs:
        if find(page):
            hits += 1
            ref_bit[index(page)] = 1
        else:
            faults += 1

            while True:
                if frames[pointer] is None:
                    frames[pointer] = page
                    ref_bit[pointer] = 1
                    pointer = (pointer + 1) % frames_count
                    break

                if ref_bit[pointer] == 0:
                    frames[pointer] = page
                    ref_bit[pointer] = 1
                    pointer = (pointer + 1) % frames_count
                    break
                else:
                    ref_bit[pointer] = 0
                    pointer = (pointer + 1) % frames_count

    final = [p for p in frames if p is not None]
    return hits, faults, final


# ------------- MAIN -------------
def main():
    import sys

    input_data = json.load(open(sys.argv[1]))

    algo = input_data["algorithm"].upper()
    frames = input_data["frames"]
    refs = input_data["references"]

    if algo == "FIFO":
        hits, faults, final_frames = fifo(frames, refs)
    elif algo == "LRU":
        hits, faults, final_frames = lru(frames, refs)
    elif algo in ["CLOCK", "SECOND-CHANCE"]:
        hits, faults, final_frames = clock(frames, refs)
    else:
        raise ValueError("Unknown algorithm")

    output = {
        "algorithm": input_data["algorithm"],
        "frames": frames,
        "faults": faults,
        "hits": hits,
        "final_frames": final_frames
    }

    import re
    result = json.dumps(output, indent=2)
    result = re.sub(r'\[([^\[\]]+)\]', lambda m: '[' + ', '.join(v.strip() for v in m.group(1).split(',')) + ']', result, flags=re.DOTALL)
    print(result)


if __name__ == "__main__":
    main()