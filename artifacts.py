from artifact import Artifact, MediaMixin
import requests
from bs4 import BeautifulSoup
from logger_config import setup_logger

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

# Review what system we're using for mixin constructors
class MediaWebScraperArtifact(WebScraperArtifact, MediaMixin):
    @classmethod
    def build(cls, url: str, start_time: int, end_time: int, user_agent: str = 'Mozilla/5.0', payload_data=None, **kwargs):
        return cls({"url": url}, payload_data, start_time=start_time, end_time=end_time, user_agent=user_agent, **kwargs)