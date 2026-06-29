import argparse
import json

from src.agent.graph import build_agent


def main():
    parser = argparse.ArgumentParser(description="Run the multimodal engineering agent.")
    parser.add_argument("--query", required=True, help="Natural language query")
    parser.add_argument("--file", required=True, help="Input engineering data file")
    args = parser.parse_args()

    app = build_agent()
    result = app.invoke(
        {
            "query": args.query,
            "file_path": args.file,
            "file_type": None,
            "task_type": None,
            "result": None,
            "error": None,
        }
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
