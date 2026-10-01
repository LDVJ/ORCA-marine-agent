from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, func
from ..db import Base

class CachedCondition(Base):
    __tablename__ = "cached_conditions"

    id : Mapped[str] = mapped_column(primary_key=True)
    latitude : Mapped[float] = mapped_column(Float)
    longitude : Mapped[float] = mapped_column(Float)
    source : Mapped[str] = mapped_column(String)
    date : Mapped[str] = mapped_column(String)
    fetched_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())