

class BaseService:
    def __init__(self, db, model):
        self.db = db
        self.model = model

    def get_all(self):
        return self.db.query(self.model).all()

    def get_by_id(self, entity_id: int):
        return self.db.query(self.model).filter(self.model.id == entity_id).first()
        
    def get_by_name(self, name: str):
        return self.db.query(self.model).filter(self.model.name == name).first()

    def get_info(self, entity):
        raise NotImplementedError()
    
    def get_info_by_name(self, name: str):
        entity = self.get_by_name(name)
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
    
    def delete(self, entity):
        if entity:
            self.db.delete(entity)
            self.db.commit()

    def delete_by_name(self, name: str):
        db_entity = self.get_by_name(name)
        self.delete(db_entity)

    def delete_by_id(self, company_id: int):
        db_entity = self.get_by_id(company_id)
        self.delete(db_entity)
