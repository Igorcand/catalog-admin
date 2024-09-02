from uuid import UUID
from dataclasses import dataclass
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from enum import StrEnum


class CastMemberFilterByType(StrEnum):
    NAME = "name"
    TYPE = "type"


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType

@dataclass
class ListCastMemberRequest:
    order_by : CastMemberFilterByType = ""


@dataclass
class ListCastMemberResponse:
    data: list[CastMemberOutput]


class ListCastMember:
    def __init__(self, repository: CastMemberRepository) -> None:
        self.repository = repository


    def execute(self, request: ListCastMemberRequest):
        cast_members = self.repository.list()
        data = [
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                )
                for cast_member in cast_members
            ]
        
        if request.order_by:
            if request.order_by and request.order_by in CastMemberOutput:
                mapped_genres = sorted(mapped_genres, key=lambda genre: getattr(genre, request.order_by))
        return ListCastMemberResponse(
            data=data
        )