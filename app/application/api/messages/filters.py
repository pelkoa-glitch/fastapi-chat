from infra.repositories.filters.messages import GetMessagesFilters as GetMessagesInfraFilters
from pydantic import BaseModel


class GetMessagesFilterss(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infra(self):
        return GetMessagesInfraFilters(limit=self.limit, offset=self.offset)
