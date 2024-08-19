import uuid

class Category:
    def __init__(self, name,id = "", description="", is_active=True) -> None:
        self.id = id or uuid.uuid4()
        self.name = name 
        self.desciption = description
        self.is_active = is_active

        if len(self.name) >255:
            raise ValueError("name must have less than 256 characteres")
    
    def __str__(self):
        return f"{self.name} - {self.desciption} ({self.is_active})"
    
    def __repr__(self) -> str:
        return f"Category {self.name} ({self.id})"
    
    def update_category(self, name, description):
        self.name = name 
        self.description = description 

        if len(self.name) >255:
            raise ValueError("name must have less than 256 characteres")