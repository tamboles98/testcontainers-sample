from dataclasses import dataclass, field
from enum import UNIQUE, Enum, verify

import review_app.database.models as models


@dataclass
class DatabaseItems:
    users: list[models.User] = field(default_factory=list)
    media_types: list[models.MediaType] = field(default_factory=list)
    authors: list[models.Author] = field(default_factory=list)
    media: list[models.Media] = field(default_factory=list)
    reviews: list[models.Review] = field(default_factory=list)

    def to_list(self):
        return self.users + self.media_types + self.authors + self.media + self.reviews


def _empty_initialization() -> DatabaseItems:
    return DatabaseItems(users=[], media_types=[], authors=[], media=[], reviews=[])


def _basic_initialization() -> DatabaseItems:
    user = models.User(name='John Doe', age=25)
    media_type = models.MediaType(name='Book')
    author = models.Author(name='Jane Smith', alive=True)
    media = models.Media(title='The Great Gatsby', media_type=media_type, author=author)
    review = models.Review(media=media, user=user, rating=5, review='Great book!')

    return DatabaseItems(
        users=[user],
        media_types=[media_type],
        authors=[author],
        media=[media],
        reviews=[review],
    )


def _noreview_initialization() -> DatabaseItems:
    user = models.User(name='John Doe', age=25)
    media_type = models.MediaType(name='Book')
    author = models.Author(name='Jane Smith', alive=True)
    media = models.Media(title='The Great Gatsby', media_type=media_type, author=author)

    return DatabaseItems(
        users=[user],
        media_types=[media_type],
        authors=[author],
        media=[media],
        reviews=[],
    )


def _nomedia_initialization() -> DatabaseItems:
    user = models.User(name='John Doe', age=25)
    media_type = models.MediaType(name='Book')
    author = models.Author(name='Jane Smith', alive=True)

    return DatabaseItems(
        users=[user],
        media_types=[media_type],
        authors=[author],
        media=[],
        reviews=[],
    )


def _rich_initialization() -> DatabaseItems:
    users = [models.User(name='John Doe', age=25), models.User(name='Maria Perez', age=30)]
    media_type = [
        models.MediaType(name='Book'),
        models.MediaType(name='Movie'),
        models.MediaType(name='Music'),
    ]
    authors = [
        models.Author(name='John Smith', alive=True),
        models.Author(name='J.R.R. Tolkien', alive=False),
    ]
    media = [
        models.Media(title='The Lord of the Rings', media_type=media_type[0], author=authors[1]),
        models.Media(title='The Silmarillion', media_type=media_type[0], author=authors[1]),
        models.Media(title='The Hobbit', media_type=media_type[0], author=authors[1]),
    ]
    reviews = [
        models.Review(media=media[0], user=users[0], rating=5, review='Good book!'),
        models.Review(media=media[0], user=users[1], rating=4, review='One of the classics!'),
        models.Review(media=media[1], user=users[0], rating=4, review='Great book!'),
        models.Review(media=media[1], user=users[1], rating=3, review='A bit dense, but good!'),
    ]
    return DatabaseItems(
        users=users, media_types=media_type, authors=authors, media=media, reviews=reviews
    )


# This is a pattern that just came up to me, It works great for this case,
# but I am not sure if it's idiomatic or if it's a good idea to use it.
@verify(UNIQUE)
class InitializationType(Enum):
    EMPTY = 'empty'
    BASIC = 'basic'
    NOREVIEW = 'noreview'
    NOMEDIA = 'nomedia'
    RICH = 'rich'

    def initialize(self) -> DatabaseItems:
        try:
            initialization_method = {
                InitializationType.EMPTY: _empty_initialization,
                InitializationType.BASIC: _basic_initialization,
                InitializationType.NOREVIEW: _noreview_initialization,
                InitializationType.NOMEDIA: _nomedia_initialization,
                InitializationType.RICH: _rich_initialization,
            }[self]
        except KeyError:
            raise NotImplementedError(f'Initialization method for {self} not implemented') from None
        return initialization_method()
