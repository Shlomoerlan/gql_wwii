from graphene import ObjectType, List, Date, Field, Int, String

from app.gql.types import MissionType, AttackResultType
from app.repository.mission_repository import get_all_missions, get_missions_by_date_range, get_mission_by_id, \
    get_mission_by_country, get_mission_by_industry, get_mission_result_by_attack


class Query(ObjectType):
    missions = List(MissionType)
    missions_by_date_range = List(MissionType, start_date=Date(required=True), end_date=Date(required=True))
    mission_by_id = Field(MissionType, mission_id=Int(required=True))
    missions_by_country = List(MissionType, country_name=String(required=True))
    missions_by_industry = List(MissionType, industry=String(required=True))
    attack_results_by_type = List(AttackResultType, target_type_id=Int(required=True))


    @staticmethod
    def resolve_missions(root, info):
        return get_all_missions()
    @staticmethod
    def resolve_missions_by_date_range(root, info, start_date, end_date):
        return get_missions_by_date_range(start_date, end_date)

    @staticmethod
    def resolve_mission_by_id(root, info, mission_id):
        return get_mission_by_id(mission_id)

    @staticmethod
    def resolve_missions_by_country(root, info, country_name):
        return get_mission_by_country(country_name)

    @staticmethod
    def resolve_missions_by_industry(root, info, industry):
        return get_mission_by_industry(industry)

    @staticmethod
    def resolve_attack_results_by_type(root, info, target_type_id):
        return get_mission_result_by_attack(target_type_id)