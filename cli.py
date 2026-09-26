import argparse
import json
from pathlib import Path
from metrics import evaluate

def main():
    parser = argparse.ArgumentParser(description='Evaluate fictional cross-app metric contracts')
    parser.add_argument('fixture')
    parser.add_argument('--audience', choices=['sales','finance','operations'], default='finance')
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.fixture).read_text(encoding='utf-8'))
        print(json.dumps(evaluate(data, args.audience), indent=2, sort_keys=True))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'Input error: {exc}\n')

if __name__ == '__main__':
    main()
