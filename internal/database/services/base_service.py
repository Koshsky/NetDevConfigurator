from .exceptions import EntityNotFoundError

class BaseService:
    def __init__(self, db, model):
        self.db = db
        self.model = model

    def get_all(self):
        return self.db.query(self.model).all()

    def get_by_id(self, entity_id: int):
        if entity := self.db.query(self.model).filter(self.model.id == entity_id).first():
            return entity
        else:
            raise EntityNotFoundError(f"{self.model.__name__} with id {entity_id} not found")

    def get_by_name(self, entity_name: str):  # TODO: get_all_by_name!
        if entity:= self.db.query(self.model).filter(self.model.name == entity_name).first():
            return entity
        else:
            raise EntityNotFoundError(f"{self.model.__name__} with name {entity_name} not found")

    def get_info(self, entity):
        raise NotImplementedError()

    def get_info_by_name(self, entity_name: str):
        entity = self.get_by_name(entity_name)
        return self.get_info(entity)

    def get_info_by_id(self, entity_id: int):
        entity = self.get_by_id(entity_id)
        return self.get_info(entity)

    def create(self, entity: dict):
        entity = self.model(**entity)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def __delete(self, entity):
        if entity:
            self.db.delete(entity)
            self.db.commit()

    def delete_by_name(self, name: str):
        if db_entity := self.get_by_name(name):
            self.__delete(db_entity)

    def delete_by_id(self, entity_id: int):
        if db_entity := self.get_by_id(entity_id):
            self.__delete(db_entity)

