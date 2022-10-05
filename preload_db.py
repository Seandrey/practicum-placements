# Script to preload data into the DB that cannot be gained from the survey (e.g. the number of hours required for each unit)
# Author: Joel Phillips (22967051)

from typing import Optional
from app import db

from sqlalchemy.orm.scoping import scoped_session

from app.models import Unit

def get_or_add_unit(name: str, required_min: int) -> Unit:
    unit: Optional[Unit] = Unit.query.filter_by(unit=name).one_or_none()
    if unit is None:
        unit = Unit(unit=name, required_minutes=required_min)
        db.session.add(unit)
    assert unit.required_minutes == required_min, f"Unit {name} says required min of {unit.required_minutes} in DB but {required_min} desired!"
    return unit

def import_units():
    # FIXME: correct values
    get_or_add_unit("SSEH2295", 120)
    get_or_add_unit("SSEH3394", 200)

    # note that some units do not have cumulative hours from previous units counted. for example, 
    """
        Units as described by Jo:
        SSEH2295: 40. "definitely". 40 hours in that unit only.
        SSEH3345: 25 (2298 doesn't count). 25 in that unit only. 
        SSEH3385: 25 (2298 doesn't count)
        SSEH3393: 140 (earlier hours count towards it)
        SSEH3394: 140 (earlier hours count towards it)
        Apparently students can, but shouldn't, do units out of order (e.g. 2298 after 3345)
        DOn't worry about 4th year.
        She notes 45 and 85 are incompatible, and 93 and 94 are incompatible. 
    """

    db.session.commit()

def import_data():
    import_units()

if __name__ == "__main__":
    import_data()
