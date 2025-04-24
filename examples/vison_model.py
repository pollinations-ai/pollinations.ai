import pollinations

text_model = pollinations.Text(
    model="openai",  # Use vision capable model
)

def main() -> None:
    text_model.Image(["image.png", "image1.png"])  # text_model.Image("image.png") works as well
    print(text_model("Describe the images"))
    
main()
