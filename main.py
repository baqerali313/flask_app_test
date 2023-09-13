# استدعاء المكتيات اللازمة

from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo

# تشغيل البرنامج
app = Flask(__name__)

# اتصال قاعدة البيانات بوستغرس
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:baqerali123@localhost/flask_app'
db = SQLAlchemy(app)
# مفتاح سري للفورمة و حماية من ثغرة csrf
app.config['SECRET_KEY'] = 'BAQERALI123_@@'


# # انشاء جدول و الاتصال به دائماً
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


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    wordtopass = db.Column(db.String(50))

    def __repr__(self):
        return f'<User {self.email}>'


# دفع البيانات الى الجدول


app.app_context().push()
db.create_all()


# كلاس لغرض تفعيل الفاليديترز
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('submit')


class UpdateForm(FlaskForm):
    email = StringField('البريد الإلكتروني', validators=[DataRequired()])
    new_password = PasswordField('كلمة المرور الجديدة', validators=[DataRequired()])
    confirm_password = PasswordField('تأكيد كلمة المرور الجديدة', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('تحديث')


@app.route('/')
def home():
    # people = استدعاء جميع البيانات المخزونة في القاعدة

    return render_template('home.html')


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


@app.route('/about', methods=['POST', 'GET'])
def about():
    users = Users.query.all()
    email = None
    password = None
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        flash('submit is successfully!!')

        # اسناد القيم الاتية من الفورمة الى قيم الجدول لغرض حفظها
        user = Users(email=email, wordtopass=password)
        db.session.add(user)
        db.session.commit()

        form.email.data = ''
        form.password.data = ''
        return redirect('/')

    return render_template('about.html', email=email, password=password, form=form, users=users)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user_update = Users.query.get_or_404(id)
    form = UpdateForm()  # تأكد من أنك تستخدم الفورم الصحيح هنا

    if request.method == 'POST' and form.validate_on_submit():
        # تحديث البريد الإلكتروني
        user_update.email = form.email.data
        user_update.wordtopass = form.new_password.data
        db.session.commit()
        return redirect(url_for('about', id=user_update.id))

    return render_template('update.html', form=form, user_update=user_update)


if __name__ == "__main__":
    app.run(debug=True)
