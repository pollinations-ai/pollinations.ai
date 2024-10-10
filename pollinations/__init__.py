__version__: str = "2.0.9"

import requests
import datetime
import difflib
import chardet
import random
import string
import pytz
import time
import sys
import io

from PIL import Image
from serpapi import GoogleSearch

_keystore: dict = {"serpapi": False}

TEXT_API: str = "text.pollinations.ai"
IMAGE_API: str = "image.pollinations.ai"
HEADER: dict = {"Content-Type": "application/json"}
ASPECT_RATIOS: dict = {"1:1": (1024, 1024), "3:4": (768, 1024), "16:9": (1024, 576)}

text_default: str = "openai"
openai: str = "openai"
mistral: str = "mistral"
mistral_large: str = "mistral-large"
llama: str = "llama"
karma: str = "karma"
command_r: str = "command-r"
unity: str = "unity"
midjourney: str = "midjourney"
rtist: str = "rtist"

image_default: str = "flux"
turbo: str = "turbo"
flux: str = "flux"
flux_realism: str = "flux-realism"
flux_pro: str = "flux-pro"
flux_anime: str = "flux-anime"
flux_3D: str = "flux-3d"
flux_cablyai: str = "flux-cablyai"
any_dark: str = "any-dark"


def text_models(*args, **kwargs) -> tuple:
    models: list = []
    request: requests.Request = requests.get(
        url=f"https://{TEXT_API}/models", headers=HEADER, timeout=30
    )
    for model in request.json():
        models.append(model["name"])
    return tuple(models)


def image_models(*args, **kwargs) -> list:
    request: requests.Request = requests.get(
        url=f"https://{IMAGE_API}/models", headers=HEADER, timeout=30
    )
    return tuple(request.json())


def keys(serpapi: str = False, *args, **kwargs) -> None:
    _keystore["serpapi"] = serpapi


class TextObject(object):
    def __init__(
        self,
        text: str = "",
        prompt: str = "",
        model: str = "",
        messages: list = [],
        params: dict = {},
        *args,
        **kwargs,
    ) -> None:
        self.text: str = str(text)
        self.prompt: str = str(prompt)
        self.model: str = str(model)
        self.messages: list = list(messages)
        self.params: dict = dict(params)
        self.time: str = f"[{datetime.date.today().strftime('%Y-%m-%d')}] {time.strftime('%H:%M:%S')}"

    def __str__(self) -> str:
        return (
            f"TextObject({self.text=}, {self.prompt=}, {self.model=}, {self.time=}, self.messages=[...], self.params="
            + "{...})"
        )

    def __repr__(self) -> repr:
        return repr(self.__str__())


class ImageObject(object):
    def __init__(
        self,
        prompt: str = "",
        negative: str = "",
        model: str = "",
        params: dict = {},
        *args,
        **kwargs,
    ) -> None:
        self.prompt: str = str(prompt)
        self.negative: str = str(negative)
        self.model: str = str(model)
        self.params: dict = dict(params)
        self.time: str = f"[{datetime.date.today().strftime('%Y-%m-%d')}] {time.strftime('%H:%M:%S')}"

    def save(self, file: str="image-output.png", *args, **kwargs) -> object:
        request: requests.Request = requests.get(
            url=self.params["url"],
            headers=HEADER,
            timeout=30,
        )
        Image.open(io.BytesIO(request.content)).save(file)

    def __str__(self) -> str:
        return f"ImageObject({self.prompt=}, {self.negative=}, {self.model=}, {self.params=}, {self.time=})"

    def __repr__(self) -> repr:
        return repr(self.__str__())


