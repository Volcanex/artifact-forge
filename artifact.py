from abc import ABC, abstractmethod
import json
import pickle

class Artifact(ABC):
    def __init__(self, prompt, serialized_data=None, constructed=False, **kwargs):
        self.prompt = prompt
        self.mandatory_tags = {}
        self.optional_tags = {}
        self.serialized_data = serialized_data
        self.constructed = constructed
        self._data = None
        
        for key, value in kwargs.items():
            self.optional_tags[key] = value

    @classmethod
    @abstractmethod
    def build(cls, prompt, **kwargs):
        formatted_prompt = json.dumps({"prompt": prompt})
        return cls(formatted_prompt, **kwargs)

    @abstractmethod
    def generate_data(self, prompt):
        pass

    def validate_data(self, data):
        if data is None:
            raise RuntimeError("Generation failed to set the artifact data")

    def construct(self):
        if self.constructed:
            raise RuntimeError("Artifact is already constructed")
        
        if self.serialized_data is None:
            self._data = self.generate_data(self.prompt)
        else:
            self._data = self.deserialize_data(self.serialized_data)
        
        self.validate_data(self._data)
        self.constructed = True

    def serialize_data(self):
        return pickle.dumps(self._data)

    def deserialize_data(self, serialized_data):
        return pickle.loads(serialized_data)

    @property
    def data(self):
        if not self.constructed:
            raise RuntimeError("Artifact is not constructed yet")
        return self._data

class MediaMixin:
    def __init__(self, *args, start_time, end_time, **kwargs):
        super().__init__(*args, **kwargs)
        self.mandatory_tags['start_time'] = start_time
        self.mandatory_tags['end_time'] = end_time

    @classmethod
    def build(cls, prompt, start_time, end_time, **kwargs):
        formatted_prompt = json.dumps({"prompt": prompt})
        return cls(formatted_prompt, start_time=start_time, end_time=end_time, **kwargs)

    @property
    def duration(self):
        return self.mandatory_tags['end_time'] - self.mandatory_tags['start_time']

    @property
    def start_time(self):
        return self.mandatory_tags['start_time']

    @property
    def end_time(self):
        return self.mandatory_tags['end_time']

