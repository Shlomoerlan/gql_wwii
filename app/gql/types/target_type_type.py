from graphene import ObjectType, Int, String


class TargetTypeType(ObjectType):
    target_type_id = Int(required=True)
    target_type_name = String(required=True)