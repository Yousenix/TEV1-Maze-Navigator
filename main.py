import time



MAZE = """########...########
#..#.....#........#
#.##..###.###.##.##
#.................#
#.##.#.#####.#.##.#
#....#...#...#....#
####.###.#.###.####
#.................#
#.##.##.#.##.##.#.#
#@...#...#...#....#
###################"""



maze_rows = [list(row) for row in MAZE.splitlines()]

DIRECTIONS = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1)
}

def move_char(direction):
    global loc, previous_loc

    if direction not in DIRECTIONS:
        return False

    row_change, col_change = DIRECTIONS[direction]
    current_row, current_col = loc

    next_row = current_row + row_change
    next_col = current_col + col_change

    if not (0 <= next_row < len(maze_rows)):
        return False

    if not (0 <= next_col < len(maze_rows[next_row])):
        return False

    if maze_rows[next_row][next_col] == "#":
        return False

    previous_loc = loc

    maze_rows[current_row][current_col] = "."
    maze_rows[next_row][next_col] = "@"

    loc = (next_row, next_col)

    return True




import requests

OLLAMA_URL = "http://localhost:11434/v1/systemone"
MODEL = "tev1:0.8b"

CATEGORIES = {
    "up": (
        "Move UP by exactly one cell. "
        "The row index decreases by 1. "
        "Choose this only if the cell above is walkable "
        "and this move helps reach the goal."
    ),

    "down": (
        "Move DOWN by exactly one cell. "
        "The row index increases by 1. "
        "Choose this only if the cell below is walkable "
        "and this move helps reach the goal."
    ),

    "left": (
        "Move LEFT by exactly one cell. "
        "The column index decreases by 1. "
        "Choose this only if the cell to the left is walkable "
        "and this move helps reach the goal."
    ),

    "right": (
        "Move RIGHT by exactly one cell. "
        "The column index increases by 1. "
        "Choose this only if the cell to the right is walkable "
        "and this move helps reach the goal."
    )
}

previous_loc = None

def choose_move():
    valid_moves = get_valid_moves()
    payload = {
    "model": MODEL,
    "state": {
        "maze": maze_rows,
        "position": {
            "row": loc[0],
            "col": loc[1]
        },
        "goal": {
            "row": 0,
            "col": 9
        }
    },
    "questions": {
    "category": {
    "type": "choice",
    "instructions": """
You are the navigation controller for Pac-Man in a grid-based maze.

YOUR OBJECTIVE:
Guide Pac-Man from its current position to the goal at row 0, column 9.

MAZE REPRESENTATION:

* "#" means a wall. Pac-Man cannot enter a wall.
* "." means an open, walkable cell.
* "@" marks Pac-Man's current position.
* The goal is located at row 0, column 9.
* Row and column indices start at 0.

MOVEMENT RULES:

* "up": decrease the row index by 1.
* "down": increase the row index by 1.
* "left": decrease the column index by 1.
* "right": increase the column index by 1.
* Every move advances exactly one cell.
* Never move into a wall or outside the maze.

DECISION PROCESS:

1. Read the current maze and Pac-Man's current position.
2. Identify the goal position.
3. Consider the available direction choices.
4. Choose a legal move that helps Pac-Man reach the goal.
5. Avoid moving back and forth between the same positions.
6. Prefer exploring an unvisited corridor when the current route does not lead to the goal.
7. Do not assume that moving toward a smaller row or column index is always the best choice. Check the maze layout.

OUTPUT:
Select exactly one direction from the available choices.

""",
    "criteria": {
        direction: CATEGORIES[direction]
        for direction in valid_moves
    }    }
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()
    result = response.json()

    answer = result["answers"]["category"]

    return {
        "category": answer["choice"],
        "confidence": answer["confidence"],
        "probabilities": answer["probabilities"]
}

loc = (9,1)

def get_valid_moves():
    valid_moves = []
    row, col = loc

    for direction, (dr, dc) in DIRECTIONS.items():
        next_row = row + dr
        next_col = col + dc

        if not (0 <= next_row < len(maze_rows)):
            continue

        if not (0 <= next_col < len(maze_rows[next_row])):
            continue

        if maze_rows[next_row][next_col] == "#":
            continue

        if previous_loc == (next_row, next_col):
            continue

        valid_moves.append(direction)

    if not valid_moves:
        for direction, (dr, dc) in DIRECTIONS.items():
            next_row = row + dr
            next_col = col + dc

            if not (0 <= next_row < len(maze_rows)):
                continue

            if not (0 <= next_col < len(maze_rows[next_row])):
                continue

            if maze_rows[next_row][next_col] != "#":
                valid_moves.append(direction)

    return valid_moves  


goal = (0,9)

BLUE = lambda text: f"\033[34m{text}\033[0m"

def main():
    print(f"=== {BLUE("Smart maze")} ===")

    while True:
        if loc == goal:
            print("\n Pac-Man reached the goal!")
            break
        try:
            result = choose_move()

            print(f"\nCategory: {result['category']}")
            print(f"Confidence: {result['confidence']:.2%}")

            print("\nProbabilities:")
            for category, probability in result["probabilities"].items():
                print(f"  {category}: {probability:.2%}")

            direction = result["category"]
            moved = move_char(direction)

            if moved:

                for row in maze_rows:
                    print("".join(row))
            else:
                print(f"\nCannot move {direction}!")

            time.sleep(0.5)

        except requests.RequestException as error:
            print(f"Connection error: {error}")
            break

        except (KeyError, TypeError, ValueError) as error:
            print(f"Unexpected response from Ollama: {error}")
            break


if __name__ == "__main__":
    main()