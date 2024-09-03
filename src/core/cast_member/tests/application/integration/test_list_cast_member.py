from unittest.mock import create_autospec

import pytest
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.list_cast_member import (
    CastMemberOutput,
    ListCastMember,
    ListCastMemberRequest,
    ListCastMemberResponse,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository
from src.core._shered.pagination import ListOutputMeta


class TestListCastMember:
    @pytest.fixture
    def actor(self) -> CastMember:
        return CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

    @pytest.fixture
    def director(self) -> CastMember:
        return CastMember(
            name="John Krasinski",
            type=CastMemberType.DIRECTOR,
        )

    def test_when_no_cast_members_then_return_empty_list(
        self,
    ) -> None:
        use_case = ListCastMember(repository=InMemoryCastMemberRepository())
        response = use_case.execute(request=ListCastMemberRequest())

        assert response == ListCastMemberResponse(
            data=[],
            meta = ListOutputMeta(current_page=1, per_page=2, total=0)
            )

    def test_when_cast_members_exist_then_return_mapped_list(
        self,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        repository = InMemoryCastMemberRepository()
        repository.save(actor)
        repository.save(director)

        use_case = ListCastMember(repository=repository)
        response = use_case.execute(request=ListCastMemberRequest())

        assert response == ListCastMemberResponse(
            data=[
                CastMemberOutput(
                    id=actor.id,
                    name=actor.name,
                    type=actor.type,
                ),
                CastMemberOutput(
                    id=director.id,
                    name=director.name,
                    type=director.type,
                ),
            ],
            meta = ListOutputMeta(current_page=1, per_page=2, total=2)
        )