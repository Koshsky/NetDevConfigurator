import json
import logging

from .exceptions import EntityNotFoundError

logger = logging.getLogger("db")


class BaseService:
    def __init__(self, db, model):
        self.db = db
        self.model = model

    def get_all(self):
        return self.db.query(self.model).all()

    def get_one(self, **args):
        if not args:
            logger.error("No arguments provided for query.")
            raise ValueError("At least one argument must be provided.")

        entities = self.db.query(self.model).filter_by(**args).all()
        entity_count = len(entities)

        if entity_count == 1:
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

    def get_info_by_name(self, entity_name: str):
        entity = self.get_one(name=entity_name)
        return self.get_info(entity)

    def get_info_by_id(self, entity_id: int):
        entity = self.get_one(id=entity_id)
        return self.get_info(entity)

    def create(self, data: dict):
        entity = self.model(**data)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        logger.info("create %s successfully: %s", self.model.__name__, data)
        return entity

    def update(self, entity, updated_data: dict):
        for key, value in updated_data.items():
            setattr(entity, key, value)
        self.db.commit()
        self.db.refresh(entity)
        logger.info(
            "Updated %s entities successfully: %s", self.model.__name__, updated_data
        )
        return entity

    def delete(self, entity):
        if entity:
            self.db.delete(entity)
            self.db.commit()
            logger.info(
                "%s with id %d deleted successfully", self.model.__name__, entity.id
            )

    def delete_by_name(self, entity_name: str):
        if db_entity := self.get_one(name=entity_name):
            self.delete(db_entity)

    def delete_by_id(self, entity_id: int):
        if db_entity := self.get_one(id=entity_id):
            self.delete(db_entity)
