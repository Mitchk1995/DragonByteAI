# AI Dungeon Master

AI Dungeon Master is a text-based role-playing game that uses artificial intelligence to create dynamic and engaging storytelling experiences.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-dungeon-master.git
   cd ai-dungeon-master
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the MongoDB database:
   - Make sure MongoDB is installed and running on your system.
   - Create a `.env` file in the project root and add your MongoDB URI:
     ```
     MONGO_URI=mongodb://localhost:27017/ai_dungeon
     ```

5. Initialize the database:
   ```
   python src/init_db.py
   ```

## Usage

To start the game, run:

```
python src/app.py
```

Follow the on-screen prompts to create a character and begin your adventure!

## Project Structure

- `src/`: Contains the main application code
  - `app.py`: Flask application setup
  - `game_loop.py`: Main game loop
  - `models/`: Database models
  - `utils/`: Utility functions
  - `ai/`: AI-related modules
- `tests/`: Unit tests
- `venv/`: Virtual environment (created during installation)
- `requirements.txt`: List of Python dependencies
- `README.md`: This file

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
