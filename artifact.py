from abc import ABC, abstractmethod
import json
import inspect
from logger_config import setup_logger

class Artifact(ABC):
    def __init__(self, prompt: dict, payload_data=None, mandatory_tags: dict = None, optional_tags: dict = None, data: dict = None, metadata: dict = None, constructed: bool = False, **kwargs):
        self.prompt = prompt
        self.payload_data = payload_data
        self.mandatory_tags = mandatory_tags or {}
        self.optional_tags = optional_tags or {}
        self.data = data
        self.metadata = metadata
        self.constructed = constructed
        
        self.logger = setup_logger(self.__class__.__name__)
        
        if (data is None) != (metadata is None):
            raise ValueError("Can't load data without metadata or vice versa.")

        if not constructed:
            if (data is not None) or (metadata is not None):
                raise ValueError("Can't load data or metadata into an unconstructed artifact, set constructed to true.")
        
        excluded_keys = ['prompt', 'payload_data', 'mandatory_tags', 'optional_tags', 'data', 'metadata', 'constructed']
        for key, value in kwargs.items():
            if key not in excluded_keys:
                self.optional_tags[key] = value
        
        # Should this check be done elsewhere?
        def is_json_serializable(data):
            try:
                json.dumps(data)
                return True
            except (TypeError, OverflowError, ValueError):
                return False
    
        if not is_json_serializable(self.prompt):
            raise ValueError("Prompt must be JSON serializable.")
        if not is_json_serializable(self.mandatory_tags):
            raise ValueError("Mandatory tags must be JSON serializable.")
        if not is_json_serializable(self.optional_tags):
            raise ValueError("Optional tags must be JSON serializable.")
        if metadata is not None and not is_json_serializable(self.metadata):
            raise ValueError("Metadata must be JSON serializable.")
        
        if constructed:
            self.construct()
    
    @classmethod
    @abstractmethod
    def build(cls, prompt: dict, payload_data=None, **kwargs):
        return cls(prompt, payload_data, **kwargs)

    @abstractmethod
    def generate_data(self, prompt: dict, payload_data):
        # Returns data, metadata
        pass

    def validate_data(self, data: dict):
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
    @classmethod
    def combine_build(cls, build_method1, build_method2):
        # Combines two build method, implement
        pass
    
class MediaMixin(Artifact):
    def __init__(self, *args, start_time: int, end_time: int, **kwargs):
        super().__init__(*args, **kwargs)
        self.mandatory_tags['start_time'] = start_time
        self.mandatory_tags['end_time'] = end_time

    @classmethod
    def build(cls, start_time: int, end_time: int, **kwargs):
        return cls(start_time=start_time, end_time=end_time, **kwargs)

    @property
    def duration(self) -> int:
        return self.mandatory_tags['end_time'] - self.mandatory_tags['start_time']

    @property
    def start_time(self) -> int:
        return self.mandatory_tags['start_time']

    @property
    def end_time(self) -> int:
        return self.mandatory_tags['end_time']