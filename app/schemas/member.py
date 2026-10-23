"""Member request/response schemas."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.member import MembershipType

Name = Annotated[str, Field(min_length=1, max_length=100)]
Phone = Annotated[str, Field(pattern=r"^\+?[0-9\- ]{7,20}$")]


class MemberCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "name": "Ravi Kumar",
                "email": "ravi.kumar@example.com",
                "phone": "+91 98765 43210",
                "membership_type": "standard",
            }
        },
    )

    name: Name
    email: EmailStr
    phone: Phone | None = None
    membership_type: MembershipType = MembershipType.STANDARD


class MemberUpdate(BaseModel):
    """Partial update: only fields that are sent are changed."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={"example": {"membership_type": "premium", "is_active": True}},
    )

    name: Name | None = None
    email: EmailStr | None = None
    phone: Phone | None = None
    membership_type: MembershipType | None = None
    is_active: bool | None = None


class MemberRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: str | None
    membership_type: MembershipType
    is_active: bool
    created_at: datetime
    updated_at: datetime
