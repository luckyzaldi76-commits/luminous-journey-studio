from pathlib import Path
from typing import Dict

from engine.production_engine import ProductionEngine
from services.gospel_input import GospelInputService
from services.job_service import JobService


class ProductionContentPipeline:

    def __init__(
        self,
        engine=None,
        gospel_input=None,
        job_service=None,
    ):

        self.engine = (
            engine
            or ProductionEngine()
        )

        self.gospel_input = (
            gospel_input
            or GospelInputService()
        )

        self.job_service = (
            job_service
            or JobService()
        )

    def generate(
        self,
        gospel: str,
        language: str,
        audience: str,
        output_dir: Path,
        workflow_name: str = "Daily Gospel",
    ) -> Dict:

        gospel = (
            self.gospel_input
            .validate(gospel)
        )

        if not language.strip():

            raise ValueError(
                "Language cannot be empty."
            )

        if not audience.strip():

            raise ValueError(
                "Audience cannot be empty."
            )

        output_dir = Path(
            output_dir
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        job = self.job_service.create()

        self.job_service.start(
            job.job_id
        )

        try:

            result = self.engine.run(
                gospel=gospel,
                language=language,
                audience=audience,
                output_dir=output_dir,
                workflow_name=workflow_name,
            )

            if not isinstance(
                result,
                dict,
            ):

                raise TypeError(
                    "Production engine must return a dict."
                )

            result.setdefault(
                "gospel",
                gospel,
            )

            result.setdefault(
                "language",
                language,
            )

            result.setdefault(
                "audience",
                audience,
            )

            result.setdefault(
                "workflow",
                workflow_name,
            )

            result.setdefault(
                "output_dir",
                str(output_dir),
            )

            self.job_service.complete(
                job.job_id,
                result,
            )

            result["job_id"] = (
                job.job_id
            )

            result["job_status"] = (
                "completed"
            )

            return result

        except Exception as error:

            self.job_service.fail(
                job.job_id,
                str(error),
            )

            raise
