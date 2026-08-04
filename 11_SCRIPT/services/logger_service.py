from datetime import datetime
from pathlib import Path


class LoggerService:

    def log(
        self,
        output_dir,
        message
    ):

        # Pastikan output_dir selalu berupa Path
        output_dir = Path(output_dir)

        logfile = output_dir / "production.log"

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            logfile,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                f"[{timestamp}] {message}\n"
            )

        print(message)


logger_service = LoggerService()