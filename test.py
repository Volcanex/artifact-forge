# test_web_scraper_artifact.py
from artifacts import WebScraperArtifact, MediaWebScraperArtifact, StabilityArtifact
import random
def test_web_scraper_artifact():
    url = 'https://www.reddit.com/'
    user_agent = 'Mozilla/5.0'
    
    #artifact = WebScraperArtifact.build(url, user_agent="Test")
    #artifact.construct()
    
    media_artifact = MediaWebScraperArtifact.build(url, 0, 60, user_agent=user_agent)
    media_artifact.construct()
    
    #print(f"Artifact Representation: {repr(artifact)}")
    print(f"Media Artifact Representation: {repr(media_artifact)}")
    
def test_stability_artifact():

    g = StabilityArtifact.build("A man in a tree", 0, 0, 256, 256)
    g.construct()
        
    g.output_data_to_file("images/"+"testimage.png")
    
    
if __name__ == '__main__':
    test_stability_artifact()