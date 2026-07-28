# This class normalize date data
from datetime import datetime
from fastapi import HTTPException


class DateNormalizer:


    def normalize(
        self,
        value: str
    ) -> datetime:

        try:

            return datetime.strptime(
                value.strip(),
                "%Y-%m-%d"
            )

        except ValueError:

            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use YYYY-MM-DD"
            )


date_normalizer = DateNormalizer()