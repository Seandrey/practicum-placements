# Build charts for google charts to display
# Author: David Norris (22690264)

from app.models import *
from app import db
import random
import contextlib
from sqlalchemy import MetaData

# 500 Random names
names_list = ["Brandon Bell", "Victoria Little", "Samuel Wilkinson", "Charles Taylor", "Stephen Hopkins", "Justin Chan", "Matthew Hobbs", "George Morgan", "Donald Ritter", "Margaret Hamilton", "William Mullen", "Keith Simmons", "Roberta Boyle", "Tammy Matthews", "Ryan Stephens", "Helen Thompson", "Judith Smith", "Timothy Mack", "Lisa Hernandez", "Gabriel Willis", "Zachary Smith", "Sylvia Chen", "Sydney Johnson", "Cheryl Miller", "Casey Green", "Justin Miller", "Robert Welch", "Jesse Farley", "Courtney Wilson", "Craig Brown", "Christine Mendoza", "Danielle Juarez", "Bridget Blake", "Bailey Brown", "Juan Shannon", "Eric Mcclure", "Rachel Hudson", "Melissa Garcia", "Andrew Tran", "James Gonzalez", "Rachel Smith", "Christopher Morrow", "Shane Stark", "Earl Johnson", "Larry Moss", "Laurie Case", "Jennifer Garner", "Robert Ramos", "Chris Wilkins", "Maria Rice", "Margaret Jenkins", "Charles Ferguson", "Seth Jones", "Alex Thompson", "James Mcbride", "Annette Brown", "Jennifer Orozco", "Daniel Cannon", "Caleb Christensen", "Kathleen Smith", "Laura Hernandez", "Douglas Johnson", "Theresa Taylor", "Cynthia Mann", "Angelica Spencer", "Eileen Patel", "Elizabeth Thompson", "Richard Lee", "Sierra Daniels", "Christine Perez", "Barry Daniel", "Justin Bates", "Edwin Stone", "Paul Garner", "Randy Chapman", "Jamie Jones", "Alex Rose", "Melissa Williams", "Michelle Reed", "John Salinas", "Debra Michael", "Donna Hendricks", "Thomas Romero", "Robert Cochran", "Ryan Grant", "Terry Hunter", "Micheal Brooks", "Tricia Mathis", "Leslie House", "Andrew Davis", "Belinda Wade", "Nicole Wiggins", "Lisa Ferguson", "Taylor Hanson", "Mrs. Pamela Fleming", "Matthew Miles", "Toni Small", "Jordan Davis", "Tyler Drake", "Ralph Barber", "Paige Cook", "Penny Santos", "Amy King", "Anthony Smith", "Sarah Munoz", "Amy Howard", "Paul Butler", "Joshua Matthews", "Robin Phillips", "Angela Horton", "Michele Arnold", "Emily White", "David Bishop", "William Lewis", "Alison Klein", "Cory Jenkins", "Brian Moore", "John Ryan", "Clarence Ruiz", "Angel Holland", "Justin Schneider", "Matthew Jones", "James Acosta", "Miguel Walker", "Kathleen Long", "Megan Armstrong", "Sheena Mcdaniel", "Matthew Parker", "Benjamin Carter", "Ariel Vasquez", "Brett Kidd", "Suzanne Powers", "Justin Little", "Maxwell Meza", "Erica Vega", "Kimberly Miller", "Brittany Kelly", "Trevor Osborne", "John Hester", "Eric Baldwin", "Danielle Mccoy", "Evan Bailey", "Stephen Anderson", "Brian Hill", "Dustin Smith", "Dennis Melton", "Misty Jimenez", "Duane Rodriguez", "Andrew Silva", "Casey Collins", "Sarah Hines", "Laura Bradford", "Heather Myers", "Andrew Soto", "Jennifer Mendoza", "Amanda Wolf", "Mr. Cory Morrison MD", "Emily James", "Jennifer Gonzalez", "Stephanie Miller", "Jeffery Jones", "Danielle George", "Antonio Yang", "John Harris", "Linda Garcia", "Richard Flynn", "Allen Wright", "Michael Williams", "Joshua Kelley", "Samantha Rojas", "Christopher Ewing", "Andrew Li", "Madeline Davenport", "Roy Myers", "George Martin", "Michael Kelley", "Kristin Patterson", "Christopher Flores", "Michael Phillips", "Mrs. Julie Hudson", "Claire Baker", "Jeffrey Palmer DDS", "Arthur Hanna", "Richard King", "Wendy Wilson", "Jo Cooper", "Tara Brown", "Brett Pitts", "Matthew Butler", "Benjamin Johnson", "Paul Fox", "Michael Richard", "Jennifer Smith", "Bonnie Chase", "Sara Mcknight", "Robert Short", "Michelle Tanner", "Karen Villanueva", "Eric Walters", "Allen Weber", "Robin Parrish", "Julie Hutchinson DVM", "Veronica Russell", "Sarah Weaver", "Ronnie Griffith", "Brenda Ramirez", "John Goodman", "Tiffany Wagner", "Michael Richardson", "Samuel Williams", "Christopher Hill", "Nathan Lynch", "Michael Powers", "Patricia Banks", "Deanna Baldwin", "Joshua Torres", "Earl Dalton", "Charles Munoz", "Douglas Evans", "Matthew Garcia", "Julia Hubbard", "Andrea White", "Jerry Dodson", "Angela Morris", "Sherri Reid", "Nicole Jones DVM", "Gloria James", "Steven Blake", "Paul Bradley", "Mary Guerrero", "Andrew Cruz", "Paul Scott", "Misty Hicks", "Tracy Hunter", "Mackenzie Carroll", "Amy Collins", "Shannon Vargas", "Katrina Anderson", "David Anderson", "Natalie Brown DDS", "Ashley Hughes", "Brian Richardson", "Lisa Bentley", "Colton Fernandez", "Susan Singh", "John Leonard", "Mark Turner", "Jeremy Garcia", "Sydney Richard", "Shannon Cooper", "Willie Briggs",
              "Denise Knight", "Mark Moses", "Daniel Freeman", "Glen Romero", "Tiffany Villarreal", "Robert Morris", "Amber Thomas", "Phillip Henson", "Michelle Miller", "James Ross", "Samantha Kelley", "Joshua Brown", "Joseph Walker", "Laurie Shaw", "Ashley Hill", "Brian Wallace", "Richard Morrison", "Ronald Arnold MD", "Jane Bennett", "Whitney Hurst", "Samantha Phillips", "Daniel Pena", "Sharon Greene", "Anne Cain", "Kyle Huff", "Dawn Sanchez", "Richard Orr", "Angela Hayes", "Courtney Ferguson", "Jason Myers", "Ashley Hansen", "Sarah White", "Katie Kirby", "Kimberly Mitchell", "Ronnie Bailey", "Veronica Grant", "Kevin Gonzalez", "Pamela Wheeler", "Eddie Ramirez", "Shelly Perry", "Bailey Callahan", "Stacey Thomas", "Isabel Berger", "James Knight", "Kevin Reynolds", "Susan Gordon", "Brittany Banks", "Roy Small", "Deanna Sharp", "William Cox", "Linda Burnett", "Cathy Kennedy", "Jennifer Smith", "Pam Black", "Tonya Hughes", "Alex Nguyen", "Rachel Carroll", "Keith Murray", "Colleen Martin", "Kelly Edwards", "Michael David", "Corey Ortiz", "Alyssa Harrell", "Sharon Salazar", "Gabriela Williams", "Mark Reynolds", "Kimberly Butler", "Alicia Stephenson", "Mr. Jeremy Moon DDS", "Loretta Edwards", "Lisa Dickson", "Janice Brewer", "Tracey Douglas", "Anthony Miller", "Jennifer Jones MD", "Bethany Holden", "Mary Mclean", "John Chapman", "Regina Johnson", "Daniel Evans", "Lori Lyons", "Anthony Thomas", "Jesse Ware", "Christopher Steele", "Jenny Scott", "Christopher Jones", "Angela Lopez", "Andrew Daugherty", "Daniel Calhoun", "Oscar Mckenzie", "Abigail Anderson", "Jesus Cooper", "Stacie Ponce", "Stephen Lewis", "Jessica Fitzgerald", "Mary Roberts", "Thomas Rasmussen", "Larry Rodgers", "Debra Carter", "John Day", "Carrie Lee", "Rachel Bell", "Patrick Mejia", "Brandon Roberts", "Donna Mcdonald", "Sandra Perez", "Katherine Hunt", "Lisa Valencia", "Danielle Murphy", "Cynthia Carter", "Danielle Young", "Nicole Miles", "Henry Spencer", "Steven Barker DDS", "Lawrence Reynolds", "Mary Larson", "Brian Mcmillan", "Laura Day", "Brandon Gonzalez", "James Gonzalez", "Christopher Rodriguez", "Hunter Edwards", "Alison Williams", "Shelby Gonzalez", "Edward Lambert", "Julie Peterson", "Michael Brown", "Virginia Stuart", "William Chen", "Cassandra Kelly", "Jennifer Lambert", "Ms. Tara Gonzalez", "Steven Sosa", "Lindsay Rivera", "Jesse Black", "Jessica Mendoza", "Jay Rogers", "Justin Mcdonald", "Kelli Bowen", "Mr. Brian Williamson", "Ronald Jackson", "Laurie Mccullough", "Alexis Delgado", "Robert Burnett III", "Priscilla Adams", "Gwendolyn Horton", "Melissa Lewis", "Diana Watson", "Marissa Thompson", "Sheila Hunter", "Mr. Shane Gregory", "Lisa Oconnor", "Kelly Allen", "Carrie Lopez", "Kenneth Anderson", "Ruben Collier", "Mark Odom", "Joel Snow", "Andrew Johns", "Taylor Campbell", "Terri Ayala", "Miss Rebecca Montgomery", "Kristen Gomez", "April Barnett", "Annette Santos", "Thomas Ortiz", "Mr. Matthew Collins", "Michele Hale", "Melissa Diaz", "Pamela Gilmore", "Michael Murphy", "Elizabeth Moreno", "Travis Becker", "Allen Cantrell", "Tracy Cook", "Kyle Mcclain", "Jeremy Clark", "Ashley Weber", "Jennifer Roberts", "Robert Reynolds", "Gary Smith", "Lindsey West", "Charles Stevenson", "Julie Travis", "Mallory Potter", "Cindy Lewis", "Eric Williams", "Jeremiah Snyder", "Shane Smith", "Janice Bass", "Holly Weiss", "Sarah Duncan", "Javier Smith", "Monica Fitzpatrick", "Sandra Rasmussen", "Emily Little", "Corey Rice MD", "Robin Brown", "Bryan Wilson", "Rachel Whitney", "Daniel Pena", "Tammy Santana", "Paul Levy", "Wendy Burke", "Brenda Summers", "Jillian Payne", "Gary Brown", "Jennifer Gonzalez", "Leslie Cole", "Amanda Alvarado", "Benjamin Macias", "Steven Black", "Pamela Patterson", "Shannon Wright", "Eric Williams", "Nicholas Miranda", "Robert Graham", "Savannah Adams", "Ronald Mills", "Ashley Freeman", "Ryan Key", "Manuel Shelton", "Wesley Hopkins", "Ashley Christensen", "Madeline Floyd", "Joshua Perry", "Anthony Mcclain", "Michelle Hall", "Brian Perry", "Philip Rogers", "Crystal Smith", "Monica Smith", "Ryan Edwards", "Mary Coleman", "Aaron Dorsey", "Charles Campbell", "Gary Stevenson", "Mackenzie Ryan", "Wanda Santana", "Anthony Johnson", "Deanna Mcknight", "Gregory Hernandez", "David Guzman", "Amanda Harper", "Wanda Rich", "Crystal Jones", "Mary Rodriguez", "Kelsey Rodriguez", "Mary White"]

