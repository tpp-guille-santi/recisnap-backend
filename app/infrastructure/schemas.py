from pydantic import BaseModel


class ImagesCountResponse(BaseModel):
    count: int
