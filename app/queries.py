# from app.models import *
from app import db
from app.models import *





# result = db.session.query(ActivityLog, Activity, Domain).outerjoin(Domain, isouter=True).outerjoin(Activity).all()
#     user = User.query.filter_by(username='testing').first()
#     # location = db.session.query(Location.location, sum(ActivityLog.minutes_spent)).leftjoin(Activity_Log, location.locationid = activity_log.locationid group by location.location having activity_log.studentid = 1
#     session: scoped_session = db.session
#     loc = session.query(
#         ActivityLog.minutes_spent, Activity.activity, Activity.activityid, Domain.domain, Domain.domainid).outerjoin(Domain, isouter=True).outerjoin(Activity).filter(Activity.activity == Activity)
#     # location = loc.query(MINUTES_SPENT, Domain.domain, func.sum(ActivityLog.minutes_spent)).groupby()
#     location = loc.groupby


# # user=user, location=location, result=result

#On what premise should the Core, 

def checkPass(studid, minHours):
    #Determines if student has enough hours to pass all requirements
    check = db.session.query(func.sum(ActivityLog.minutes_spent)).filter(ActivityLog.studentid==studid).first()
    if ((check[0] % 10) > minHours):
        return True
    return False

def studentRep():
    #Returns student Table
    students = db.session.query(Student).all()
    return students

def queryStudent(studname):
    #finds student id
    student = db.session.query(Student).filter(Student.name==studname).all()
    print(student[0].studentid)
    return student


def createLocationRep(studid):
    locations = db.session.query(Location.location).all()
    studlocation = db.session.query(Location.location, func.sum(ActivityLog.minutes_spent)).join(ActivityLog, Location.locationid == ActivityLog.locationid).filter(ActivityLog.studentid==studid).group_by(Location.location).all()

    #convert list object into tuple


    location = {}

    for loc, minutes in studlocation:
        location[loc] = minutes
    for loc in locations:
        if loc.location not in location:
            location[loc.location] = 0.0
    return location


#Create New Table of DomainACT
#Columns are Activity Types
#Domains are Rows
# Measurements are Hours Used
# Go Figure

# Test Transposing of Activity Types, With Filters

#Essentially creating a new table from 3.

#2D Array?

def createDomainAct(studid):
    # domain = db.session.query(Domain.domain, Activity)
    domain = db.session.query(Domain.domain, Activity.activity, func.sum(ActivityLog.minutes_spent)).outerjoin(Domain).outerjoin(Activity).filter(ActivityLog.studentid==studid).group_by(Domain.domain).all()
    return(domain)


def createReport(studid, minHours):
    local = createLocationRep(studid)
    data = {'location': local,'check': checkPass(studid, minHours), 'domainAct':createDomainAct(studid)}
    return data
