from ljcli.main import build_parser


def main():

    parser = build_parser()

    args = parser.parse_args(
        [
            "batch",
            "--gospel",
            "Lukas 5:33-39",
            "--languages",
            "IND,ENG,ESP",
            "--audience",
            "adult",
            "--output-dir",
            "exports/test-batch",
            "--workflow",
            "Daily Gospel",
        ]
    )

    assert args.command == "batch"

    assert args.gospel == (
        "Lukas 5:33-39"
    )

    assert args.languages == (
        "IND,ENG,ESP"
    )

    assert args.audience == "adult"

    assert args.output_dir == (
        "exports/test-batch"
    )

    assert args.workflow == (
        "Daily Gospel"
    )

    print("=" * 60)
    print(
        "CLI BATCH GENERATION TEST PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
