from artifact import Artifact, MediaMixin, GraphicalMixin
import requests
from bs4 import BeautifulSoup
from artifact_logger import setup_logger
from collections import deque
from typing import Any
import os 
import json
import tempfile
from mutagen.mp3 import MP3
class WebScraperArtifact(Artifact):
    def __init__(self, *args, user_agent: str = 'Mozilla/5.0', **kwargs):
        super().__init__(*args, **kwargs)
        self.user_agent = user_agent
        self.logger = setup_logger(self.__class__.__name__)

    @classmethod
    def build(cls, url: str, user_agent: str = 'Mozilla/5.0', payload_data=None, **kwargs):
        return cls({"url": url}, payload_data, user_agent=user_agent, **kwargs)

    def generate_data(self, prompt: dict, payload_data):
        url = prompt["url"]
        headers = {'User-Agent': self.user_agent}
        self.logger.info(f"Sending GET request to {url}")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            self.logger.info("Request successful. Parsing HTML content.")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = soup.title.text if soup.title else None
            paragraphs = [p.text for p in soup.find_all('p')]
            
            data = {
                'title': title,
                'paragraphs': paragraphs
            }
            
            metadata = {
                'url': url,
                'status_code': response.status_code,
                'content_type': response.headers.get('Content-Type')
            }
            
            self.logger.info("Data and metadata generated successfully.")
            return data, metadata
        else:
            self.logger.error(f"Failed to scrape the webpage. Status code: {response.status_code}")
            raise RuntimeError(f"Failed to scrape the webpage. Status code: {response.status_code}")

class MediaWebScraperArtifact(WebScraperArtifact, MediaMixin):
    pass
class StabilityArtifact(Artifact, GraphicalMixin):
    def __init__(self, *args, **kwargs):
        self.logger = setup_logger(self.__class__.__name__)
        super().__init__(*args, **kwargs)
        
    @classmethod
    def build(cls, prompt: str, position_x: int, position_y: int, resolution_x: int, resolution_y: int, **kwargs):
        logger = setup_logger(cls.__name__)
        logger.debug(f"Building {cls.__name__} with prompt: {prompt[:50]}, position: ({position_x}, {position_y}), resolution: {resolution_x}x{resolution_y}")
        
        prompt_dict = {
            "prompt": prompt,
            "resolution": f"{resolution_x},{resolution_y}"
        }
        
        mandatory_tags = {
            "position_x": position_x,
            "position_y": position_y
        }
        
        return cls(prompt_dict, mandatory_tags=mandatory_tags, **kwargs)

    def generate_image(self, prompt: str):
        self.logger.info(f"Generating image with prompt: {prompt[:50]}...")
        api_url = "https://api.stability.ai/v2beta/stable-image/generate/core"
        api_key = os.getenv("STABILITY_API_KEY")
        
        if api_key is None:
            self.logger.error("STABILITY_API_KEY environment variable is not set.")
            raise ValueError("STABILITY_API_KEY environment variable is not set.")
        
        headers = {
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        }
        data = {
            "prompt": prompt,
            "output_format": "png"
        }
        files = {"none": ''}
        
        try:
            self.logger.debug("Sending request to Stability API")
            response = requests.post(api_url, headers=headers, files=files, data=data)
            
            if response.status_code == 200:
                self.logger.info("Image generated successfully")
                image_data = response.content
                return image_data
            else:
                self.logger.error(f"API request failed with status code: {response.status_code}")
                raise Exception(str(response.json()))
        except Exception as e:
            self.logger.error(f"Error in Stability API call: {str(e)}")
            raise

    def generate_data(self, prompt: dict, payload_data):
        self.logger.info("Generating data for Stability artifact")
        image_data = self.generate_image(prompt["prompt"])
        
        data = {
            "image": image_data
        }
        
        metadata = {
            "prompt": prompt["prompt"]
        }
        
        if "resolution" in prompt:
            metadata["resolution"] = prompt["resolution"]
        
        return data, metadata

    def validate_data(self, data: dict):
        self.logger.debug("Validating Stability artifact data")
        super().validate_data(data)
        if not isinstance(data.get("image"), bytes):
            self.logger.error("Validation failed: Image data is not in bytes format")
            raise ValueError("Image data must be in bytes format")
        self.logger.info("Stability artifact data validated successfully")
        
    def output_data_to_file(self, filepath: str):
        """
        Output the StabilityArtifact's image data to a file.
        
        :param filepath: The path where the image file should be saved.
        """
        if not self.constructed:
            raise ValueError("StabilityArtifact must be constructed before outputting data.")

        if 'image' not in self.data or not isinstance(self.data['image'], bytes):
            raise ValueError("StabilityArtifact does not contain valid image data.")

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'wb') as f:
            f.write(self.data['image'])

        # Write metadata to a separate JSON file
        metadata_filepath = os.path.splitext(filepath)[0] + '_metadata.json'
        with open(metadata_filepath, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2)

        self.logger.info(f"Image data output to file: {filepath}")
        self.logger.info(f"Metadata output to file: {metadata_filepath}")
        
