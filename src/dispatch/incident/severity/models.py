from typing import List, Optional
from pydantic import Field
from pydantic.color import Color

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.event import listen
from sqlalchemy_utils import TSVectorType

from dispatch.database.core import Base, ensure_unique_default_per_project
from dispatch.models import DispatchBase, NameStr, ProjectMixin, PrimaryKey
from dispatch.project.models import ProjectRead


class IncidentSeverity(Base, ProjectMixin):
    __table_args__ = (UniqueConstraint("name", "project_id"),)
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    color = Column(String)
    enabled = Column(Boolean, default=True)
    default = Column(Boolean, default=False)

    # This column is used to control how severities should be displayed
    # Lower numbers will be shown first.
    view_order = Column(Integer, default=9999)

    search_vector = Column(
        TSVectorType(
            "name",
            "description",
            regconfig="pg_catalog.simple",
        )
    )


listen(IncidentSeverity.default, "set", ensure_unique_default_per_project)


# Pydantic models
class IncidentSeverityBase(DispatchBase):
    color: Optional[Color] = Field(None, nullable=True)
    default: Optional[bool]
    description: Optional[str] = Field(None, nullable=True)
    enabled: Optional[bool]
    name: NameStr
    project: Optional[ProjectRead]
    view_order: Optional[int]


class IncidentSeverityCreate(IncidentSeverityBase):
    pass


class IncidentSeverityUpdate(IncidentSeverityBase):
    pass


class IncidentSeverityRead(IncidentSeverityBase):
    id: PrimaryKey


class IncidentSeverityPagination(DispatchBase):
    total: int
    items: List[IncidentSeverityRead] = []
