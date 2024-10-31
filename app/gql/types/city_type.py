from graphene import ObjectType, String, Int, Float


class CityType(ObjectType):
    city_id = Int()
    city_name = String()
    county_id = Int()
    lat = Float()
    lon = Float()