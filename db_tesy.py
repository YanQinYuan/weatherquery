from weather_run import db
# db.create_all()
from weather_run import User
admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com')
db.session.add(admin)
db.session.add(guest)
db.session.commit()
print(User.query.all())
print(User.query.filter_by(username='admin').first())