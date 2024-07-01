from artifact import Artifact, MediaMixin
import json
import requests
from bs4 import BeautifulSoup
from artifact import Artifact
from logger_config import setup_logger
class WebScraperArtifact(Artifact):
    def __init__(self, *args, user_agent='Mozilla/5.0', **kwargs):
        super().__init__(*args, **kwargs)
        self.user_agent = user_agent
        self.logger = setup_logger(self.__class__.__name__)

    @classmethod
    def build(cls, prompt, user_agent='Mozilla/5.0', payload_data=None, **kwargs):
        formatted_prompt = json.dumps({"url": prompt})
        return cls(formatted_prompt, payload_data, user_agent=user_agent, **kwargs)

    def generate_data(self, prompt, payload_data):
        url = json.loads(prompt)['url']
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
            return json.dumps(data), json.dumps(metadata)
        else:
            self.logger.error(f"Failed to scrape the webpage. Status code: {response.status_code}")
            raise RuntimeError(f"Failed to scrape the webpage. Status code: {response.status_code}")