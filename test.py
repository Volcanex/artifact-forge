# test_web_scraper_artifact.py
from artifacts import WebScraperArtifact, MediaWebScraperArtifact

def test_web_scraper_artifact():
    url = 'https://www.reddit.com/'
    user_agent = 'Mozilla/5.0'
    
    #artifact = WebScraperArtifact.build(url, user_agent="Test")
    #artifact.construct()
    
    media_artifact = MediaWebScraperArtifact.build(url, start_time=0, end_time=60, user_agent=user_agent)
    media_artifact.construct()
    
    #print(f"Artifact Representation: {repr(artifact)}")
    print(f"Media Artifact Representation: {repr(media_artifact)}")

if __name__ == '__main__':
    test_web_scraper_artifact()