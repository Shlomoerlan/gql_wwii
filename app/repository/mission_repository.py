from sqlalchemy import and_

from app.db.database import session_maker
from app.models import Mission, Country, Target, City


def get_all_missions():
    with session_maker() as session:
        return session.query(Mission).limit(10)


def get_missions_by_date_range(start_date, end_date):
    with session_maker() as session:
        missions = session.query(Mission).filter(
            and_(Mission.mission_date >= start_date, Mission.mission_date <= end_date)
        ).all()
        return missions

def get_mission_by_id(mission_id):
    with session_maker() as session:
        mission = session.query(Mission).filter(Mission.mission_id == mission_id).first()
        return mission

def get_mission_by_country(country_name):
    with session_maker() as session:
        missions = session.query(Mission).join(Mission.targets).join(Target.city).join(City.country).filter(
            Country.country_name == country_name
        ).all()
        return missions

def get_mission_by_industry(industry):
    with session_maker() as session:
        missions = session.query(Mission).join(Mission.targets).filter(
            Target.target_industry == industry
        ).all()
        return missions