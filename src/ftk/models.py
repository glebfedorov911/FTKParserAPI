from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY, JSON

from typing import List, Dict
from datetime import datetime

from src.config.base import Base


class FTK(Base):

    product_name: Mapped[str] = mapped_column()
    category: Mapped[str] = mapped_column()
    url_to_product: Mapped[str] = mapped_column() 
    icons: Mapped[List[str]] = mapped_column(ARRAY(String))
    characteristics: Mapped[Dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    actually: Mapped[bool] = mapped_column(default=True)