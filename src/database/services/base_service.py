import json
import logging
from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)
JsonType = Union[List["JsonType"], Dict[str, "JsonType"]]


class EntityNotFoundError(Exception):
    """Raised when an entity is not found in the database."""

    pass


class BaseService(Generic[ModelType]):
    """Base service for database operations."""

    def __init__(self, db: Session, model: Type[ModelType]) -> None:
        """Initializes the BaseService with a database session and model.

        Args:
            db: The SQLAlchemy database session.
            model: The SQLAlchemy model class.
        """
        self.db = db
        self.model = model

    def get_all(self, **kwargs: Any) -> List[ModelType]:
        """Retrieves all entities of the model, optionally filtered by kwargs.

        Args:
            **kwargs: Keyword arguments representing filter criteria.

        Returns:
            A list of model entities.
        """
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

    def get_one(self, **kwargs: Any) -> ModelType:
        """Retrieves a single entity based on filter criteria.

        Args:
            **kwargs: Keyword arguments representing filter criteria.

        Returns:
            A single model entity.

        Raises:
            ValueError: If no arguments are provided.
            EntityNotFoundError: If no or multiple entities are found.
        """
        if not kwargs:
            logger.error("No arguments provided for query.")
            raise ValueError("At least one argument must be provided.")

        entities = self.get_all(**kwargs)
        entity_count = len(entities)

        if entity_count == 1:
            logger.debug("Found one %s entity: %s", self.model.__name__, kwargs)
            return entities[0]
        elif entity_count == 0:
            logger.warning(
                "%s with %s not found", self.model.__name__, json.dumps(kwargs)
            )
            raise EntityNotFoundError(
                f"{self.model.__name__} with {json.dumps(kwargs)} not found"
            )
        else:  # entity_count > 1
            logger.warning(
                "Multiple %s entities found with %s",
                self.model.__name__,
                json.dumps(kwargs),
            )
            raise EntityNotFoundError(
                f"Multiple {self.model.__name__} entities found with {json.dumps(kwargs)}"
            )

    def get_info(self, entity: ModelType) -> JsonType:
        """Retrieves information about a specific entity.

        Args:
            entity: The model entity.

        Returns:
            A JSON representation of the entity's information.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError()

    def get_info_one(self, **kwargs: Any) -> JsonType:
        """Retrieves information about a single entity based on filter criteria.

        Args:
            **kwargs: Keyword arguments representing filter criteria.

        Returns:
            A JSON representation of the entity's information.
        """
        entity = self.get_one(**kwargs)
        return self.get_info(entity)

    def get_info_all(self, **kwargs: Any) -> List[JsonType]:
        """Retrieves information about all entities, optionally filtered by kwargs.

        Args:
            **kwargs: Keyword arguments representing filter criteria.

        Returns:
            A list of JSON representations of the entities' information.
        """
        entities = self.get_all(**kwargs)
        return [self.get_info(entity) for entity in entities]

    def create(self, **kwargs: Any) -> ModelType:
        """Creates a new entity.

        Args:
            **kwargs: Keyword arguments representing the entity's attributes.

        Returns:
            The newly created entity.

        Raises:
            SQLAlchemyError: If an error occurs during database operations.
        """
        try:
            entity = self.model(**kwargs)
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            logger.debug("Created %s successfully: %s", self.model.__name__, kwargs)
            return entity
        except SQLAlchemyError as e:
            logger.error("Failed to create %s: %s", self.model.__name__, str(e))
            self.db.rollback()
            raise

    def update(self, entity: ModelType, **updated_data: Any) -> ModelType:
        """Updates an existing entity.

        Args:
            entity: The entity to update.
            **updated_data: Keyword arguments representing the updated attributes.

        Returns:
            The updated entity.
        """
        for key, value in updated_data.items():
            setattr(entity, key, value)
        self.db.commit()
        self.db.refresh(entity)
        logger.debug("Updated %s successfully: %s", self.model.__name__, updated_data)
        return entity

    def delete_one(self, **kwargs: Any) -> None:
        """Deletes a single entity based on filter criteria.

        Args:
            **kwargs: Keyword arguments representing filter criteria.
        """
        entity = self.get_one(**kwargs)
        self.delete(entity)

    def delete(self, entity: ModelType) -> None:
        """Deletes an entity.

        Args:
            entity: The entity to delete.
        """
        if entity:
            self.db.delete(entity)
            self.db.commit()
            logger.debug(
                "%s with id %d deleted successfully", self.model.__name__, entity.id
            )
