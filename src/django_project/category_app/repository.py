from uuid import UUID
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.django_project.category_app.models import Category as CategoryORM

class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, model: CategoryORM | None = None) -> None:
        self.model = model or CategoryORM
    
    def save(self, category: Category) -> None:
        category_orm = CategoryModelMapper.to_model(category)
        category_orm.save()
    
    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category = self.model.objects.get(id=id)
            return CategoryModelMapper.to_entity(category)
        except self.model.DoesNotExist:
            return None
        
    def delete(self, id: UUID) -> None:
        return self.model.objects.filter(id=id).delete()
    
    def list(self) -> list[Category]:
        return [
            CategoryModelMapper.to_entity(category_model)
            for category_model in self.model.objects.all()]

    def update(self, category: Category) -> None:
        self.model.objects.filter(pk=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

class CategoryModelMapper:
    @staticmethod
    def to_model(category: Category) -> CategoryORM:
        return CategoryORM(
            id=category.id,
            name=category.name,
            description = category.description,
            is_active=category.is_active
        )
    
    def to_entity(category: CategoryORM) -> Category:
        return Category(
            id=category.id,
            name=category.name,
            description = category.description,
            is_active=category.is_active
        )