# TEV1 Maze Navigator

A small Python maze-navigation experiment that uses a locally running TEV1 language model to choose Pac-Man's next move.

The project sends the current maze, Pac-Man's position, the goal position, and the available movement choices to a local API. The API returns a direction, and the Python program applies that move if it is legal.

## Features

- Uses the local `tev1:0.8b` model.
- Represents the maze as a grid:
  - `#` — wall
  - `.` — walkable cell
  - `@` — Pac-Man's current position
- Tracks Pac-Man's current position and a goal coordinate.
- Filters out moves that would hit a wall or leave the maze.
- Prints the model's selected direction, confidence, probabilities, and updated maze.

## Requirements

- Python 3.10 or newer
- [Ollama](https://ollama.com/) installed and running locally
- The `tev1:0.8b` model available in Ollama
- A local service that implements the project's `/v1/systemone` endpoint
- Python package: `requests`

> **Important:** This project uses `http://localhost:11434/v1/systemone`. That is a custom endpoint, not one of Ollama's usual built-in API routes. Installing Ollama and downloading the model may not be enough on its own: make sure the service that provides `/v1/systemone` is running and accepts the request format used in `pacman.py`.

## Setup

### 1. Get the project

Clone the repository, or download it from GitHub and open a terminal in the project folder.

```bash
git clone https://github.com/YOUR-USERNAME/TEV1-Maze-Navigator.git
cd TEV1-Maze-Navigator
```

Replace `YOUR-USERNAME` with your GitHub username. If you downloaded the repository as a ZIP file, open a terminal in the extracted folder instead.

### 2. Create a virtual environment (recommended)

**Windows:**

```powershell
py -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Download the model

If you use Ollama and the model is available under this name, run:

```bash
ollama pull tev1:0.8b
```

Check that it appears in the local model list:

```bash
ollama list
```

### 5. Start the required local API service

Make sure Ollama is running and that the service providing `/v1/systemone` is available at:

```text
http://localhost:11434/v1/systemone
```

If your setup uses a separate server or extension for this endpoint, start that service according to its own instructions.

## Run the game

From the project folder, run:

```bash
python pacman.py
```

The program should print the model's chosen direction and the updated maze after each move.

Press `Ctrl+C` in the terminal to stop the program if it does not stop on its own.

## How it works

1. The maze is stored as a grid of characters.
2. The program finds Pac-Man's current position.
3. It determines which neighboring cells are legal moves.
4. It sends the current state and available choices to the local model API.
5. The model selects a direction.
6. Python checks and applies the move, then prints the updated maze.

The model's output is a suggestion, so the Python program should still validate every move before changing the game state.

## Configuration

The main settings are near the top of `pacman.py`:

```python
OLLAMA_URL = "http://localhost:11434/v1/systemone"
MODEL = "tev1:0.8b"
```

The goal is supplied in the game state. Update its row and column if you change the maze or want to choose a different destination. Row and column indices start at `0`.

## Troubleshooting

### Connection error

- Check that the local model service is running.
- Confirm that the endpoint URL and port match your setup.
- Remember that `/v1/systemone` is custom; a standard Ollama installation may not provide it automatically.

### Model not found

Run `ollama list` and confirm that `tev1:0.8b` is installed. If the model is available in your Ollama library, you can try `ollama pull tev1:0.8b`.

### Pac-Man repeats moves

A language model may choose a locally valid move that does not make progress toward the goal. Make sure the prompt includes the goal coordinates and the current maze state. Tracking visited positions or using a pathfinding algorithm such as BFS can make navigation more reliable.

## Project status

This is an experimental learning project for exploring local language models, structured inputs, classification-style choices, and grid navigation. The model's decisions are not guaranteed to be optimal for every maze.

## License

No license has been specified yet. Add a `LICENSE` file if you want to define how others may use, modify, and distribute the project.
