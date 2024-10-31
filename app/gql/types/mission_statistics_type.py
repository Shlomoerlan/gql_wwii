from graphene import ObjectType, List, Int, Float
from app.gql.types import MissionType

class MissionStatisticsType(ObjectType):
    missions = List(MissionType)
    total_missions = Int()
    average_target_priority = Float()