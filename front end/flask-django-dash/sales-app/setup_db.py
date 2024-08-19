# Launch flask shell and run these commands
db.drop_all()
db.create_all()

users = [
    {
        "first_name": "Scott",
        "last_name": "Tiger",
        "username": "stiger",
        "email": "stiger@email.com",
    },
    {
        "first_name": "Mickey",
        "last_name": "Mouse",
        "username": "mmouse",
        "email": "mmouse@email.com",
    },
    {
        "first_name": "Charlie",
        "last_name": "Chaplin",
        "username": "cchaplin",
        "email": "cchaplin@email.com",
    },
]

for user in users:
    user_rec = User(**user)
    db.session.add(user_rec)

db.session.commit()


courses = [
    {
        "course_name": "Mastering Python",
        "course_author": "Scott Tiger",
        "course_endpoint": "mastering-python",
    },
    {
        "course_name": "Python App Development",
        "course_author": "Donald Duck",
        "course_endpoint": "python-app-development",
    },
    {
        "course_name": "DevOps Bootcamp",
        "course_author": "Mickey Mouse",
        "course_endpoint": "devops-bootcamp",
    },
]

for item in courses:
    course = Course(**item)
    db.session.add(course)

db.session.commit()
