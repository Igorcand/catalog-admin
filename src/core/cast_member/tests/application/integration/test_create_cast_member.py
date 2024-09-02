from uuid import UUID
from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMember,
    CreateCastMemberRequest,
)
import pytest
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMember



class TestCreateCastMember:
    def test_create_cast_member_with_valid_data(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)
        request = CreateCastMemberRequest(
            name="John Krasinski",
            type=CastMemberType.DIRECTOR,
        )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response.id, UUID)
        assert len(repository.cast_members) == 1

        persisted_cast_member = repository.cast_members[0]
        assert persisted_cast_member.id == response.id
        assert persisted_cast_member.name == "John Krasinski"
        assert persisted_cast_member.type == CastMemberType.DIRECTOR

    def test_create_inactive_cast_member_with_valid_data(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)
        use_case = CreateCastMember(repository=repository)
        with pytest.raises(InvalidCastMember, match="name cannot be empty") as exc_info:
            use_case.execute(CreateCastMemberRequest(name="", type=""))

        assert exc_info.type is InvalidCastMember
        assert str(exc_info.value) == "name cannot be empty"