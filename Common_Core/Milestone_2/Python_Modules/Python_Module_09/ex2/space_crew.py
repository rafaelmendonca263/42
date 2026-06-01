import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field  # type: ignore
from pydantic import ValidationError, model_validator  # type: ignore


class Rank(str, Enum):

    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):  # type: ignore[misc]

    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):  # type: ignore[misc]
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime.datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")  # type: ignore[misc]
    def validate_mission_safety(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_leadership = any(
            member.rank in (Rank.CAPTAIN, Rank.COMMANDER)
            for member in self.crew
        )
        if not has_leadership:
            raise ValueError(
                "Mission must have at least " "one Commander or Captain"
            )

        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        if self.duration_days > 365:
            exp_crew = [
                member for member in self.crew if member.years_experience >= 5
            ]
            if len(exp_crew) / len(self.crew) < 0.5:
                raise ValueError(
                    "Long missions (> 365 days) need 50% "
                    "experienced crew (5+ years)"
                )

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")

    commander_member = CrewMember(
        member_id="C01",
        name="Sarah Connor",
        rank=Rank.COMMANDER,
        age=45,
        specialization="Mission Command",
        years_experience=15,
    )
    lieutenant_member = CrewMember(
        member_id="L02",
        name="John Smith",
        rank=Rank.LIEUTENANT,
        age=32,
        specialization="Navigation",
        years_experience=6,
    )
    officer_member = CrewMember(
        member_id="O03",
        name="Alice Johnson",
        rank=Rank.OFFICER,
        age=28,
        specialization="Engineering",
        years_experience=2,
    )

    try:
        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.datetime.now(),
            duration_days=900,
            crew=[commander_member, lieutenant_member, officer_member],
            budget_millions=2500.0,
        )
        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_millions}M")
        print(f"Crew size: {len(valid_mission.crew)}")
        print("Crew members:")
        for m in valid_mission.crew:
            print(f" - {m.name} ({m.rank.value}) - {m.specialization}")
    except ValidationError as e:
        print(f"Unexpected error: {e}")

    print("=========================================")

    try:
        print("Attempting to launch mission without a Captain or Commander...")
        SpaceMission(
            mission_id="M2026_MOON",
            mission_name="Lunar Base Logistics",
            destination="Moon",
            launch_date=datetime.datetime.now(),
            duration_days=30,
            crew=[lieutenant_member, officer_member],
            budget_millions=150.0,
        )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error["msg"])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
