from graphene import ObjectType, Int, String


class CountryType(ObjectType):
    country_id = Int()
    country_name = String()