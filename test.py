# test_web_scraper_artifact.py
from artifacts import WebScraperArtifact, MediaWebScraperArtifact, StabilityArtifact
import random
def test_web_scraper_artifact():
    url = 'https://www.reddit.com/'
    user_agent = 'Mozilla/5.0'
    
    #artifact = WebScraperArtifact.build(url, user_agent="Test")
    #artifact.construct()
    
    media_artifact = MediaWebScraperArtifact.build(url=url, start_time=0, end_time=60, user_agent=user_agent)
    media_artifact.construct()
    
    #print(f"Artifact Representation: {repr(artifact)}")
    print(f"Media Artifact Representation: {repr(media_artifact)}")
    
def test_stability_artifact():

    g = StabilityArtifact.build(prompt="A man in a tree",  
                                position_x=0,
                                position_y=0,
                                resolution_x=0, 
                                resolution_y=0
                                )
    g.construct()
        
    g.output_data_to_file("images/"+"testimage.png")
    
    
if __name__ == '__main__':
    test_web_scraper_artifact()