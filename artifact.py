from abc import ABC, abstractmethod
import json
class Artifact(ABC):
    def __init__(self, prompt, payload_data=None, mandatory_tags='', optional_tags='', data=None, metadata=None, constructed=False, **kwargs):
        self.prompt = prompt # JSON
        self.payload_data = payload_data # Any
        self.mandatory_tags = mandatory_tags # JSON
        self.optional_tags = optional_tags # JSON
        self.data = data # JSON
        self.metadata = metadata # JSON
        self.constructed = constructed # Bool
        
        if (data is None) != (metadata is None):
            raise ValueError("Can't load data without metadata or vice versa.")

        if not constructed:
            if (data is not None) or (metadata is not None):
                raise ValueError("Can't load data or metadata into an unconstructed artifact, set constructed to true.")
            
        excluded_keys = ['prompt', 'payload_data', 'mandatory_tags', 'optional_tags', 'data', 'metadata', 'constructed']
        for key, value in kwargs.items():
            if key not in excluded_keys:
                optional_tags = json.loads(self.optional_tags)
                optional_tags[key] = value
                self.optional_tags = json.dumps(optional_tags)
            
        if constructed:
            self.construct()
            
    @classmethod
    @abstractmethod
    def build(cls, prompt, payload_data=None, **kwargs):
        formatted_prompt = json.dumps({"prompt": prompt})
        return cls(formatted_prompt, payload_data, **kwargs)

    @abstractmethod
    def generate_data(self, prompt, payload_data):
        # Returns data, metadata
        pass

    def validate_data(self, data):
        if data is None:
            raise RuntimeError("Generation failed to set the artifact data")

    def construct(self):
        if self.constructed:
            raise RuntimeError("Artifact is already constructed")
        
        if self.data is None:
            self.data, self.metadata = self.generate_data(self.prompt, self.payload_data)
            
        self.validate_data(self.data)
        self.constructed = True
        
    def __repr__(self):
        return f"Artifact(prompt={self.prompt}, payload_data={self.payload_data}, mandatory_tags={self.mandatory_tags}, optional_tags={self.optional_tags}, data={self.data}, metadata={self.metadata}, constructed={self.constructed})"

class MediaMixin:
    def __init__(self, *args, start_time, end_time, **kwargs):
        super().__init__(*args, **kwargs)
        mandatory_tags = json.loads(self.mandatory_tags) if self.mandatory_tags else {}
        mandatory_tags['start_time'] = start_time
        mandatory_tags['end_time'] = end_time
        self.mandatory_tags = json.dumps(mandatory_tags)

    @classmethod
    def build(cls, prompt, start_time, end_time, payload_data=None, **kwargs):
        formatted_prompt = json.dumps({"prompt": prompt})
        return super().build(formatted_prompt, payload_data, start_time=start_time, end_time=end_time, **kwargs)

    @property
    def duration(self):
        tags = json.loads(self.mandatory_tags)
        return tags['end_time'] - tags['start_time']

    @property
    def start_time(self):
        return json.loads(self.mandatory_tags)['start_time']

    @property
    def end_time(self):
        return json.loads(self.mandatory_tags)['end_time']