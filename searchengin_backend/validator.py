from typing import List
from pydantic import (
    BaseModel,
    StrictInt,
)

# cette classe permet de faire la validation des données 
class AttributesSchema(BaseModel):
    idIndex : StrictInt
    idBook  : StrictInt
    words   : List
