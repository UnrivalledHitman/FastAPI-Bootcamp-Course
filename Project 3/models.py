from database import base
from sqlalchemy.orm import Mapped, mapped_column


class Todos(base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    priority: Mapped[int] = mapped_column()
    complete: Mapped[bool] = mapped_column(default=False)
