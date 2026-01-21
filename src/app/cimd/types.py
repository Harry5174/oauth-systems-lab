from pydantic import BaseModel, HttpUrl
from typing import List


class ClientMetadata(BaseModel):
    client_id: HttpUrl
    redirect_uris: List[HttpUrl]
    grant_types: List[str] = ["authorization_code"]
    response_types: List[str] = ["code"]
