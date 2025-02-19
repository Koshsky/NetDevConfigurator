import json
import logging

from .exceptions import EntityNotFoundError

logger = logging.getLogger("db")


class BaseService:
    def __init__(self, db, model):
        self.db = db
        self.model = model

    def get_all(self, **args):
        entities = self.db.query(self.model)

        for key, value in args.items():
            column = getattr(self.model, key)
            if isinstance(value, list):
                entities = entities.filter(column.in_(value))
            else:
                entities = entities.filter(column == value)
        entities = entities.all()
        logger.info(
            "Found %d %s entities with filters: %s",
            len(entities),
            self.model.__name__,
            json.dumps(args),
        )
        return entities

    def get_one(self, **args):
        if not args:
            logger.error("No arguments provided for query.")
            raise ValueError("At least one argument must be provided.")

        entities = self.db.query(self.model).filter_by(**args).all()
        entity_count = len(entities)

        if entity_count == 1:
            logger.debug(
                "Successfully retrieved %s entity matching criteria: %s",
                self.model.__name__,
                json.dumps(args),
            )
            return entities[0]
        elif entity_count == 0:
            logger.error("%s with %s not found", self.model.__name__, json.dumps(args))
            raise EntityNotFoundError(
                f"{self.model.__name__} with {json.dumps(args)} not found"
            )
        else:  # entity_count > 1
            logger.error(
                "Multiple %s entities FOUND with %s",
                self.model.__name__,
                json.dumps(args),
            )
            raise EntityNotFoundError(
                f"Multiple {self.model.__name__} entities found with {json.dumps(args)}"
            )

    def get_info(self, entity):
        raise NotImplementedError()

    def get_info_one(self, **args):
        entity = self.get_one(**args)
        return self.get_info(entity)

    def get_info_all(self, **args):
        entities = self.get_all(**args)
        return [self.get_info(entity) for entity in entities]

    def create(self, data: dict):
        try:
            entity = self.model(**data)
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            logger.info("Created %s successfully: %s", self.model.__name__, data)
            return entity
        except Exception as e:
            logger.error("Failed to create %s: %s", self.model.__name__, str(e))
            self.db.rollback()
            raise

    def update(self, entity, updated_data: dict):
        for key, value in updated_data.items():
            setattr(entity, key, value)
        self.db.commit()
        self.db.refresh(entity)
        logger.info(
            "Updated %s entities successfully: %s", self.model.__name__, updated_data
        )
        return entity

    def delete_one(self, **args):
        entity = self.get_one(**args)
        self.delete(entity)

    def delete(self, entity):
        if entity:
            self.db.delete(entity)
            self.db.commit()
            logger.info(
                "%s with id %d deleted successfully", self.model.__name__, entity.id
            )
