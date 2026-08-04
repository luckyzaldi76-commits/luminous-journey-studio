from datetime import datetime
from datetime import timedelta

from services.production_service import ProductionService


class BatchProductionService:

    def run(self):

        print()
        print("=" * 60)
        print("BATCH PRODUCTION")
        print("=" * 60)

        start = input(
            "Start Date (YYYY-MM-DD): "
        ).strip()

        end = input(
            "End Date (YYYY-MM-DD): "
        ).strip()

        start_date = datetime.strptime(
            start,
            "%Y-%m-%d"
        )

        end_date = datetime.strptime(
            end,
            "%Y-%m-%d"
        )

        total = (
            end_date - start_date
        ).days + 1

        print()
        print(f"Total Days : {total}")

        current = start_date

        while current <= end_date:

            print()
            print("=" * 60)
            print(current.strftime("%Y-%m-%d"))
            print("=" * 60)

            production = ProductionService()

            production.run_auto(
                current.strftime("%Y-%m-%d")
            )

            current += timedelta(days=1)


batch_production_service = BatchProductionService()