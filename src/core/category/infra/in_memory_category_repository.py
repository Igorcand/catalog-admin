class InMemoryCategoryRepository:
    def __init__(self, categories=None) -> None:
        self.categories = categories or []
    
    def save(self, category):
        self.categories.append(category)