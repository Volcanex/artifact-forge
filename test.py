# test_web_scraper_artifact.py
from artifacts import WebScraperArtifact

def test_web_scraper_artifact():
    url = 'https://example.com'
    user_agent = 'Custom User Agent'
    
    artifact = WebScraperArtifact.build(url, user_agent=user_agent)
    artifact.construct()
    
    print(f"Artifact Representation: {repr(artifact)}")

if __name__ == '__main__':
    test_web_scraper_artifact()