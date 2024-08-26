from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user_account'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    age: Mapped[Optional[int]] = mapped_column()

    reviews: Mapped[List['Review']] = relationship(back_populates='user')

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, name={self.name!r}, age={self.age!r})'


class MediaType(Base):
    __tablename__ = 'media_type'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f'MediaType(id={self.id!r}, name={self.name!r})'


class Author(Base):
    __tablename__ = 'author'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    alive: Mapped[bool] = mapped_column()

    works: Mapped[List['Media']] = relationship(back_populates='author')

    def __repr__(self) -> str:
        return f'Author(id={self.id!r}, name={self.name!r}, alive={self.alive!r})'


class Media(Base):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    media_type_id: Mapped[int] = mapped_column(ForeignKey('media_type.id'))
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey('author.id'))

    media_type: Mapped['MediaType'] = relationship()
    author: Mapped[Optional['Author']] = relationship(back_populates='works')
    reviews: Mapped[List['Review']] = relationship(back_populates='media')

    def __repr__(self) -> str:
        return (
            f'Media(id={self.id!r}, title={self.title!r},'
            f'media_type={self.media_type!r}, author={self.author!r})'
        )


class Review(Base):
    __tablename__ = 'review'
    id: Mapped[int] = mapped_column(primary_key=True)
    media_id: Mapped[int] = mapped_column(ForeignKey('media.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user_account.id'))
    rating: Mapped[int] = mapped_column()
    review: Mapped[str] = mapped_column()

    media: Mapped['Media'] = relationship(back_populates='reviews')
    user: Mapped['User'] = relationship(back_populates='reviews')

    def __repr__(self) -> str:
        return (
            f'Review(id={self.id!r}, media={self.media!r}, '
            f'user={self.user!r}, rating={self.rating!r}, review={self.review!r})'
        )