class MediaStabilityArtifact(MediaMixin, StabilityArtifact):
    pass

class NarrationArtifact(Artifact):
    def __init__(self, *args, **kwargs):
        self.logger = setup_logger(self.__class__.__name__)
        super().__init__(*args, **kwargs)

    @classmethod
    def build(cls, prompt: str, **kwargs):
        logger = setup_logger(cls.__name__)
        logger.debug(f"Building {cls.__name__} with prompt: {prompt[:50]}...")
        
        prompt_dict = {
            "prompt": prompt
        }
        
        return cls(prompt_dict, **kwargs)

    def generate_data(self, prompt: dict, payload_data):
        self.logger.info(f"Generating audio data for prompt: {prompt['prompt'][:50]}...")
        url = f"https://api.elevenlabs.io/v1/text-to-speech/29vD33N1CtxCmqQRPOHJ"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": os.getenv("ELEVEN_API_KEY")
        }
        data = {
            "text": prompt['prompt'],
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        CHUNK_SIZE = 1024 
        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 200:
            response_content = json.loads(response.content)
            self.logger.error(f"API request failed. Status code: {response.status_code}. Detail: {response_content.get('detail')}")
            raise ValueError(f"Request failed with status code {response.status_code}")
    
        audio_data = b''
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                audio_data += chunk
        
        try:
            duration = self.get_audio_duration(audio_data)
            self.logger.info(f"Audio generated successfully. Duration: {duration} seconds")
        except Exception as e:
            self.logger.error(f"Error getting audio duration: {str(e)}")
            raise ValueError("Likely invalid audio data, could be network issue?")
        
        data = {
            "audio": audio_data
        }
        
        metadata = {
            "duration": duration,
            "prompt": prompt['prompt']
        }
        
        return data, metadata

    def get_audio_duration(self, audio_data):
        self.logger.debug("Getting audio duration")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name

        audio = MP3(temp_file_path)
        duration = audio.info.length
        os.remove(temp_file_path)
        self.logger.debug(f"Audio duration: {duration} seconds")
        return duration

    def validate_data(self, data: dict):
        self.logger.debug("Validating Narration artifact data")
        super().validate_data(data)
        if not isinstance(data.get("audio"), bytes):
            self.logger.error("Validation failed: Audio data is not in bytes format")
            raise ValueError("Audio data must be in bytes format")
        self.logger.info("Narration artifact data validated successfully")

class MediaNarrationArtifact(MediaMixin, NarrationArtifact):
    @classmethod
    def build(cls, prompt: str, start_time: float, end_time: float, **kwargs):
        logger = setup_logger(cls.__name__)
        logger.debug(f"Building {cls.__name__} with prompt: {prompt[:50]}, start_time: {start_time}, end_time: {end_time}")
        
        prompt_dict = {
            "prompt": prompt
        }
        
        mandatory_tags = {
            "start_time": start_time,
            "end_time": end_time
        }
        
        return cls(prompt_dict, mandatory_tags=mandatory_tags, **kwargs)