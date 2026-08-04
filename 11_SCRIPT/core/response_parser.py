import json


class ResponseParser:

    def parse(self, text):

        try:

            return json.loads(text)

        except:

            return {
                "raw": text
            }


parser = ResponseParser()