d = (
    'Health/Fitness',
    'Sport and Perfomance',
    'Healthy Aging',
    'Paediatics & Young People',
    'Mental Health & Wellness',
    'Community Wellness',
    'Employment Health & Wellness',
    'Clinical Case'
)
a = (
    'Excercise Assessment',
    'Excercise Prescription',
    'Excercise Delivery',
    'Other'
)
l = (
    'UWA Exercise & Performance Centre',
    'WACRH (Geraldton)',
    'Agility Rehabilitation',
    'Curtin Stadium'
    'Fiona Stanley Hospital',
    'Guardian Exercise Rehabilitation',
    'Health Care WA',
    'HFRC',
    'Made to Move Rehabilitation Gym',
    'Neuromoves',
    'O2 Active',
    'Redimed',
    'Reps Movement',
    'The Exercise Therapist',
    'Other/Self Directed',
    'Shenton College'
)
# 20 random names from the list = 20 supervisors
s = [random.choice(names_list) for _ in range(1, 20)]


def teardown_db():
    """removes all db table entries except user table"""
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        if '%s' % table != 'user':
            print('Clear table %s' % table)
            db.session.execute(table.delete())
    db.session.commit()


def fill_db_multiple_students(num):
    """fill the db with n students equal to param num. 
    student id start at 2200000 and increment by 1 to 22000000 + num"""
    count = 0
    for domain in d:
        if count < 3:
            i = Domain(domain=domain, core=True)
        else:
            i = Domain(domain=domain, core=False)
        db.session.add(i)
        count += 1

    for activity in a:
        i = Activity(activity=activity)
        db.session.add(i)

    for location in l:
        i = Location(location=location)
        db.session.add(i)

    for supervisor in s:
        i = Supervisor(name=supervisor)
        db.session.add(i)

    db.session.commit()

    for i in range(0, num):
        fill_db_student_random_hours(22000000 + i, random.choice(names_list))


