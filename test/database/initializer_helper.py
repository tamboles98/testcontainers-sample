from dataclasses import dataclass

import review_app.database.models as models


@dataclass
class DatabaseItems:
    users: list[models.User]
    media_types: list[models.MediaType]
    authors: list[models.Author]
    media: list[models.Media]
    reviews: list[models.Review]

    def to_list(self):
        return self.users + self.media_types + self.authors + self.media + self.reviews
