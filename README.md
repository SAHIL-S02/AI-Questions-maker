# AI Questions Maker

A professional command-line tool to automatically generate study questions (MCQs, short answer, and long answer) from your study notes using the Ollama LLM.

## Features

- **Interactive Prompts:** Simple interactive flow to specify the exact number of 1-mark, 2-mark, 3-mark, and 5-mark questions you want.
- **Local AI:** Uses `ollama` with the `llama3.1:8b` model to run queries entirely locally.
- **Answer Generation:** Option to include or exclude answers with the generated questions.
- **JSON Export:** Automatically saves generated questions and notes into `questions.json` for easy parsing.

## Prerequisites

1. Install [Ollama](https://ollama.com/)
2. Pull the required model:
```bash
ollama run llama3.1:8b
```
3. Python 3.8+

## Setup

1. Clone this repository (or download the source).
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

Simply run the main script. The tool will interactively prompt you for your study notes and preferences.

```bash
python main.py
```

### Example

```text
Give me your study note : Mitochondria is the powerhouse of the cell.
How many mcqs do you want? : 2
How many 1 mark question do you need? : 0
How many 2 mark question do you need? : 1
How many 3 mark question do you need? : 0
How many 5 mark question do you need? : 0
Do you want answer? (Yes/No): Yes
```

## Output

Generated questions will be printed directly to the console and saved to `questions.json` in the same directory.