class TextModel(object):
    def __init__(
        self,
        frequency_penalty: tuple[int, float] = 0,
        presence_penalty: tuple[int, float] = 0,
        temperature: tuple[int, float] = 0.5,
        top_p: tuple[int, float] = 1,
        model: str = "openai",
        stream: bool = True,
        contextual: bool = False,
        system: str = "",
        *args,
        **kwargs,
    ) -> None:
        self.frequency_penalty: tuple[int, float] = float(frequency_penalty)
        self.presence_penalty: tuple[int, float] = float(presence_penalty)
        self.temperature: tuple[int, float] = float(temperature)
        self.top_p: tuple[int, float] = float(top_p)
        self.model: str = str(model)
        self.stream: bool = bool(stream)
        self.contextual: bool = bool(contextual)
        self.system: str = str(system)
        self.messages: list = list()
        self.limit: list = list([0, 10])

        self.system_create: object = lambda _: {"role": "system", "content": str(_)}
        self.user_create: object = lambda _: {"role": "user", "content": str(_)}
        self.assistant_create: object = lambda _: {
            "role": "assistant",
            "content": str(_),
        }

        self.messages.append(self.system_create(self.system))

    def generate(
        self, prompt: str, display: bool = False, *args, **kwargs
    ) -> TextObject:
        prompt: str = str(prompt)
        display: bool = bool(display)

        params: dict = {
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": self.stream,
            "system": self.system,
            "model": self.model,
            "url": f"https://{TEXT_API}/"
        }

        if self.limit[0] >= self.limit[1]:
            self.messages.pop(1)

        self.messages.append(self.user_create(prompt))
        self.limit[0] += 1

        if self.contextual:
            params["messages"] = self.messages
            url: str = params["url"]
            request: requests.Request = requests.post(
                url, json=params, headers=HEADER, timeout=30
            )
        else:
            url: str = f"https://{TEXT_API}/{prompt}"
            request: requests.Request = requests.get(
                url,
                params=params,
                headers=HEADER,
                timeout=30,
            )

        if request.status_code == 200:
            try:
                content: str = request.content.decode("utf-8")
            except:
                result: dict = chardet.detect(request.content)
                encoding: str = result['encoding']
                content: str = request.content.decode(encoding)
        else:
            content: str = "An error occurred during generation, try a new prompt."

        self.messages.append(self.assistant_create(content))
        self.limit[0] += 1

        if display:
            for i, character in enumerate(content):
                if i > 0 and content[i - 1] not in set(
                    string.ascii_letters + string.digits + " \t\n"
                ):
                    time.sleep(random.uniform(0.1, 0.3))
                else:
                    time.sleep(random.uniform(0.01, 0.05))

                sys.stdout.write(character)
                sys.stdout.flush()

            print()

        params["url"] = url
        text_object: TextObject = TextObject(
            text=content,
            prompt=prompt,
            model=self.model,
            messages=self.messages,
            params=params,
        )
        return text_object


class ImageModel(object):
    def __init__(
        self,
        model: str = "flux",
        seed: int = 0,
        width: int = 1024,
        height: int = 1024,
        enhance: bool = False,
        nologo: bool = False,
        private: bool = False,
        *args,
        **kwargs,
    ) -> None:
        self.model: str = str(model)
        self.seed: int = (
            int(seed)
            if str(seed).lower().strip() != "random"
            else random.randint(0, 9999999999)
        )
        self.width: int = int(width)
        self.height: int = int(height)
        self.enhance: bool = bool(enhance)
        self.nologo: bool = bool(nologo)
        self.private: bool = bool(private)

        try:
            aspect_ratio_input = width / height

            closest_ratio_width = 0
            closest_ratio_height = 0
            closest_difference = float("inf")

            for _, (rat_width, rat_height) in ASPECT_RATIOS.items():
                aspect_ratio_ratio = rat_width / rat_height
                difference = abs(aspect_ratio_ratio - aspect_ratio_input)

                if difference < closest_difference:
                    closest_difference = difference
                    closest_ratio_width = rat_width
                    closest_ratio_height = rat_height

            self.width: int = int(closest_ratio_width)
            self.height: int = int(closest_ratio_height)
        except:
            pass

    def generate(
        self,
        prompt: str,
        negative: str = "",
        save: bool = False,
        file: str = "image-output.png",
        *args,
        **kwargs,
    ) -> ImageObject:
        prompt: str = str(prompt)
        save: bool = bool(save)
        file: str = str(file)

        params: str = f"negative={negative}&seed={self.seed}&width={self.width}&height={self.height}&nologo={self.nologo}&private={self.private}&model={self.model}&enhance={self.enhance}"
        url: str = f"https://{IMAGE_API}/prompt/{prompt}?{params}"
        request: requests.Request = requests.get(
            url=url,
            headers=HEADER,
            timeout=30,
        )
        try:
            image: Image = Image.open(io.BytesIO(request.content))
            if save:
                image.save(file)
            w_h: tuple = (self.width, self.height)
            if w_h == (1024, 1024):
                aspect_ratio: str = "1:1"
            elif w_h == (768, 1024):
                aspect_ratio: str = "3:4"
            elif w_h == (1024, 576):
                aspect_ratio: str = "16:9"
            else:
                aspect_ratio: str = "N/A"
            params = {
                "aspect": aspect_ratio,
                "seed": self.seed,
                "width": self.width,
                "height": self.height,
                "nologo": self.nologo,
                "private": self.private,
                "enhance": self.enhance,
                "url": url
            }
            image_object: ImageObject = ImageObject(
                prompt=prompt, negative=negative, model=self.model, params=params
            )
            return image_object
        except:
            return "Image failed to generate, please try again."


