

# install dependencies
poetry install

# Options:
- `--model` - model name: for example gpt-3.5-turbo-1106 or gpt-4o 
- `--apikey` - OpenAI API key
- `--ask` - question to ask
- `--path` - path of existing code to provide context for the question

# Run code
poetry run python main.py \
    --model gpt-4o \
    --apikey $OPENAI_API_KEY \
    --ask "How to modify question method so it would support conversation history" \
    --path `pwd`
