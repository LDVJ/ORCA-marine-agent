from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, func, DateTime
from ..db import Base

class Query(Base):
    __tablename__ = "query"

    id : Mapped[str] = mapped_column(primary_key=True)
    user_query : Mapped[str] = mapped_column(String)
    latitude : Mapped[float] = mapped_column(Float, nullable=True)
    longitude : Mapped[float] = mapped_column(Float, nullable=True)
    response : Mapped[str] = mapped_column(String, nullable=True)
    created_at  : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

