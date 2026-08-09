from dataclasses import dataclass, field


@dataclass(slots=True)
class PipelineContext:

    gospel: str

    language: str

    audience: str

    outputs: dict = field(
        default_factory=dict,
    )

    metadata: dict = field(
        default_factory=dict,
    )

    analytics: dict = field(
        default_factory=dict,
    )

    def set(
        self,
        key: str,
        value,
    ):

        self.outputs[key] = value

        return value

    def get(
        self,
        key: str,
        default=None,
    ):

        return self.outputs.get(
            key,
            default,
        )

    def has(
        self,
        key: str,
    ) -> bool:

        return (
            key in self.outputs
        )

    def remove(
        self,
        key: str,
    ):

        self.outputs.pop(
            key,
            None,
        )

    def update(
        self,
        **kwargs,
    ):

        self.outputs.update(
            kwargs,
        )

    def clear_outputs(
        self,
    ):

        self.outputs.clear()

    def clear_metadata(
        self,
    ):

        self.metadata.clear()

    def clear_analytics(
        self,
    ):

        self.analytics.clear()

    def reset(
        self,
    ):

        self.clear_outputs()

        self.clear_metadata()

        self.clear_analytics()

    def to_dict(
        self,
    ) -> dict:

        return {

            "gospel": self.gospel,

            "language": self.language,

            "audience": self.audience,

            "outputs": self.outputs,

            "metadata": self.metadata,

            "analytics": self.analytics,

        }