from sqlalchemy.orm import (
    DeclarativeBase, declared_attr, mapped_column, Mapped
)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Automatically create name for table by class name"""
        return f"{cls.__name__.lower()}s"
    
    def to_dict(self) -> dict:
        """Method help to create dict from Base-record"""
        {   
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)