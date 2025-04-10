from typing import TypeVar

from pydantic import BaseModel as PydanticModel

from src.database import BaseModel as DBModel

DBModelType = TypeVar("DBModelType", bound=DBModel)
SchemaType = TypeVar("SchemaType", bound=PydanticModel)


class DataMapper:
    db_model: type[DBModelType] = None 
    schema: type[SchemaType] = None 

    @classmethod
    def map_to_domain_entity(cls, db_model):
        """SQLalchymy model to Pydantic schema"""

        return cls.schema.model_validate(db_model, from_attributes=True)
    @classmethod
    def map_to_persistance_entity(cls, schema):
        """Pydantic schema to SQLalchemy model"""

        return cls.db_model(**schema.model_dump())