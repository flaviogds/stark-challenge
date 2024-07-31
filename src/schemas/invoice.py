from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class FlexModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class Invoice(FlexModel):
    id: str | None = None
    tax_id: str | None = None
    name: str | None = None
    amount: int | None = None
    status: str | None = None
    descriptions: List[Optional[str]] | None = None
    due: Optional[datetime] | None = None
    fine: Optional[float] | None = None
    interest: Optional[float] | None = None
    expiration: Optional[int] | None = None
    descriptions: List[Optional[Dict[str, str]]] | None = None
    discounts: List[Optional[Dict[str, str]]] = None
    tags: List[Optional[str]] | None = None
    rules: List[Optional[Dict]] | None = None
    updated: Optional[datetime] | None = None


class Log(FlexModel):
    id: str | None = None
    created: datetime | None = None
    errors: List[Optional[Dict[str, str]]] | None = None
    type: str | None = None
    invoice: Invoice | None = None


class Event(FlexModel):
    id: str | None = None
    subscription: str | None = None
    workspaceId: str | None = None
    created: datetime | None = None
    log: Log | None = None


class RequestPayload(FlexModel):
    event: Event | None = None
