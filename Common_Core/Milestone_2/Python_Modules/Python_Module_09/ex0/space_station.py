
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


if __name__ == "__main__":

    print("Space Station Data Validation")
    print("========================================")

    # ✅ VALID CASE
    try:
        station = SpaceStation(
            station_id="ISS01",
            name="International Station",
            crew_size=6,
            power_level=87.5,
            oxygen_level=92.0,
            last_maintenance=datetime(2026, 4, 10, 14, 30),
            is_operational=True,
            notes="All systems nominal"
        )

        print("Valid station created:")
        print("ID:", station.station_id)
        print("Name:", station.name)
        print("Crew:", f"{station.crew_size} people")
        print("Power:", f"{station.power_level}%")
        print("Oxygen:", f"{station.oxygen_level}%")
        print("Status:", "Operational")

    except ValidationError as e:
        print(e.errors()[0]["msg"])

    print("\n========================================")
    print("Expected validation error:")

    # ❌ INVALID CASE
    try:
        SpaceStation(
            station_id="S1",
            name="",
            crew_size=0,
            power_level=150.0,
            oxygen_level=-10.0,
            last_maintenance="2026-04-10T14:30:00"
        )

    except ValidationError as e:
        print(e.errors()[0]["msg"])
