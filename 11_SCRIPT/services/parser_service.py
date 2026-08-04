from core.markdown_parser import parse_markdown


class ParserService:

    def parse(self, response):

        print()
        print("=" * 60)
        print("MARKDOWN PARSER")
        print("=" * 60)

        data = parse_markdown(response)

        print(f"Sections Found : {len(data)}")

        return data


parser_service = ParserService()