class MultiModel(object):
    def __init__(
        self,
        system: str = "",
        default: str = None,
        text_model: str = "openai",
        image_model: str = "turbo",
        *args,
        **kwargs,
    ) -> None:
        self.models: list = image_models()
        self.system: str = str(system)
        self.default: str = str(default)
        self.details: dict = {}

        self.distinguish_model: TextModel = TextModel(
            model=text_model,
            system="Your task is to determine if the user's prompt is requesting an image generation. Look for specific clues such as the user asking for 'image', 'picture', 'art', 'visuals', 'graph', or any related visual terms. If you are unsure but the user seems to describe something that could be represented visually (like 'draw', 'design', 'generate a photo'), assume they want an image. Respond with just 'Y' (for image generation) wrapped in triple backticks (```Y```). If the user does not seem to want an image, respond with 'N' in the same format (```N```). Don't provide any additional text or explanation.",
        )

        self.guesser_model: TextModel = TextModel(
            model=text_model,
            system=f"""Your task is to choose the best model for generating the image described by the user. The available models are:
                - Turbo (default): For general image generation.
                - Flux: Ideal for abstract, creative visuals.
                - Flux-Realism: For realistic images.
                - Flux-Anime: For anime-style images.
                - Flux-3D: For 3D-rendered images.
                - Flux-Pro: Pro version of Realism & 3D.
                - Flux-CablyAi: 3D-cartoonish images.
                - Any-Dark: Realistic images with vibrant colors. Less trained.

                Read the prompt carefully and analyze for clues on the desired style. If the user mentions 'realistic', 'real-life', or 'natural', choose Flux-Realism. If they mention 'anime', 'cartoon', or '2D-style', choose Flux-Anime. For '3D', 'render', or '3D model', choose Flux-3D. Otherwise, use Turbo. Or if they hint for you to mutate the image description, etc.

                Respond with only the model name, wrapped in triple backticks (```<model>```), without any additional text.""",
        )

        self.main_model: TextModel = TextModel(
            model=text_model,
            system=f"Provide concise responses. Act as a test model and engage lightly without offering assistance unless explicitly requested. {self.system}",
            contextual=True,
        )

        self.image_model: ImageModel = ImageModel(
            enhance=True, model=image_model, private=True, nologo=True
        )

    def __closest(self, name: str, *args, **kwargs) -> str:
        name: str = str(name)

        closest_matches = difflib.get_close_matches(name, self.models, n=1)
        return closest_matches[0] if closest_matches else self.models[0]

    def generate(
        self,
        prompt: str,
        display: bool = False,
        provide_details: bool = False,
        *args,
        **kwargs,
    ) -> tuple:
        prompt: str = str(prompt)
        display: bool = bool(display)
        provide_details: bool = bool(provide_details)

        gen_type: str = str(self.distinguish_model.generate(prompt).text)
        try:
            gen_type: str = (
                gen_type.split("```", 1)[1].split("```", 1)[0].strip().lower()
            )
        except:
            pass

        details: dict = {"Prompt": prompt, "Img": gen_type}

        if gen_type == "y":
            content_1: str = self.main_model.generate(
                f"Dont wrap in quotes. Dont engage in conversation or say other stuff. Say something like: 'Sure!', 'Of course,', etc, 'Generating your image! but relate it to the user's prompt: {prompt}' (Might need to look at chat history)",
                display,
            )
            enhanced: str = self.main_model.generate(
                f"Dont wrap in quotes. Say what the user wants to generate with images for the image generator, enhance the prompt very slightly. Only say the new prompt (no other text): (Might need to look at chat history) Prompt: {prompt}"
            )

            if self.default == "None":
                model_guess: str = str(self.guesser_model.generate(enhanced.text).text)
                try:
                    model_guess: str = (
                        model_guess.split("```", 1)[1]
                        .split("```", 1)[0]
                        .strip()
                        .lower()
                    )
                except:
                    model_guess: str = "turbo"
                closest: str = self.__closest(model_guess)
            else:
                model_guess: str = self.default
                closest: str = self.default

            self.image_model.model = closest
            try:
                content_2: str = self.image_model.generate(enhanced.text, "", True)
            except:
                content_2: str = self.main_model.generate(
                    "Make an apology that the image generator didn't work.", display
                )

            content: list = [content_1, content_2]

            details["Enhanced"] = enhanced
            details["ModelGuess"] = model_guess
            details["Closest"] = closest
        else:
            content_1: str = self.main_model.generate(prompt, display)
            content: list = [content_1]

        self.details[len(self.details)] = details
        if provide_details:
            content.append(details)

        return tuple(content)


