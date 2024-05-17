

poetry install
poetry run python main.py --model gpt-3.5-turbo-1106 --apikey $OPENAI_API_KEY --ask "How to modify question method so it would support conversation history" --path `pwd`
