from dataclasses import dataclass
from dataclasses_json import dataclass_json
from sqlalchemy import types, text, ForeignKey
from sqlalchemy import VARCHAR, TEXT
from sqlalchemy.orm import MappedAsDataclass, Mapped, relationship, DeclarativeBase
import uuid


from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    pass

@dataclass
@dataclass_json
class User(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key = True,
        server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(VARCHAR)
    email: Mapped[str] = mapped_column(VARCHAR)


@dataclass
@dataclass_json
class Post(Base):
    __tablename__ =  'post'

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    title: Mapped[str] = mapped_column(VARCHAR)
    content: Mapped[str] = mapped_column(TEXT)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
