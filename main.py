import os
import smtplib
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from wtforms.fields.simple import SubmitField, StringField, EmailField


app = Flask(__name__)




class AboutForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    message = StringField('Message:', validators=[DataRequired()])
    email = EmailField('E-Mail:', validators=[DataRequired(), Email()])
    submit = SubmitField('SEND')


@app.route("/")
def home():

    return render_template("index.html")

@app.route("/menu")
def menu():

    return render_template("menu.html")

@app.route("/about", methods=['GET', 'POST'])
def about():
    aboutform = AboutForm()
    if aboutform.validate_on_submit():
        name = aboutform.name.data
        email = aboutform.email.data
        message = aboutform.message.data
        my_email = os.getenv('my_email')
        password = os.getenv('password')
        mail = os.getenv('mails')

        with smtplib.SMTP("mail.johnmapunda.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=mail,
                msg=f"Subject:{email}\n\nHello i am {name} \nMessage:{message}\n{email}."
                )

        return redirect(url_for('home'))

    return render_template("about.html", aboutform=aboutform,)


if __name__ == '__main__':
    app.run(debug=True)
