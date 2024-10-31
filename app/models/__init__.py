from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .city import City
from .target import Target
from .country import Country
from .mission import Mission
from .target_type import TargetType
