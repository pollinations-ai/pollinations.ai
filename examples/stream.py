import pollinations

text_model = pollinations.Text()

def main() -> None:
    for token in text_model("This is a test.", stream=True):
        print(token, end="", flush=True)

    print()
    
main()
