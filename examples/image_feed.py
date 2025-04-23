import pollinations

feed = pollinations.Feed(
    type="image",
    max_data=10  # Optional: If None then will be indefinite
)

def main() -> None:
    for item in feed():  # feed.Get()
        print(len(feed.data), item, item["width"])
        
main()
