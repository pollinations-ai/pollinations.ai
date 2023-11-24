import random
from .. import abc

samples: list = abc.samples
styles: dict = {
    "realistic": "realistic, realism, real life, ultra realistic, high quality, real",
    "cartoon": "cartoony, cartoon, cartoonish",
    "anime": "anime, anime art, anime style",
    "logo": "logo, logo design, logo graphic design, logo digital art",
}

realistic: str = styles.get("realistic")
cartoon: str = styles.get("cartoon")
anime: str = styles.get("anime")
logo: str = styles.get("logo")


@abc.resource(deprecated=False)
def sample_style(*args, **kwargs):
    return styles.get(random.choice(list(styles.keys())))


@abc.resource(deprecated=False)
def sample(*args, **kwargs) -> str:
    return f"prompt: {random.choice(samples)}, details: ({sample_style()})"


@abc.resource(deprecated=False)
def sample_batch(size: int, *args, **kwargs) -> str:
    return [sample() for iter in range(size)]
