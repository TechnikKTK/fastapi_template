from sqlalchemy.orm import Mapped, mapped_column

from app.apps.models import BASE, BaseModelMixin


class Core(BASE, BaseModelMixin):
    __tablename__ = "core"

    id: Mapped[int] = mapped_column(primary_key=True)
