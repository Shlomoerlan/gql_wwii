from graphene import ObjectType

from app.gql.mutation.mission_mutation import AddMission
from app.gql.mutation.target_mutation import AddTarget


class Mutation(ObjectType):
    add_mission = AddMission.Field()
    add_target = AddTarget.Field()