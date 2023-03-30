# LLMChess 

## Repository Structure

```graphql
LLMChess/
│
├── engine/
│   └── engine.py           # Backend logic and LLM move calculation
│
├── static/
│   ├── css/
│   │   └── styles.css      # Styles for the frontend
│   ├── js/
│   │   └── script.js       # JavaScript for chessboard interaction
│   └── images/             # Chess piece images
│
├── templates/
│   └── index.html          # Frontend HTML file
│
├── main.py                 # Flask server
├── requirements.txt        # Python environment dependencies
└── README.md               # This file
```

## Installation and Setup

1. Clone the repository to your local machine:

```bash
git clone https://github.com/username/LLMChess.git
cd LLMChess
```

2. Set up a virtual environment and activate it:

```bash 
python3 -m venv venv
source venv/bin/activate   # For Unix systems
venv\Scripts\activate      # For Windows systems
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

4. Run the Flask server:

```bash
python main.py
```

5. Open your web browser and navigate to http://127.0.0.1:81/ to start playing the game.

## How to Play

See instructions on [webpage](https://llmchess.org/).


## License

LLMChess is released under the [MIT License](LICENSE).