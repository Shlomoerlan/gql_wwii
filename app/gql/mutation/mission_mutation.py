from graphene import Mutation, Int, Field, Date
from returns.result import Success
from sqlalchemy import String

from app.gql.types import MissionType
from app.repository.mission_repository import add_mission, update_mission_attack_result, update_attack_result, \
    delete_mission


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
    message = String()

    @staticmethod
    def mutate(root, info, mission_date, airborne_aircraft, attacking_aircraft, bombing_aircraft,
               aircraft_returned, aircraft_failed, aircraft_damaged, aircraft_lost):
        new_mission = add_mission(
            mission_date, airborne_aircraft, attacking_aircraft,
            bombing_aircraft, aircraft_returned, aircraft_failed,
            aircraft_damaged, aircraft_lost
        )
        if isinstance(new_mission, Success):
            return AddMission(mission=new_mission.unwrap(), message='success')
        return AddMission(mission=None,message=new_mission.failure())



class UpdateMissionAttackResult(Mutation):
    class Arguments:
        mission_id = Int(required=True)
        returned_aircraft = Int(required=True)
        failed_aircraft = Int(required=True)
        lost_aircraft = Int(required=True)

    mission = Field(lambda: MissionType)
    message = String()

    @staticmethod
    def mutate(root, info, mission_id, returned_aircraft, failed_aircraft, damaged_aircraft, lost_aircraft):
        updated_mission = update_mission_attack_result(
            mission_id, returned_aircraft, failed_aircraft,
            damaged_aircraft, lost_aircraft
        )
        if isinstance(updated_mission, Success):
            return UpdateMissionAttackResult(mission=updated_mission, message='success')
        return UpdateAttackResult(mission=None,message=updated_mission.failure())


class UpdateAttackResult(Mutation):
    class Arguments:
        mission_id = Int(required=True)
        returned_aircraft = Int(required=True)
        failed_aircraft = Int(required=True)
        damaged_aircraft = Int(required=True)
        lost_aircraft = Int(required=True)

    mission = Field(lambda: MissionType)
    message = String()

    @staticmethod
    def mutate(root, info, mission_id, returned_aircraft, failed_aircraft, damaged_aircraft, lost_aircraft):
        updated_mission = update_attack_result(
            mission_id, returned_aircraft, failed_aircraft,
            damaged_aircraft, lost_aircraft
        )
        if isinstance(updated_mission, Success):
            return UpdateAttackResult(mission=updated_mission, message='success')
        return UpdateAttackResult(mission=None,message=updated_mission.failure())


class DeleteMission(Mutation):
    class Arguments:
        mission_id = Int(required=True)

    mission = Field(lambda: MissionType)
    message = String()

    @staticmethod
    def mutate(root, info, mission_id):
        result = delete_mission(mission_id)
        if isinstance(result, Success):
            return DeleteMission(mission=result.unwrap(), message='success')

        return DeleteMission(mission=None, message=result.unwrap())
