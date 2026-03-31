import json
import logging
from typing import Dict, Any

import ollama
from num2words import num2words


def get_int_input(prompt_msg: str) -> int:
    """Prompt the user for an integer until a valid one is provided."""
    while True:
        user_input = input(prompt_msg).strip()
        if not user_input:
            print("Please enter a valid number (e.g., 0).")
            continue
        try:
            return int(user_input)
        except ValueError:
            print(f"Invalid input: '{user_input}'. Please enter a whole number.")


def generate_prompt(
    note: str,
    mcq: int,
    marks1: int,
    marks2: int,
    marks3: int,
    marks5: int,
    want_answer: bool
) -> str:
    """Constructs the prompt string to send to the LLM."""
    prompt = "You are a teaching assistant. Read the following note and generate:\n"

    # MCQ/2/3/5 mark questions
    if mcq > 0:
        count_str = num2words(mcq).capitalize() if mcq > 1 else "One"
        suffix = "questions." if mcq > 1 else "question."
        prompt += f"\n{count_str} 1-mark MCQ {suffix}"

    if marks1 > 0:
        count_str = num2words(marks1).capitalize() if marks1 > 1 else "One"
        suffix = "questions." if marks1 > 1 else "question."
        prompt += f"\n{count_str} 1-mark SAQ {suffix}"

    if marks2 > 0:
        count_str = num2words(marks2).capitalize() if marks2 > 1 else "One"
        suffix = "questions." if marks2 > 1 else "question."
        prompt += f"\n{count_str} 2-mark {suffix}"

    if marks3 > 0:
        count_str = num2words(marks3).capitalize() if marks3 > 1 else "One"
        suffix = "questions." if marks3 > 1 else "question."
        prompt += f"\n{count_str} 3-mark {suffix}"

    if marks5 > 0:
        count_str = num2words(marks5).capitalize() if marks5 > 1 else "One"
        suffix = "questions." if marks5 > 1 else "question."
        prompt += f"\n{count_str} 5-mark {suffix}"

    prompt += f"\n\nNote:\n{note}"

    if want_answer:
        prompt += "\n\nAnd also give all answers according to the note."
    else:
        prompt += "\n\nDon't give me the answers."

    return prompt


def parse_and_save_json(note: str, generated_text: str, filename: str = "questions.json") -> None:
    """Parses text line-by-line and saves it as a JSON object."""
    # Process list
    lines = [line.strip() for line in generated_text.split('\n') if line.strip()]
    questions = []

    for line in lines:
        if line and (line[0].isdigit() or line.startswith("- ")):
            line = line.lstrip("0123456789.- ")
        questions.append(line)

    output_json: Dict[str, Any] = {
        "note": note.strip(),
        "questions": questions
    }

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output_json, f, indent=4, ensure_ascii=False)
        print(f"Questions successfully saved to '{filename}'")
    except Exception as e:
        print(f"Error occurred while saving to '{filename}': {e}")


def main() -> None:
    print("=== AI Questions Maker ===")
    print("Press Ctrl+C at any time to exit.\n")

    try:
        while True:
            question = input("Give me your study note (or type 'exit' to quit): ").strip()
            if question.lower() == 'exit':
                break
            if not question:
                print("Study note cannot be empty.")
                continue

            note = question
            mcq = get_int_input("How many mcqs do you want? (e.g., 0, 1, 2) : ")
            marks1 = get_int_input("How many 1 mark question do you need?   : ")
            marks2 = get_int_input("How many 2 mark question do you need?   : ")
            marks3 = get_int_input("How many 3 mark question do you need?   : ")
            marks5 = get_int_input("How many 5 mark question do you need?   : ")

            print("\n")
            answer_input = input("Do you want answers? (Yes/No): ").strip().lower()
            want_answer = answer_input in ("yes", "y", "true", "1")

            # Generate Prompt
            prompt = generate_prompt(
                note=note,
                mcq=mcq,
                marks1=marks1,
                marks2=marks2,
                marks3=marks3,
                marks5=marks5,
                want_answer=want_answer
            )

            print("\nGenerating... Please wait.\n")

            try:
                # LLM execution
                response = ollama.chat(
                    model='llama3.1:8b',
                    messages=[
                        {"role": "system", "content": "You are an AI that generates exam-style questions from educational notes."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                generated_text = response.get('message', {}).get('content', '').strip()
                if not generated_text:
                    print("Received empty response from the AI. Please try again.")
                    continue

                print("\n=== Generated Questions ===\n")
                print(generated_text)
                print("\n===========================\n")

                # Save output automatically replacing what was commented out
                parse_and_save_json(note=note, generated_text=generated_text)

            except Exception as e:
                print(f"An error occurred while communicating with Ollama: {e}")
                print("Make sure Ollama is running (`ollama serve`) and the model `llama3.1:8b` is pulled.")

            print("\n" + "-"*40 + "\n")

    except KeyboardInterrupt:
        print("\n\nExiting softly. Goodbye!")
    except EOFError:
        print("\n\nExiting softly. Goodbye!")


if __name__ == "__main__":
    # Suppress verbose module logs outside of our explicit prints
    logging.basicConfig(level=logging.WARNING)
    main()
