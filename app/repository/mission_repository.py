from datetime import date
from typing import List

from sqlalchemy import and_, func
from app.db.database import session_maker
from app.models import Mission, Country, Target, City
from returns.result import Result, Success, Failure


def get_all_missions():
    with session_maker() as session:
        return session.query(Mission).all()


def get_missions_by_date_range(start_date: date, end_date: date):
    try:
        with session_maker() as session:
            missions = session.query(Mission).filter(
                and_(Mission.mission_date >= start_date, Mission.mission_date <= end_date)
            ).all()
            return Success(missions)
    except Exception as e:
        session.rollback()
        return Failure(str(e))

def get_mission_by_id(mission_id: int) -> Result[Mission, str]:
    try:
        with session_maker() as session:
            mission = session.query(Mission).filter(Mission.mission_id == mission_id).first()
            return Success(mission)
    except Exception as e:
        session.rollback()
        return Failure(str(e))

def get_mission_by_country(country_name: str) -> List[Mission]:
    with session_maker() as session:
        missions = session.query(Mission).join(Mission.targets).join(Target.city).join(City.country).filter(
            Country.country_name == country_name
        ).all()
        return missions

def get_mission_by_industry(industry: str) -> List[Mission]:
    with session_maker() as session:
        missions = session.query(Mission).join(Mission.targets).filter(
            Target.target_industry == industry
        ).all()
        return missions

def get_mission_result_by_attack(target_type_id: int):
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

def add_mission(mission_date: date, airborne_aircraft: int, attacking_aircraft: int, bombing_aircraft: int,
               aircraft_returned: int, aircraft_failed: int, aircraft_damaged: int, aircraft_lost: int) -> Result[Mission, str]:
    try:
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
            return Success(mission)
    except Exception as e:
        session.rollback()
        return Failure(str(e))


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

# def get_mission_statistics_by_city(city_name):
#     with session_maker() as s:
#         results = s.query(
#             City.city_name,
#             func.count(Mission.mission_id).label("mission_count"),
#             func.avg(Target.target_priority).label("average_target_priority")
#         ).join(Target, Target.city_id == City.city_id) \
#             .join(Mission, Mission.mission_id == Target.mission_id) \
#             .group_by(City.city_name) \
#             .all()
#
#         return results



def get_mission_statistics_by_city(city_name: str) -> Result[dict, str]:
    try:
        with session_maker() as session:
            result = session.query(
                City.city_name,
                func.count(Mission.mission_id).label("mission_count"),
                func.avg(Target.target_priority).label("average_target_priority")
            ).join(Target, Target.city_id == City.city_id) \
                .join(Mission, Mission.mission_id == Target.mission_id) \
                .filter(City.city_name == city_name) \
                .group_by(City.city_name) \
                .first()

            if result is None:
                return Failure(f"No data found for city: {city_name}")

            stats = {
                "city_name": result.city_name,
                "mission_count": result.mission_count,
                "average_target_priority": result.average_target_priority
            }

            return Success(stats)
    except Exception as e:
        return Failure(str(e))
print(get_mission_statistics_by_city("100 AIRCRAFT ON BEACH").unwrap())