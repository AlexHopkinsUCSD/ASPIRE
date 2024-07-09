import logging
import random
from datetime import datetime, timedelta
from typing import Any, Dict, Iterable

from sqlmodel import SQLModel, Session
from app.domain.models.trigger_event import TriggerEventCreate, TriggerEvent

logger = logging.getLogger(__name__)

# TODO implement your own data seeding or remove this code. Also update app/api/app.py:register_events function

def _populate_table(
    db: Session, table: SQLModel, values: Iterable[Dict[str, Any]],
):
    name = table.__tablename__
    logger.info(f"Seeding table {name}")
    for v in values:
        db.add(table.from_orm(v))
    db.commit()
    logger.info(f"Seeded table {name} successfully")

def _populate_trigger_events_test(db: Session):
    concepts = ["string", "string1", "string2", "string3", "string4"]

    start_date, end_date = datetime(year=2020, month=1, day=1), datetime(year=2024, month=1, day=1)
    date_choices = [start_date]

    while start_date < end_date:
        # print(start_date)
        start_date += timedelta(days=2.0)
        date_choices.append(start_date)

    values = []
    for _ in range(250000):
        date = random.choice(date_choices)
        concept = random.choice(concepts)
        score = random.random()
        weight = random.random()
        test_event = TriggerEventCreate(datetime_stamp=date, student_id=random.choice([i for i in range(1000)]), concept=concept, value=score, weight=weight)
        values.append(test_event)

    _populate_table(db, TriggerEvent, values)


def run(db: Session) -> None:
    logger.info("Initializing databases")
    logger.info("Populating database")
    # for fn in [_populate_trigger_events_test]:
    #     fn(db)
    logger.info("Finished populating database")