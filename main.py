# استدعاء المكتيات اللازمة

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# تشغيل البرنامج
app = Flask(__name__)
# اتصال قاعدة البيانات بوستغرس
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:baqerali123@localhost/flask_app'
db = SQLAlchemy(app)


# انشاء جدول و الاتصال به دائماً
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    def __repr__(self):
        return f'<User {self.username}>'
# دفع البيانات الى الجدول


app.app_context().push()
db.create_all()

# روت الموقع


@app.route('/')
def home():
    # people = استدعاء جميع البيانات المخزونة في القاعدة
    people = Person.query.all()
    return render_template('home.html', people=people)

# اضافة شخص جديد الى قاعدة البيانات


@app.route('/add_person', methods=['POST', 'GET'])
def add_person():

    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')

    # اسناد القيم الاتية من الفورمة الى قيم الجدول لغرض حفظها
    person = Person(first_name=first_name, last_name=last_name)

    db.session.add(person)
    db.session.commit()

    return render_template('baqerdata.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
