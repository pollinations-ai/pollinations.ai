import pollinations

text_model = pollinations.Text(
    model="openai", 
    system="You are a helpful assistant.", 
    contextual=True,
    private=True,
    seed="random"
)

def main() -> None:
    while True:
        prompt = input("User: ")
        if prompt.lower().strip() == "exit":
            break
        
        print("Assistant: ", end="", flush=True)
        
        # print(text_model(prompt))
        for token in text_model(prompt, stream=True):
            print(token, end="", flush=True)

        print("\n")
        
main()
