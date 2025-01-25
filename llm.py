from llama_cpp import Llama
from pathlib import Path
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse command-line arguments for completion with local model."
    )
    parser.add_argument(
        "--model", type=str, required=True, help="Path to the model file."
    )
    parser.add_argument(
        "--input", type=str, required=True, help="Path to the input file."
    )
    parser.add_argument(
        "--output", type=str, required=True, help="Path to the output file."
    )
    args = parser.parse_args()

    llm = Llama(model_path=args.model, n_ctx=2048)
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": Path(args.input).read_text()},
        ]
    )
    content = response["choices"][0]["message"]["content"]
    if content:
        Path(args.output).write_text(content)
    else:
        raise RuntimeError("Failed to generate output file")
