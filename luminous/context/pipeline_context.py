from dataclasses import dataclass, field

@dataclass
class PipelineContext:

    gospel: str

    language: str

    audience: str

    outputs: dict = field(default_factory=dict)

    metadata: dict = field(default_factory=dict)

    analytics: dict = field(default_factory=dict)