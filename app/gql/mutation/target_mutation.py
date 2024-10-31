from graphene import Mutation, Int, String, Field

from app.models import TargetType
from app.repository.target_repository import add_target


class AddTarget(Mutation):
    class Arguments:
        mission_id = Int(required=True)
        target_industry = String(required=True)
        city_id = Int(required=True)
        target_type_id = Int(required=True)
        target_priority = Int(required=True)

    target = Field(lambda: TargetType)

    @staticmethod
    def mutate(root, info, mission_id, target_industry, city_id, target_type_id, target_priority):
        new_target = add_target(mission_id, target_industry, city_id, target_type_id, target_priority)
        return AddTarget(target=new_target)