def fill_db_student_random_hours(studentid, name):
    """fill db with a student entry with id of param student id and name name, also generate 50 activity entries"""
    st = Student(studentid=studentid, name=name)
    db.session.add(st)
    for i in range(0, 50):
        al = ActivityLog(studentid=studentid, domainid=random.randint(1, len(d)), activityid=random.randint(1, len(
            a)), locationid=random.randint(1, len(l)), supervisorid=random.randint(1, len(s)), minutes_spent=random.randint(40, 200))
        db.session.add(al)

    db.session.commit()


def build_chart(key, value, core=True):
    """format some queries to populate a dictionary the way google charts expects, this passed after using json.dumps() into a jinja macro data structure"""
    title = ''
    if key == 'student':
        q = db.session.query(ActivityLog).filter_by(
            studentid=value).order_by("domainid").all()
        title = db.session.query(Student).filter_by(
            studentid=value).first().name
    elif key == 'location':
        q = db.session.query(ActivityLog).filter_by(
            locationid=value).order_by("domainid").all()
        title = db.session.query(Location).filter_by(
            locationid=value).first().location

    q = db.session.query(Domain).filter_by(core=core).all()
    domains = [domain.domain for domain in q]
    length = len(domains)
    domains.insert(0, 'Category')
    # this is for google charts annotations
    domains.append({'role': 'annotation'})
    # this is for google charts annotations
    domains.append({'role': 'annotation'})

    data = {
        'title': title + ' Core' if core else title + ' Additional',
        'graph': [domains],
        'total': 0,
        'len': length
    }

    q = db.session.query(Activity).all()
    data['activities'] = [act.activity for act in q]
    for activity in q:
        activityHours = [0] * data['len']
        activityHours.insert(0, activity.activity)
        p = db.session.query(
            ActivityLog.domainid,
            func.sum(ActivityLog.minutes_spent).label('total'),
            Domain.core,
        ).join(Activity.logs
               ).filter(Domain.core == core, Domain.domainid == ActivityLog.domainid
                        ).filter(ActivityLog.activityid == activity.activityid
                                 ).group_by(ActivityLog.domainid
                                            ).all()

        total = 0
        for domain in p:
            activityHours[domain[0] if core else domain[0] -
                          3] = round(domain[1] / 60, 2)
            total += round(domain[1] / 60, 2)
        data['total'] += round(total, 2)
        activityHours.append(total)  # this is for google charts annotations
        activityHours.append('')  # this is for google charts annotations

        data['graph'].append(activityHours)

    return data


def get_student_info(studentid):
    data = {}
    data['core'] = build_chart('student', studentid, True)
    data['additional'] = build_chart('student', studentid, False)
    # here we should also add data for location and domain, currently only gains graphs
    return data