class SmartModel(object):
    def __init__(self, system: str = "", text_model: str="openai", image_model: str=None, *args, **kwargs) -> None:
        self.distinguish_model: TextModel = TextModel(
            model=mistral_large,
            contextual=True,
            system="""Your task is to determine what the user is asking for: 
                    1. **Time**: Look for clues that suggest the user wants to know the current time or date, such as 'what's the time', 'what time is it', 'current time', or related phrases. If the user asks for the time, respond with ```get_time(<timezone>)``` where `<timezone>` is a valid timezone (e.g., 'America/New_York').

                    2. **Weather**: Look for phrases like 'what's the weather', 'temperature', 'forecast', or anything suggesting the user is asking for the current weather. Respond with ```get_weather(<location>)```, where `<location>` is the place they are asking about (e.g., 'new york').

                    3. **Search**: If the user is asking for world, recent news, general information, or anything that would require a web search (like 'find', 'latest news', 'search', 'latest', etc, or asking questions about topics), respond with ```get_search(<search term>)```. 

                    4. **Combined Requests**: If the user requests both time and a search, or weather and search, or even all three, combine them. For example:
                    - For time and weather, use ```get_time_and_weather(<timezone>, <location>)```.
                    - For time and search, use ```get_time_and_search(<timezone>, <search term>)```.
                    - For weather and search, use ```get_weather_and_search(<location>, <search term>)```.

                    If you don't detect any of these, respond with ```N``` for 'None' (no action). Wrap the responses in triple backticks (```...```). Handle ambiguous prompts carefully, assuming the most relevant option when unclear.
                    
                    Remember, the user won't tell you to use get_time, get_weather, get_search, etc exactly, so if they indirectly ask for you to fetch something, make sure you use it.
                    """,
        )
        self.main_model: MultiModel = MultiModel(
            system=system,
            default=image_model,
            text_model=text_model,
            image_model=image_model
        )

        self.methods: dict = {
            "n": None,
            "get_time": lambda d_r: self.get_time(d_r),
            "get_weather": lambda d_r: self.get_weather(d_r),
            "get_search": lambda d_r: self.get_search(d_r),
            "get_time_and_search": lambda d_r: self.get_time_and_search(d_r),
            "get_time_and_weather": lambda d_r: self.get_time_and_weather(d_r),
            "get_weather_and_search": lambda d_r: self.get_weather_and_search(d_r),
            "get_time_and_weather_and_search": lambda d_r: self.get_time_and_weather_and_search(
                d_r
            ),
        }

    def get_time(self, timezone: str="UTC") -> str:
        try:
            tz = (
                timezone.split("(", 1)[-1].split(")", 1)[0].strip()
                if "(" in timezone
                else "UTC"
            )
            tz = pytz.timezone(tz)
        except:
            tz = pytz.timezone("UTC")
        now = datetime.datetime.now(tz)
        return f"Y-M-D H-M-S: {now.strftime('%Y-%m-%d %I:%M:%S %p')} (Timezone: {timezone})"

    def get_weather(self, location: str) -> str:
        location = location.replace(" ", "%20")
        url = f"https://api.open-meteo.com/v1/forecast?latitude=0&longitude=0&current_weather=true"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            weather_info = data.get("current_weather", {})
            temperature = weather_info.get("temperature", "N/A")
            condition = weather_info.get("weathercode", "N/A")
            return f"Current temperature in {location}: {temperature}°C, Condition: {condition}"
        else:
            return f"Could not fetch weather for {location}"

    def get_search(self, query: str) -> str:
        if _keystore["serpapi"] == False:
            text: str = "To make searches, please provide a search api key using:\n>>> pollinations.keys(serpapi='key')\n>>> To get a key go to https://serpapi.com/"
            return f"No search results found. Tell the user that you cannot perform searches since the devloper didn't provide an API key. How developer can add one: {text}"

        search = GoogleSearch(
            {
                "q": query,
                "api_key": _keystore["serpapi"],
                "num": 2,
            }
        )

        results = search.get_dict()
        output = ""

        if "organic_results" in results:
            for result in results["organic_results"]:
                title = result.get("title", "No Title")
                link = result.get("link", "#")
                snippet = result.get("snippet", "No snippet available.")

                output += f"Title: {title}\nURL: {link}\nSnippet: {snippet}\n\n"
        else:
            output = "No search results found."

        return output

    def get_time_and_search(self, query: str) -> str:
        tz, search = query.split(",", 1)
        return f"{self.get_time(tz.strip())} | {self.get_search(search.strip())}"

    def get_time_and_weather(self, query: str) -> str:
        tz, location = query.split(",", 1)
        return f"{self.get_time(tz.strip())} | {self.get_weather(location.strip())}"

    def get_weather_and_search(self, query: str) -> str:
        place, search = query.split(",", 1)
        return f"{self.get_weather(place.strip())} | {self.get_search(search.strip())}"

    def get_time_and_weather_and_search(self, query: str) -> str:
        tz, place, search = query.split(",", 2)
        return f"{self.get_time(tz.strip())} | {self.get_weather(place.strip())} | {self.get_search(search.strip())}"

    def generate(
        self, prompt: str, display: bool = False, provide_details: bool = False
    ) -> TextObject:
        check: str = self.main_model.distinguish_model.generate(prompt)
        self.main_model.distinguish_model.messages.pop()

        try:
            check: str = (
                check.text.split("```", 1)[1].split("```", 1)[0].strip().lower()
            )
        except:
            check: str = "n"

        if check == "n":
            distinguish_response: str = self.distinguish_model.generate(prompt)
            try:
                distinguish_response: str = (
                    str(distinguish_response.text)
                    .split("```", 1)[1]
                    .split("```", 1)[0]
                    .lower()
                    .strip()
                )
            except:
                distinguish_response: str = "n"

            distinguish_type: str = distinguish_response.split("(", 1)[0].strip()

            if distinguish_type in self.methods and self.methods[distinguish_type]:
                message: dict = self.main_model.main_model.system_create(
                    f"{distinguish_response} -> {self.methods[distinguish_type](distinguish_response)}"
                )
                self.main_model.main_model.messages.append(message)
                self.main_model.guesser_model.messages.append(message)
                self.main_model.distinguish_model.messages.append(message)
                prompt = f"{prompt}"

        content: str = self.main_model.generate(prompt, display, provide_details)
        return content


