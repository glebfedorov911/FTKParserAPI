from pydantic import BaseModel
from pydantic_settings import BaseSettings


class FTKParserConfig(BaseModel):
    image_path: str = "parsers/ftk_image/"

class ParserConfig(BaseSettings):
    ftk_parser_config: FTKParserConfig = FTKParserConfig()

config = ParserConfig()