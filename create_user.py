from app import db, User

# first_user = User(username ='wc1321@uw.edu', password = 'qwerty' )
# db.session.add(first_user)
# db.session.commit()


with app.app_context():
    all_users = User.query.all()

print(all_users)