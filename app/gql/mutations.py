from graphene import ObjectType

from app.gql.mutation.mission_mutation import AddMission, UpdateMissionAttackResult, UpdateAttackResult, DeleteMission
from app.gql.mutation.target_mutation import AddTarget


class Mutation(ObjectType):
    add_mission = AddMission.Field()
    add_target = AddTarget.Field()
    update_mission_attack_result = UpdateMissionAttackResult.Field()
    update_attack_result = UpdateAttackResult.Field()
    delete_mission = DeleteMission.Field()