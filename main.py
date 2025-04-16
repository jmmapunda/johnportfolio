import datetime
import os
import smtplib
from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from flask.cli import load_dotenv
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, NumberRange
from wtforms.fields.simple import SubmitField, StringField, EmailField
from wtforms import FloatField

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'


class ConnectForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    message = StringField('Message:', validators=[DataRequired()])
    email = EmailField('E-Mail:', validators=[DataRequired(), Email()])
    submit = SubmitField('SEND')

class CalculatorForm(FlaskForm):
    salary = FloatField("Monthly Salary", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Calculate")

menudata = {
    "Burgers": {
        "url": "BBQ Burger.webp",  # Category URL
        "items": {
            "Cheese Burger": {
                "description": "Beef patty, cheese, lettuce, tomato",
                "price": 8000,
                "url": "Cheese Burger.webp"  # Item URL
            },
            "BBQ Burger": {
                "description": "Grilled beef, BBQ sauce, onions",
                "price": 9500,
                "url": "BBQ Burger.webp"  # Item URL
            },
            "Veggie Burger": {
                "description": "Plant-based patty, lettuce, mayo",
                "price": 7500,
                "url": "veggie burger.webp"  # Item URL
            },
            "Spicy Burger": {
                "description": "Jalapeños, spicy sauce, beef",
                "price": 10000,
                "url": "spicy burger.webp"  # Item URL
            },
            "Mushroom Burger": {
                "description": "Mushrooms, Swiss cheese, beef",
                "price": 9000,
                "url": "mushroom burger.webp"  # Item URL
            },
        }
    },
    "Pizzas": {
        "url": "bbq chicken pizza.webp",  # Category URL
        "items": {
            "Margherita": {
                "description": "Tomato, mozzarella, basil",
                "price": 12000,
                "url": "margherita.webp"  # Item URL
            },
            "Pepperoni": {
                "description": "Pepperoni, cheese, tomato sauce",
                "price": 14000,
                "url": "pepperoni.webp"  # Item URL
            },
            "BBQ Chicken": {
                "description": "BBQ chicken, onions, peppers",
                "price": 15000,
                "url": "bbq chicken pizza.webp"  # Item URL
            },
            "Veggie Supreme": {
                "description": "Bell peppers, mushrooms, olives",
                "price": 13500,
                "url": "veggie supreme.webp"  # Item URL
            },
            "Four Cheese": {
                "description": "Mozzarella, cheddar, parmesan",
                "price": 16000,
                "url": "four cheese.webp"  # Item URL
            },
        }
    },
    "Drinks": {
        "url": "coke.webp",  # Category URL
        "items": {
            "Coke": {
                "description": "Classic cola drink",
                "price": 2500,
                "url": "coke.webp"  # Item URL
            },
            "Orange Juice": {
                "description": "Freshly squeezed oranges",
                "price": 3500,
                "url": "orange juice.webp"  # Item URL
            },
            "Lemonade": {
                "description": "Sweet & sour lemon drink",
                "price": 3000,
                "url": "lemonade.webp"  # Item URL
            },
            "Iced Tea": {
                "description": "Cold brewed tea with lemon",
                "price": 3500,
                "url": "iced tea.webp"  # Item URL
            },
            "Milkshake": {
                "description": "Vanilla, chocolate, or strawberry",
                "price": 5000,
                "url": "milkshake.webp"  # Item URL
            },
        }
    },
    "Desserts": {
        "url": "chocolate cake.webp",  # Category URL
        "items": {
            "Chocolate Cake": {
                "description": "Rich, moist chocolate cake",
                "price": 6000,
                "url": "chocolate cake.webp"  # Item URL
            },
            "Cheesecake": {
                "description": "Classic New York-style cheesecake",
                "price": 7000,
                "url": "cheesecake.webp"  # Item URL
            },
            "Apple Pie": {
                "description": "Warm apple pie with cinnamon",
                "price": 5500,
                "url": "apple pie.webp"  # Item URL
            },
            "Ice Cream Sundae": {
                "description": "Vanilla ice cream, chocolate syrup",
                "price": 5000,
                "url": "ice cream sundae.webp"  # Item URL
            },
            "Tiramisu": {
                "description": "Italian coffee-flavored dessert",
                "price": 8500,
                "url": "tiramisu.webp"  # Item URL
            },
        }
    },
    "Pasta": {
        "url": "spaghetti bolognese.webp",  # Category URL
        "items": {
            "Spaghetti Bolognese": {
                "description": "Pasta with rich meat sauce",
                "price": 10500,
                "url": "spaghetti bolognese.webp"  # Item URL
            },
            "Chicken Alfredo": {
                "description": "Creamy garlic sauce, grilled chicken",
                "price": 11000,
                "url": "chicken alfredo.webp"  # Item URL
            },
            "Penne Arrabbiata": {
                "description": "Spicy tomato sauce, parmesan",
                "price": 9500,
                "url": "penne arrabbiata.webp"  # Item URL
            },
            "Lasagna": {
                "description": "Layered pasta, beef, ricotta cheese",
                "price": 12000,
                "url": "lasagna.webp"  # Item URL
            },
            "Pesto Pasta": {
                "description": "Basil pesto, cherry tomatoes",
                "price": 10000,
                "url": "pesto pasta.webp"  # Item URL
            },
        }
    },
    "Seafood": {
        "url": "grilled salmon.webp",  # Category URL
        "items": {
            "Grilled Salmon": {
                "description": "Served with lemon butter sauce",
                "price": 18000,
                "url": "grilled salmon.webp"  # Item URL
            },
            "Garlic Shrimp": {
                "description": "Sauteed shrimp in garlic butter",
                "price": 16500,
                "url": "garlic shrimp.webp"  # Item URL
            },
            "Fish & Chips": {
                "description": "Crispy battered fish, fries",
                "price": 14000,
                "url": "fish & chips.webp"  # Item URL
            },
            "Lobster Thermidor": {
                "description": "Baked lobster in creamy sauce",
                "price": 25000,
                "url": "lobster thermidor.webp"  # Item URL
            },
            "Calamari Rings": {
                "description": "Fried squid rings, tartar sauce",
                "price": 13000,
                "url": "calamari rings.webp"  # Item URL
            },
        }
    },
}

menukey = menudata.keys()

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.datetime.now().year}

