import logging

from .exceptions import EntityNotFoundError

logger = logging.getLogger("db")


class BaseService:
    def __init__(self, db, model):
        self.db = db
        self.model = model

    def get_all(self):
        return self.db.query(self.model).all()

    def get_by_id(self, entity_id: int):
        if (
            entity := self.db.query(self.model)
            .filter(self.model.id == entity_id)
            .first()
        ):
            return entity
        else:
            logger.error(
                "%s with id %d not found",
                self.model.__name__,
                entity_id,
            )
            raise EntityNotFoundError(f"%s with id {entity_id} not found")

    def get_by_name(self, entity_name: str):
        entities = (
            self.db.query(self.model).filter(self.model.name == entity_name).all()
        )
        logger.debug(
            "There %s %d entities found in %s table with name=%s",
            "are" if len(entities) > 1 else "is",
            len(entities),
            self.model.__name__,
            entity_name,
        )
        if len(entities) == 1:
            return entities[0]
        elif len(entities) == 0:
            logger.error("%s with name %s not found", self.model.__name__, entity_name)
            raise EntityNotFoundError(
                "%s with name %s not found", self.model.__name__, entity_name
            )
        else:
            logger.error(
                "Multiple %s entities found with name %s",
                self.model.__name__,
                entity_name,
            )
            raise EntityNotFoundError(
                "Multiple %s entities found with name %s",
                self.model.__name__,
                entity_name,
            )

    def get_info(self, entity):
        raise NotImplementedError()

    def get_info_by_name(self, entity_name: str):
        entity = self.get_by_name(entity_name)
        return self.get_info(entity)

    def get_info_by_id(self, entity_id: int):
        entity = self.get_by_id(entity_id)
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

    def delete_by_name(self, name: str):
        if db_entity := self.get_by_name(name):
            self.delete(db_entity)

    def delete_by_id(self, entity_id: int):
        if db_entity := self.get_by_id(entity_id):
            self.delete(db_entity)