def text(
    frequency_penalty: tuple[int, float] = 0,
    presence_penalty: tuple[int, float] = 0,
    temperature: tuple[int, float] = 0.5,
    top_p: tuple[int, float] = 1,
    model: str = text_default,
    stream: bool = True,
    contextual: bool = False,
    system: str = "",
    *args,
    **kwargs,
) -> TextModel:
    return TextModel(
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        temperature=temperature,
        top_p=top_p,
        model=model,
        stream=stream,
        contextual=contextual,
        system=system,
        *args,
        **kwargs,
    )


def image(
    model: str = image_default,
    seed: int = "random",
    width: int = 1024,
    height: int = 1024,
    enhance: bool = False,
    nologo: bool = False,
    private: bool = False,
    *args,
    **kwargs,
) -> ImageModel:
    return ImageModel(
        model=model,
        seed=seed,
        width=width,
        height=height,
        enhance=enhance,
        nologo=nologo,
        private=private,
        *args,
        **kwargs,
    )


def multi(
    system: str = "",
    default: tuple[None, str] = None,
    text_model: str = text_default,
    image_model: str = image_default,
    *args,
    **kwargs,
) -> MultiModel:
    return MultiModel(
        system=system,
        default=default,
        text_model=text_model,
        image_model=image_model,
        *args,
        **kwargs,
    )


def smart(
        system: str = "", 
        text_model: str=text_default,
        image_model: str=None,
        *args, **kwargs) -> SmartModel:
    return SmartModel(
        system=system,
        text_model=text_model,
        image_model=image_model,
        *args, **kwargs
    )