@app.route("/home")
@app.route("/")
def home():

    return render_template("index.html")

@app.route("/menu")
def menu():

    return render_template("menu.html", menudata=menudata, menukey=menukey)

@app.route("/about")
def about():

    return render_template("about.html",)

@app.route("/connect", methods=['GET', 'POST'])
def connect():
    connectform = ConnectForm()
    if connectform.validate_on_submit():
        name = connectform.name.data
        email = connectform.email.data
        message = connectform.message.data
        my_email = 'admin@johnmapunda.com'
        password = os.getenv('password')
        mail = 'admin@johnmapunda.com'
        print(password)

        with smtplib.SMTP("mail.johnmapunda.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=mail,
                msg=f"Subject:{email}\n\nHello i am {name} \nMessage:{message}\n{email}."
                )

        return redirect(url_for('home'))

    return render_template("connect.html", connectform=connectform,)

@app.route("/calculator", methods=['GET', 'POST'])
def calculator():
    calculatorform = CalculatorForm()
    salary = None
    nssf = None
    taxable = None
    paye = None
    net = None
    if calculatorform.validate_on_submit():
        salary = calculatorform.salary.data
        # salary = float(input("Gross Salary? "))
        nssf = salary * 0.10
        taxable = salary - nssf

        paye = 0

        if taxable <= 270000:
            paye = 0
        elif taxable <= 520000:
            paye = (taxable - 270000) * 0.08
        elif taxable <= 760000:
            paye = 20000 + (taxable - 520000) * 0.20
        elif taxable <= 1000000:
            paye = 68000 + (taxable - 760000) * 0.25
        else:
            paye = 128000 + (taxable - 1000000) * 0.30

        net = salary - nssf - paye

    return render_template("calculator.html", calculatorform=calculatorform, taxable=taxable, nssf=nssf, paye=paye, net=net)

@app.route('/robots.txt')
def serve_robots():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'robots.txt')

@app.route('/sitemap.xml')
def serve_sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')


if __name__ == '__main__':
    app.run(debug=True)
