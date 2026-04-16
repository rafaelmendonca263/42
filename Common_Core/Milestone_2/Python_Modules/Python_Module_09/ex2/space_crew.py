
import enum
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from pydantic import ValidationError


class Rank(enum.Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank = Field(...)
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_items=1, max_items=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def check_cross_data(self):
        if not self.mission_id.startswith("M"):
            raise ValueError("mission_id must start with 'M'")

        for member in self.crew:
            if member.rank == Rank.CAPTAIN:
                break
            elif member.rank == Rank.COMMANDER:
                break
            else:
                continue
        else:
            raise ValueError("Mission must have at least one Commander"
                             " or Captain")

        if self.duration_days > 365:
            experienced_people = 0
            for member in self.crew:
                if member.years_experience >= 5:
                    experienced_people += 1
            if experienced_people < len(self.crew) / 2:
                raise ValueError("Long missions require at least "
                                 "half of the crew to have 5+ years of"
                                 " experience")

        for member in self.crew:
            if not member.is_active:
                raise ValueError(f"Crew member {member.name} is not active")

        return self


if __name__ == "__main__":
    print("Space Mission Crew Validation")
    print("=========================================")

    # ✔ Caso válido
    try:
        mission = SpaceMission(
            mission_name="Mars Colony Establishment",
            mission_id="M2024_MARS",
            destination="Mars",
            launch_date=datetime(2026, 5, 1, 10, 0),
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="C001",
                    name="Sarah Connor",
                    rank=Rank.COMMANDER,
                    age=45,
                    specialization="Mission Command",
                    years_experience=15,
                    is_active=True
                ),
                CrewMember(
                    member_id="C002",
                    name="John Smith",
                    rank=Rank.LIEUTENANT,
                    age=34,
                    specialization="Navigation",
                    years_experience=8,
                    is_active=True
                ),
                CrewMember(
                    member_id="C003",
                    name="Alice Johnson",
                    rank=Rank.OFFICER,
                    age=29,
                    specialization="Engineering",
                    years_experience=6,
                    is_active=True
                ),
            ]
        )

        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")
        print("Crew members:")

        for member in mission.crew:
            print(
                f"- {member.name} ({member.rank.value}) - "
                f"{member.specialization}"
            )

    except ValidationError as e:
        print("Expected validation error:")
        msg = e.errors()[0]["msg"]
        if "Value error, " in msg:
            msg = msg.replace("Value error, ", "")
        print(msg)

    print("\n=========================================")

    # ❌ Caso inválido (sem commander/captain)
    try:
        invalid_mission = SpaceMission(
            mission_name="Failed Mission",
            mission_id="M2024_FAIL",
            destination="Mars",
            launch_date=datetime(2026, 5, 1, 10, 0),
            duration_days=100,
            budget_millions=500.0,
            crew=[
                CrewMember(
                    member_id="C004",
                    name="John Smith",
                    rank=Rank.LIEUTENANT,
                    age=34,
                    specialization="Navigation",
                    years_experience=4,
                    is_active=True
                ),
                CrewMember(
                    member_id="C005",
                    name="Alice Johnson",
                    rank=Rank.OFFICER,
                    age=29,
                    specialization="Engineering",
                    years_experience=3,
                    is_active=True
                ),
            ]
        )

    except ValidationError as e:
        print("Expected validation error:")
        msg = e.errors()[0]["msg"]
        if "Value error, " in msg:
            msg = msg.replace("Value error, ", "")
        print(msg)
