import argparse

from code_assistant import assistant


def main(ask: str, model: str, api_key: str, code_path: str | None):
    print(assistant.question(ask, model, api_key, code_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Code Assistant CLI')
    parser.add_argument('--model', type=str, required=True, help='Model to use')
    parser.add_argument('--apikey', type=str, required=True, help='API Key')
    parser.add_argument('--ask', type=str, required=True, help='Question')
    parser.add_argument('--path', type=str, required=True, help='Existing code path')

    args = parser.parse_args()
    main(ask=args.ask, model=args.model, api_key=args.apikey, code_path=args.path)
