# This class normalize email data
class EmailNormalizer:


    def normalize(
        self,
        email: str
    ) -> str:

        return email.strip().lower()


email_normalizer = EmailNormalizer()