"""
pollinations.types.ImageModel

Classes:
    ImageModel (models.ImageModel): Text-to-image generative AI model.
    ImageObject (types.ImageObject): Image object.
"""

import random, time, json, io
from .. import abc
from .. import types
from ..requests.src import requests
from PIL import Image
import piexif


@abc.resource(deprecated=False)
class ImageModel:
    models: list = [
        "turbo",
        "dreamshaper",
        "deliberate",
        "pixart",
        "playground",
        "dpo",
        "dalle3xl",
        "formulaxl",
    ]
    params: dict = {
        "prompt": None,
        "width": 1024,
        "height": 1024,
        "seed": 0,
        "model": "turbo",
        "nologo": False,
        "nofeed": False,
        "enhance": None,
        "file": "pollinations-Image.png",
        "negative": "",
        "prompts": [],
        "negatives": [],
    }

    def __init__(self, file: str = "pollinations-Image.png", *args, **kwargs) -> None:
        self.default_filter: list = abc.filtered
        self.filter: list = self.default_filter
        self.data: object = object
        self.is_filtered: bool = False

        self.prompt: str = self.params.get("prompt", "...")
        self.negative: str = self.params.get("negative", "")
        self.width: int = self.params.get("width", 1024)
        self.height: int = self.params.get("height", 1024)
        self.seed: int = self.params.get("seed", random.randint(0, 2**32 - 1))
        self.model: str = self.params.get("model", "turbo")
        self.nologo: bool = self.params.get("nologo", False)
        self.nofeed: bool = self.params.get("nofeed", False)
        self.enhance: bool = self.params.get("enhance", None)

        self.file: str = self.params.get("file", file)

        self.prompts: list = self.params.get("prompts", [])
        self.negatives: list = self.params.get("negatives", [])

        self.enhanced_prompt: str = ""
        self.is_nsfw: bool = False

    def __repr__(self, *args, **kwargs) -> str:
        return f"ImageModel(file={self.file})"

    def set_filter(self, filter: list) -> None:
        self.filter: list = filter

    def extract_user_comment(self, image_bytes: bytes) -> str:
        image = Image.open(io.BytesIO(image_bytes))
        exif_dict = piexif.load(image.info["exif"])
        user_comment = exif_dict.get("Exif", {}).get(piexif.ExifIFD.UserComment, None)

        if user_comment:
            try:
                return user_comment.decode("utf-8")
            except UnicodeDecodeError:
                return "No user comment found."
        else:
            return "No user comment found."

    def generate(
        self,
        prompt: str = "...",
        *args,
        negative: str = "",
        width: int = 1024,
        height: int = 1024,
        seed: int = 0,
        model: str = None,
        nologo: bool = None,
        nofeed: bool = None,
        enhance: bool = None,
        **kwargs,
    ) -> types.ImageObject:
        if prompt != "..." and prompt != "":
            self.prompt: str = prompt
        if negative != "..." and negative != "":
            self.negative: str = negative
        if model != None:
            self.model: str = model
        if self.seed == "random" or seed == "random":
            self.seed: int = random.randint(0, 2**32 - 1)
        if nologo:
            self.nologo: bool = nologo
        if nofeed:
            self.nofeed: bool = nofeed
        if enhance:
            self.enhance: bool = enhance
        self.width: int = width
        self.height: int = height

        # setting filter like this is deprecated and returns a lot of false positives
        words: list = self.prompt.split(" ")

        for word in words:
            if word in self.filter:
                self.is_filtered: bool = True
                return Exception(f"types.ImageModel >>> InvalidPrompt (filtered)")

        words: list = self.negative.split(" ")

        for word in words:
            if word in self.filter:
                self.is_filtered: bool = True
                return Exception(f"types.ImageModel >>> InvalidPrompt (filtered)")

        request_build: str = "https://image.pollinations.ai/prompt/"
        request_build += self.prompt
        request_build += f"?width={self.width}&height={self.height}&seed={self.seed}&model={self.model}"
        request_build += f"&nologo={self.nologo}" if self.nologo else ""
        request_build += f"&nofeed={self.nofeed}" if self.nofeed else ""
        request_build += f"&negative={self.negative}" if self.negative != "" else ""
        request_build += f"&enhance={self.enhance}" if self.enhance != None else ""

        request: requests.Request = requests.get(request_build)

        try:
            user_comment = self.extract_user_comment(request.content)
            user_comment = user_comment[user_comment.find("{") :]
            user_comment = json.loads(user_comment)
            self.enhanced_prompt = user_comment["0"]["prompt"]
            self.enhanced_prompt = self.enhanced_prompt[: self.enhanced_prompt.rfind("\n")]
            self.is_nsfw = user_comment["0"]["has_nsfw_concept"]
        except Exception as e:
            print("Failed to Load User Comment, Error: ", e)
            self.enhanced_prompt = None
            self.is_nsfw = None

        self.data: types.ImageObject = types.ImageObject(
            prompt=self.prompt,
            negative=self.negative,
            width=self.width,
            height=self.height,
            model=self.model,
            seed=self.seed,
            url=request.url,
            date=time.strftime("%Y-%m-%d %H:%M:%S"),
            content=request.content,
            nologo=self.nologo,
            nofeed=self.nofeed,
            enhance=self.enhance,
            enhanced_prompt=self.enhanced_prompt,
            is_nsfw=self.is_nsfw,
        )
        self.data.save: object = self.save
        return self.data

    def generate_batch(
        self,
        prompts: list = ["..."],
        negative: list = ["..."],
        save: bool = False,
        path: str = "pollinations-Image.png",
        naming: str = "counter",
        *args,
        model: str = None,
        width: int = 1024,
        height: int = 1024,
        seed: int = 0,
        nologo: bool = False,
        nofeed: bool = False,
        enhance: bool = None,
        **kwargs,
    ) -> list[types.ImageObject]:
        if isinstance(self.prompt, list):
            self.prompts: list = self.prompt
        elif isinstance(self.prompts, list) and self.prompts != []:
            self.prompts: list = self.prompts
        else:
            self.prompts: list = prompts

        if isinstance(self.negative, list):
            self.negatives: list = self.negative
        elif isinstance(self.negatives, list) and self.negatives != []:
            self.negatives: list = self.negatives
        else:
            self.negatives: list = negative

        if len(self.prompts) != len(self.negatives):
            self.negatives: list = ["..." for _ in range(len(self.prompts))]

        if model != None:
            self.model: str = model
        if self.seed == "random" or seed == "random":
            self.seed: int = random.randint(0, 2**32 - 1)
        if nologo:
            self.nologo: bool = nologo
        if nofeed:
            self.nofeed: bool = nofeed
        if enhance:
            self.enhance: bool = enhance
        self.width: int = width
        self.height: int = height
        self.data: list = []
        counter: int = 1

        for index, prompt in enumerate(self.prompts):
            try:
                negative: str = self.negatives[index]
            except:
                negative: str = "..."
            words: list = prompt.split(" ")
            for word in words:
                if word in self.filter:
                    self.is_filtered: bool = True
                    return Exception(f"types.ImageModel >>> InvalidPrompt (filtered)")
            if negative != "..." and negative != "":
                words: list = negative.split(" ")
                for word in words:
                    if word in self.filter:
                        self.is_filtered: bool = True
                        return Exception(
                            f"types.ImageModel >>> InvalidPrompt (filtered)"
                        )

            request_build: str = "https://image.pollinations.ai/prompt/"
            request_build += prompt
            request_build += f"?width={self.width}&height={self.height}&seed={self.seed}&model={self.model}"
            request_build += f"&nologo={self.nologo}" if self.nologo else ""
            request_build += f"&nofeed={self.nofeed}" if self.nofeed else ""
            request_build += f"&enhance={self.enhance}" if self.enhance != None else ""
            if negative != "..." and negative != "":
                request_build += f"&negative={negative}"
            request: requests.Request = requests.get(request_build)

            try:
                user_comment = self.extract_user_comment(request.content)
                user_comment = user_comment[user_comment.find("{") :]
                user_comment = json.loads(user_comment)
                self.enhanced_prompt = user_comment["0"]["prompt"]
                self.enhanced_prompt = self.enhanced_prompt[: self.enhanced_prompt.rfind("\n")]
                self.is_nsfw = user_comment["0"]["has_nsfw_concept"]
            except Exception as e:
                print("Failed to Load User Comment, Error: ", e)
                self.enhanced_prompt = None
                self.is_nsfw = None

            image: types.ImageObject = types.ImageObject(
                prompt=prompt,
                negative=negative,
                width=self.width,
                height=self.height,
                model=self.model,
                seed=self.seed,
                url=request.url,
                date=time.strftime("%Y-%m-%d %H:%M:%S"),
                content=request.content,
                nologo=self.nologo,
                nofeed=self.nofeed,
                enhance=self.enhance,
                enhanced_prompt=self.enhanced_prompt,
                is_nsfw=self.is_nsfw,
            )
            image.save: object = self.save
            self.data.append(image)

            if save:
                if naming == "counter":
                    file_name: str = counter
                else:
                    file_name: str = prompt
                with open(
                    f'{path if path else ""}/batch{file_name}-pollinations.png', "wb"
                ) as handler:
                    handler.write(image.content)

            counter += 1
        return self.data

    def generate_random(
        self,
        *args,
        negative: str = "",
        width: int = 1024,
        height: int = 1024,
        seed: int = 0,
        model: str = None,
        nologo: bool = True,
        nofeed: bool = None,
        **kwargs,
    ) -> types.ImageObject:

        self.prompt: str = "Random Prompt"

        if negative != "..." and negative != "":
            self.negative: str = negative
        if model != None:
            self.model: str = model
        if self.seed == "random" or seed == "random":
            self.seed: int = random.randint(0, 2**32 - 1)
        if nologo:
            self.nologo: bool = nologo
        if nofeed:
            self.nofeed: bool = nofeed
        self.width: int = width
        self.height: int = height

        request_build: str = "https://image.pollinations.ai/prompt/"
        request_build += self.prompt
        request_build += f"?width={self.width}&height={self.height}&seed={self.seed}&model={self.model}"
        request_build += f"&nologo={self.nologo}" if self.nologo else ""
        request_build += f"&nofeed={self.nofeed}" if self.nofeed else ""
        request_build += f"&negative={self.negative}" if self.negative != "" else ""

        request: requests.Request = requests.get(request_build)

        try:
            user_comment = self.extract_user_comment(request.content)
            user_comment = user_comment[user_comment.find("{") :]
            user_comment = json.loads(user_comment)
            self.enhanced_prompt = user_comment["0"]["prompt"]
            self.enhanced_prompt = self.enhanced_prompt[: self.enhanced_prompt.rfind("\n")]
            self.is_nsfw = user_comment["0"]["has_nsfw_concept"]
        except Exception as e:
            print("Failed to Load User Comment, Error: ", e)
            self.enhanced_prompt = None
            self.is_nsfw = None

        self.data: types.ImageObject = types.ImageObject(
            prompt=self.prompt,
            negative=self.negative,
            width=self.width,
            height=self.height,
            model=self.model,
            seed=self.seed,
            url=request.url,
            date=time.strftime("%Y-%m-%d %H:%M:%S"),
            content=request.content,
            nologo=self.nologo,
            nofeed=self.nofeed,
            enhance=True,
            enhanced_prompt=self.enhanced_prompt,
            is_nsfw=self.is_nsfw,
        )
        self.data.save: object = self.save
        return self.data

    @abc.resource(deprecated=False)
    def save(self, file: str = None, *args, **kwargs) -> types.ImageObject:
        """
        pollinations.ai.types.ImageModel.save

        Parameters:
            file (str): File name to save the image to.

        Return:
            ImageObject (class): Returns the ImageObject for the saved image.
        """
        if not self.is_filtered:
            if file is None:
                file = self.file

            with open(file, "wb") as handler:
                handler.write(self.data.content)

            return self.data
        else:
            return Exception(f"types.ImageModel >>> Cannot Save (filtered)")

    @abc.resource(deprecated=False)
    def load(self, load_file: str = None, *args, **kwargs) -> str:
        """
        pollinations.ai.types.ImageModel.load

        Parameters:
            load_file (str): File name to load the image from.

        Return:
            str (binary): Returns the binary info of the image.
        """
        if load_file is None:
            load_file = self.file

        with open(load_file, "rb") as handler:
            return handler.read()

    @abc.resource(deprecated=False)
    def image(self, *args, **kwargs) -> types.ImageObject:
        """
        pollinations.ai.types.ImageModel.image

        Return:
            ImageObject (class): Returns the ImageObject for the image.
        """
        return self.data
