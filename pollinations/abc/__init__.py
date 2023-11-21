from .imageprotocol import ImageProtocol

proto: str = 'https://'
ai: str = '.ai/prompt/'

def resource(deprecated: bool=False):
  def decorator(func):
    func.deprecated: bool = deprecated
    return func
  return decorator

@resource(deprecated=False)
class ImageObject(ImageProtocol):
  def __init__(self, prompt: str, url: str, date: str, content: bin, *args, **kwargs) -> None:
      self.prompt: str = prompt
      self.url: str = url
      self.date: str = date
      self.content: bin = content

  def __repr__(self, *args, **kwargs) -> str:
      return f"ImageObject(prompt={self.prompt}, date={self.date}, url={self.url}, content={len(self.content)})"


samples: list = [
  "Cat",
  "Sunset",
  "Tree",
  "Abstract art",
  "Beach landscape",
  "City skyline at night",
  "Vintage car",
  "Mystical forest",
  "Rainy day",
  "Mountain peak",
  "Underwater world",
  "Family portrait",
  "Space exploration",
  "Dreamy clouds",
  "Autumn foliage",
  "Urban street scene",
  "Ancient ruins",
  "Endless desert",
  "Tropical paradise",
  "Fantasy castle",
  "Abstract patterns",
  "Ocean waves",
  "Garden flowers",
  "Fireworks display",
  "Snowy mountain range",
  "Wildlife safari",
  "Futuristic cityscape",
  "Countryside farmhouse",
  "Waterfall in the jungle",
  "Still life with fruits",
  "Industrial machinery",
  "Magical fairy tale",
  "Sports action shot",
  "Haunted house",
  "Vintage portrait",
  "Nighttime city traffic",
  "Majestic eagle",
  "Rainbow over a meadow",
  "Steampunk-inspired scene",
  "Cute puppies and kittens",
  "Abstract geometric shapes",
  "Artificial intelligence",
  "Dramatic storm clouds",
  "Historical landmarks",
  "Colorful hot air balloons",
  "Rural farm landscape",
  "Reflections on water",
  "Gloomy cemetery",
  "Astronaut in space",
  "Abstract surrealism",
]
