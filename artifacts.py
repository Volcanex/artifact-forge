from artifact import Artifact, MediaMixin
import json

class NarrationArtifact(Artifact):
    @classmethod
    def build(cls, prompt, voice_id=None, **kwargs):
        formatted_prompt = json.dumps({"prompt": prompt})
        instance = cls(formatted_prompt, **kwargs)
        if voice_id:
            instance.optional_tags['voice_id'] = voice_id
        return instance

    def generate_data(self, prompt):
        # Implementation for generating narration data
        pass

class MediaNarrationArtifact(MediaMixin, NarrationArtifact):
    pass