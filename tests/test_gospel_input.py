import tempfile
from pathlib import Path

from openpyxl import Workbook

from services.gospel_input import (
    GospelInputService,
)


def main():

    with tempfile.TemporaryDirectory() as tmp:

        database = Path(tmp) / "TGL.xlsx"

        workbook = Workbook()
        sheet = workbook.active

        sheet.append(
            [
                "reference",
                "text",
                "language",
            ]
        )

        sheet.append(
            [
                "Lukas 5:33-39",
                "Anggur baru harus disimpan dalam kantong yang baru.",
                "IND",
            ]
        )

        workbook.save(database)
        workbook.close()

        service = GospelInputService(
            database
        )

        result = service.find(
            "Lukas 5:33-39"
        )

        assert result is not None
        assert (
            result.reference
            == "Lukas 5:33-39"
        )
        assert (
            result.language
            == "IND"
        )
        assert (
            "Anggur baru"
            in result.text
        )

        created = service.create(
            "Lukas 5:33-39",
            "Test Gospel",
            "ind",
        )

        assert created.reference == (
            "Lukas 5:33-39"
        )
        assert created.text == "Test Gospel"
        assert created.language == "IND"

        try:
            service.validate("")
            raise AssertionError(
                "Empty Gospel should fail."
            )
        except ValueError:
            pass

    print("=" * 60)
    print("GOSPEL INPUT TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
