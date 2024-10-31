from sqlalchemy import and_
from app.db.database import session_maker
from app.models import Mission, Country, Target, City
from returns.result import Result, Success, Failure


def get_all_missions():
    with session_maker() as session:
        return session.query(Mission).all()


def get_missions_by_date_range(start_date, end_date):
    try:
        with session_maker() as session:
            missions = session.query(Mission).filter(
                and_(Mission.mission_date >= start_date, Mission.mission_date <= end_date)
            ).all()
            return Success(missions)
    except Exception as e:
        session.rollback()
        return Failure(str(e))

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

def add_mission(mission_date, airborne_aircraft, attacking_aircraft, bombing_aircraft,
               aircraft_returned, aircraft_failed, aircraft_damaged, aircraft_lost):
    with session_maker() as session:
        mission = Mission(
            mission_date=mission_date,
            airborne_aircraft=airborne_aircraft,
            attacking_aircraft=attacking_aircraft,
            bombing_aircraft=bombing_aircraft,
            aircraft_returned=aircraft_returned,
            aircraft_failed=aircraft_failed,
            aircraft_damaged=aircraft_damaged,
            aircraft_lost=aircraft_lost
        )
        session.add(mission)
        session.commit()
        session.refresh(mission)
        return mission


def update_mission_attack_result(mission_id, returned_aircraft, failed_aircraft, damaged_aircraft, lost_aircraft):
    with session_maker() as session:
        mission = session.query(Mission).filter_by(mission_id=mission_id).first()
        if mission:
            mission.aircraft_returned = returned_aircraft
            mission.aircraft_failed = failed_aircraft
            mission.aircraft_damaged = damaged_aircraft
            mission.aircraft_lost = lost_aircraft
            session.commit()
            session.refresh(mission)
        return mission


def update_attack_result(mission_id, returned_aircraft, failed_aircraft, damaged_aircraft,
                         lost_aircraft):
    with session_maker() as session:
        mission = session.query(Mission).filter_by(mission_id=mission_id).first()
        if not mission:
            raise ValueError("Mission not found")
        mission.aircraft_returned = returned_aircraft
        mission.aircraft_failed = failed_aircraft
        mission.aircraft_damaged = damaged_aircraft
        mission.aircraft_lost = lost_aircraft
        session.commit()
        session.refresh(mission)
        return mission

def delete_mission(mission_id: int) -> Result[Mission, str]:
    with (session_maker() as session):
        try:
            mission = session.query(Mission).filter_by(mission_id=mission_id).first()
            if not mission:
                return Failure("Mission not found")
            session.delete(mission)
            session.commit()
            return Success(mission)
        except Exception as e:
            session.rollback()
            return Failure(str(e))
