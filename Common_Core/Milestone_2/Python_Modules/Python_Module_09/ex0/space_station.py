import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError  # type: ignore


class SpaceStation(BaseModel):  # type: ignore[misc]
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime.datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("======================================")

    try:
        valid_station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.datetime.now(),
            is_operational=True,
            notes="All systems nominal.",
        )
        print("Valid station created:")
        print(f"ID: {valid_station.station_id}")
        print(f"Name: {valid_station.name}")
        print(f"Crew: {valid_station.crew_size} people")
        print(f"Power: {valid_station.power_level}%")
        print(f"Oxygen: {valid_station.oxygen_level}%")
        status = "Operational" if valid_station.is_operational else "Inactive"
        print(f"Status: {status}")
    except ValidationError as e:
        print(f"Unexpected validation error for valid data: {e}")

    print("======================================")

    try:
        print("Attempting to create invalid station (crew_size = 25)...")
        SpaceStation(
            station_id="MIR002",
            name="Mir Legacy Station",
            crew_size=25,
            power_level=45.0,
            oxygen_level=98.0,
            last_maintenance=datetime.datetime.fromisoformat(
                "2026-05-20T12:00:00"
            ),
            is_operational=True,
        )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(f"Field '{error['loc'][0]}': {error['msg']}")


if __name__ == "__main__":
    main()
