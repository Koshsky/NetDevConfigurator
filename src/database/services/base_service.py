import json
import logging
from typing import Dict, List, Type, Union

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session

from .exceptions import EntityNotFoundError

logger = logging.getLogger("db")


JsonType = Union[
    List["JsonType"],
    Dict[str, "JsonType"],
]
Model = Type[DeclarativeMeta]


class BaseService:
    def __init__(self, db: Session, model: Model) -> None:
        self.db = db
        self.model = model

    def get_all(self, **kwargs) -> List[Model]:
        entities = self.db.query(self.model)

        for key, value in kwargs.items():
            column = getattr(self.model, key)
            if isinstance(value, list):
                entities = entities.filter(column.in_(value))
            else:
                entities = entities.filter(column == value)
        entities = entities.all()
        logger.debug(
            "Found %d %s entities with filters: %s",
            len(entities),
            self.model.__name__,
            json.dumps(kwargs),
        )
        return entities

    def get_one(self, **kwargs) -> Model:
        if not kwargs:
            logger.error("No arguments provided for query.")
            raise ValueError("At least one argument must be provided.")

        entities = self.get_all(**kwargs)
        entity_count = len(entities)

        if entity_count == 1:
            return entities[0]
        elif entity_count == 0:
            logger.error(
                "%s with %s not found", self.model.__name__, json.dumps(kwargs)
            )
            raise EntityNotFoundError(
                f"{self.model.__name__} with {json.dumps(kwargs)} not found"
            )
        else:  # entity_count > 1
            logger.error(
                "Multiple %s entities FOUND with %s",
                self.model.__name__,
                json.dumps(kwargs),
            )
            raise EntityNotFoundError(
                f"Multiple {self.model.__name__} entities found with {json.dumps(kwargs)}"
            )

    def get_info(self, entity: Model) -> JsonType:
        raise NotImplementedError()

    def get_info_one(self, **kwargs) -> JsonType:
        entity = self.get_one(**kwargs)
        return self.get_info(entity)

    def get_info_all(self, **kwargs) -> List[JsonType]:
        entities = self.get_all(**kwargs)
        return [self.get_info(entity) for entity in entities]

    def create(self, **kwargs) -> Model:
        try:
            entity = self.model(**kwargs)
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            logger.debug("Created %s successfully: %s", self.model.__name__, kwargs)
            return entity
        except Exception as e:
            logger.error("Failed to create %s: %s", self.model.__name__, str(e))
            self.db.rollback()
            raise

    def update(self, entity: Model, **updated_data) -> Model:
        for key, value in updated_data.items():
            setattr(entity, key, value)
        self.db.commit()
        self.db.refresh(entity)
        logger.debug(
            "Updated %s entities successfully: %s", self.model.__name__, updated_data
        )
        return entity

    def delete_one(self, **kwargs) -> None:
        entity = self.get_one(**kwargs)
        self.delete(entity)

    def delete(self, entity: Model) -> None:
        if entity:
            self.db.delete(entity)
            self.db.commit()
            logger.debug(
                "%s with id %d deleted successfully", self.model.__name__, entity.id
            )
