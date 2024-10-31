from app.db.database import session_maker
from app.models import Target


def add_target(mission_id, target_industry, city_id, target_type_id, target_priority):
    with session_maker() as session:
        new_target = Target(
            mission_id=mission_id,
            target_industry=target_industry,
            city_id=city_id,
            target_type_id=target_type_id,
            target_priority=target_priority
        )
        session.add(new_target)
        session.commit()
        session.refresh(new_target)
        return new_target