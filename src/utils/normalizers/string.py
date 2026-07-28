# This class normalize string data
class StringNormalizer:


    def normalize(
        self,
        value: str
    ) -> str:

        return value.strip().lower()


string_normalizer = StringNormalizer()