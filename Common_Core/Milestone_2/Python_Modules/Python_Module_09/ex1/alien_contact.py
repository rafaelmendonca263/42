
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import Optional
import enum
from pydantic import ValidationError


class ContactType(enum.Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    SIGNAL = "signal"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"
    RADIO = "radio"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType = Field(...)
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def check_cross_data(self):
        if not self.contact_id.startswith("AC"):
            raise ValueError("contact_id must start with 'AC'")

        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contacts must be verified")

        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError("Telepathic contact requires"
                             " at least 3 witnesses")

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals must have a message received")
        return self


if __name__ == "__main__":
    print("Alien Contact Log Validation")
    print("======================================")

    # ✔ Caso válido
    try:
        contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2026, 4, 10, 14, 30),
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="'Greetings from Zeta Reticuli'",
            is_verified=True
        )

        print("Valid contact report:")
        print("ID:", contact.contact_id)
        print("Type:", contact.contact_type.value)
        print("Location:", contact.location)
        print(f"Signal: {contact.signal_strength}/10")
        print(f"Duration: {contact.duration_minutes} minutes")
        print(f"Witnesses: {contact.witness_count}")
        print(f"Message: {contact.message_received}")

    except ValidationError as e:
        print("Expected validation error:")
        msg = e.errors()[0]["msg"]

        if "Value error, " in msg:
            msg = msg.replace("Value error, ", "")

        print(msg)

    print("\n======================================")

    # ❌ Caso inválido (telepathic com poucas testemunhas)
    try:
        invalid_contact = AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime(2026, 4, 10, 14, 30),
            location="Unknown Sector",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=5.0,
            duration_minutes=30,
            witness_count=1,  # ERRO AQUI
            message_received="We come in peace",
            is_verified=False
        )

    except ValidationError as e:
        print("Expected validation error:")
        msg = e.errors()[0]["msg"]

        if "Value error, " in msg:
            msg = msg.replace("Value error, ", "")

        print(msg)
