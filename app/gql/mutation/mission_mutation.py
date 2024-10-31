from graphene import Mutation, Int, Field, Date
from app.gql.types import MissionType
from app.models import Mission
from app.repository.mission_repository import add_mission, update_mission_attack_result


class AddMission(Mutation):
    class Arguments:
        mission_date = Date(required=True)
        airborne_aircraft = Int(required=True)
        attacking_aircraft = Int(required=True)
        bombing_aircraft = Int(required=True)
        aircraft_returned = Int(required=True)
        aircraft_failed = Int(required=True)
        aircraft_damaged = Int(required=True)
        aircraft_lost = Int(required=True)

    mission = Field(lambda: MissionType)

    @staticmethod
    def mutate(root, info, mission_date, airborne_aircraft, attacking_aircraft, bombing_aircraft,
               aircraft_returned, aircraft_failed, aircraft_damaged, aircraft_lost):
        new_mission = Mission(
            mission_date=mission_date,
            airborne_aircraft=airborne_aircraft,
            attacking_aircraft=attacking_aircraft,
            bombing_aircraft=bombing_aircraft,
            aircraft_returned=aircraft_returned,
            aircraft_failed=aircraft_failed,
            aircraft_damaged=aircraft_damaged,
            aircraft_lost=aircraft_lost
        )
        add_mission(new_mission)
        return AddMission(mission=new_mission)


class UpdateMissionAttackResult(Mutation):
    class Arguments:
        mission_id = Int(required=True)
        returned_aircraft = Int(required=True)
        failed_aircraft = Int(required=True)
        damaged_aircraft = Int(required=True)
        lost_aircraft = Int(required=True)
        damage_assessment = Int(required=True)

    mission = Field(lambda: MissionType)

    @staticmethod
    def mutate(root, info, mission_id, returned_aircraft, failed_aircraft, damaged_aircraft, lost_aircraft, damage_assessment):
        updated_mission = update_mission_attack_result(mission_id, returned_aircraft, failed_aircraft, damaged_aircraft, lost_aircraft, damage_assessment)
        return UpdateMissionAttackResult(mission=updated_mission)

