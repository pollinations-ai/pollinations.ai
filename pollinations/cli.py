import argparse

import pollinations as pollinations

from pollinations.core.text import Text
from pollinations.core.image import Image


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pollinations",
        description="Work with the best generative AI from Pollinations using this Python SDK. 🐝",
    )

    parser.add_argument(
        "--version", action="version", version="%(prog)s " + pollinations.__version__
    )

    parser.add_argument("--text", action="store_true", help="Generate text")
    parser.add_argument("--image", action="store_true", help="Generate images")

    parser.add_argument("--prompt", type=str, help="Prompt to generate text or image")
    parser.add_argument(
        "--negative", type=str, help="Negative prompt to generate images", default=""
    )
    parser.add_argument("--model", type=str, help="Model to use", default="flux")
    parser.add_argument(
        "--system",
        type=str,
        help="System prompt for text models",
        default="You are a helpful AI assistant.",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="The file name to save generated images",
        default="pollinations-image.png",
    )
    parser.add_argument(
        "--private",
        type=str,
        help="Private request (not displayed on public feed for text and images) | USE: (t, f, true, false) Case insensitive",
        default=False,
    )
    parser.add_argument(
        "--seed", type=str, help="Use: int or `random`", default="random"
    )
    parser.add_argument(
        "--width", type=int, help="The width for generated images", default=1024
    )
    parser.add_argument(
        "--height", type=int, help="The height for generated images", default=1024
    )
    parser.add_argument(
        "--nologo", type=bool, help="Remove the pollinations watermark", default=False
    )
    parser.add_argument(
        "--enhance",
        type=bool,
        help="Use AI to enhance your image prompts",
        default=False,
    )

    args = parser.parse_args()
    first_sent = False

    if args.text:
        text_model = Text(
            model=args.model, system=args.system, private=args.private, seed=args.seed
        )

        print("Pollinations - Waiting...")
        for token in text_model(args.prompt, stream=True):
            if not first_sent:
                print("\033[F\033[K", end="")
            first_sent = True
            print(token, end="", flush=True)

        print()
        first_sent = False

    if args.image:
        image_model = Image(
            model=args.model,
            seed=args.seed,
            file=args.file,
            width=args.width,
            height=args.height,
            negative=args.negative,
            private=args.private,
            enhance=args.enhance,
        )

        print("Pollinations - Waiting...")

        image_model(args.prompt, save=True)
        print("\033[F\033[K", end="")
        first_sent = False
