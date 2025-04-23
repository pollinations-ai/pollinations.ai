import pollinations

feed = pollinations.Feed(
    type="text",
    max_data=10  # Optional: If None then will be indefinite
)

def main() -> None:
    for item in feed():  # feed.Get()
        print(len(feed.data), item, item.data["parameters"]["seed"])
        
main()
