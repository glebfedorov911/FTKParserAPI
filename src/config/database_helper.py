from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker,
)

from src.config.settings import settings


class DatabaseHelper:
    AUTOFLUSH = False
    AUTOCOMMIT = False
    EXPIRE_ON_COMMIT = False


    def __init__(
            self,
            url: str,
            echo: bool = False
    ) -> None:
        self.url = url
        self.echo = echo

        self.engine = create_async_engine(
            url=self.url,
            echo=self.echo
        )

        self.session_maker = async_sessionmaker(
            bind=self.engine,
            autoflush=self.AUTOFLUSH,
            autocommit=self.AUTOCOMMIT,
            expire_on_commit=self.EXPIRE_ON_COMMIT
        )

    async def session_depends(self) -> AsyncSession:
        """Method for get session for work with db"""
        async with self.session_maker() as session:
            yield session

database_helper = DatabaseHelper(
    url=settings.database_settings.db_url,
    echo=settings.database_settings.echo
)