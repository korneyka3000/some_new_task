from pydantic import BaseModel


class PhoneAddress(BaseModel):
    phone: str
    address: str
