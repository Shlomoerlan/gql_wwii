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

def get_mission_result_by_attack(target_type_id):
    with session_maker() as session:
        results = session.query(
            Mission.aircraft_returned.label("returned_aircraft"),
            Mission.aircraft_failed.label("failed_aircraft"),
            Mission.aircraft_damaged.label("damaged_aircraft"),
            Mission.aircraft_lost.label("lost_aircraft"),
            Target.target_priority.label("damage_assessment")
        ).join(Target).filter(
            Target.target_type_id == target_type_id
        ).all()
        return results

def add_mission(mission: Mission):
    with session_maker() as session:
        session.add(mission)
        session.commit()
        session.refresh(mission)
        return mission


def update_mission_attack_result(mission_id, returned_aircraft, failed_aircraft, damaged_aircraft, lost_aircraft, damage_assessment):
    with session_maker() as session:
        mission = session.query(Mission).filter_by(mission_id=mission_id).first()
        if mission:
            mission.returned_aircraft = returned_aircraft
            mission.failed_aircraft = failed_aircraft
            mission.damaged_aircraft = damaged_aircraft
            mission.lost_aircraft = lost_aircraft
            mission.damage_assessment = damage_assessment
            session.commit()
            session.refresh(mission)
        return mission