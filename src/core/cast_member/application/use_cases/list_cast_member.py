from uuid import UUID
from dataclasses import dataclass
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType

@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType

@dataclass
class ListCastMemberRequest:
    pass


@dataclass
class ListCastMemberResponse:
    data: list[CastMemberOutput]


class ListCastMember:
    def __init__(self, repository: CastMemberRepository) -> None:
        self.repository = repository


    def execute(self, request: ListCastMemberRequest):
        cast_members = self.repository.list()

        return ListCastMemberResponse(
            data=[
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                )
                for cast_member in cast_members
            ]
        )