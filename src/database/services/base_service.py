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
            raise EntityNotFoundError(
                f"{self.model.__name__} with id {entity_id} not found"
            )

    def get_by_name(self, entity_name: str):
        entities = (
            self.db.query(self.model).filter(self.model.name == entity_name).all()
        )
        if len(entities) == 1:
            return entities[0]
        elif len(entities) == 0:
            raise EntityNotFoundError(
                f"{self.model.__name__} with name {entity_name} not found"
            )
        else:
            raise EntityNotFoundError(
                f"Multiple {self.model.__name__} entities found with name {entity_name}"
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
        logger.info(f"create {self.model.__name__} successfully: {data}")
        return entity

    def update(self, entity, updated_data: dict):
        for key, value in updated_data.items():
            setattr(entity, key, value)
        self.db.commit()
        self.db.refresh(entity)
        logger.info(
            f"Updated {self.model.__name__} entities successfully: {updated_data}"
        )
        return entity

    def delete(self, entity):
        if entity:
            self.db.delete(entity)
            self.db.commit()

    def delete_by_name(self, name: str):
        if db_entity := self.get_by_name(name):
            self.delete(db_entity)

    def delete_by_id(self, entity_id: int):
        if db_entity := self.get_by_id(entity_id):
            self.delete(db_entity)
