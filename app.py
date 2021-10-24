"""
Anitech

pip3 install -r requirements.txt

requirements.txt
 - pip freeze > requirements.txt

"""

#Import libraries
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, FloatField
from wtforms.fields.html5 import DateField, TimeField

from wtforms.validators import InputRequired, Length, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

#import plotly.express as px
#import pandas as pd
#import json
#import plotly
#--------------------------------------------------------------------------------------------------------------------------------------------
app = Flask(__name__) # Start of Flask App
bootstrap = Bootstrap(app) # For WTForms
app.config['SECRET_KEY'] = 'temporarykey123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Ignore Warning message
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3' # db Will show up in this directory
db = SQLAlchemy(app) # Initialize SQLAlchemy app

# RQ Values Database 7 Columns
class Rq_table(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary key RQ 1
    date = db.Column(db.DateTime)                # Input Date 2
    co2x = db.Column(db.Float)                   # CO2 Value 3
    o2xx = db.Column(db.Float)                   # O2 Value 4
    temp = db.Column(db.Float)                   # Environmental Temperature 5
    humi = db.Column(db.Float)                   # Environmental Humidity 6
    boxx = db.Column(db.String(20))              # Sensor Number 7

# Inbound Database 12 Columns
class Inbound(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary key INBOUND 1
    buy_date = db.Column(db.DateTime)            # Buy Date and Time 2
    supplier = db.Column(db.String(30))          # Supplier Name 3
    produce = db.Column(db.String(20))           # What Kind of Produce 4
    prod_typ = db.Column(db.String(20))          # What Type of Said Produce 5
    buyprice = db.Column(db.Float)               # Buy price from supplier 6
    kilos = db.Column(db.Float)                  # Weight in Kilos from supplier 7
    comments = db.Column(db.String(50))          # Comments of the produce 8
    tryx = db.Column(db.String(3))               # Trial Value? 9
    person = db.Column(db.String(20))            # Person In Charge 10
    measure = db.Column(db.String(3))            # To be Measured? 11
    sensor = db.Column(db.String(20))            # Sensor Number 12

# Outbound Database 10 Columns
class Outbound(db.Model):
    id = db.Column(db.Integer, primary_key=True)# primary key Outbound 1
    sale_date = db.Column(db.DateTime)          # Sale Date 2
    customer = db.Column(db.String(30))         # Customer Name 3
    produce = db.Column(db.String(20))          # What Kind of Produce 4
    prod_typ = db.Column(db.String(20))         # What Type of Said Produce 5
    sellprice = db.Column(db.Float)             # Price to customer 6
    kilos = db.Column(db.Float)                 # Weight in Kilos to Customer 7
    comments = db.Column(db.String(50))         # Comments of the produce 8
    person = db.Column(db.String(20))           # Person In Charge 9
    tryx = db.Column(db.String(3))              # Trial Value? 10

"""
Initialize in Terminal with Python to make the User db above

>>> from app import db
>>> db.create_all()

"""
# Forms =========================================================================================================
class InboundForm(FlaskForm):
    buy_date = DateField('Date of Purchase', format='%Y-%m-%d')
    buy_time = TimeField('Time', format='%H:%M')
    supplier = StringField('Supplier', validators=[InputRequired(), Length(min=2, max=30)])
    produce = StringField('Produce', validators=[InputRequired(), Length(min=2, max=20)])
    prod_typ = StringField('Type of Produce', validators=[InputRequired(), Length(min=2, max=20)])
    buyprice = FloatField('Buy Price', validators=[InputRequired()])
    kilos = FloatField('Kilos', validators=[InputRequired()])
    comments = StringField('Comments', validators=[InputRequired(), Length(min=2, max=30)])
    tryx = SelectField('Trial?', choices = [('Yes', 'Yes'), ('No', 'No')], validators = [InputRequired()])
    person = SelectField('Person in Charge', choices = [('Emp_1', 'Employee 1'), ('Emp_2', 'Employee 2')], validators = [InputRequired()])
    measure = SelectField('To Measure?', choices = [('No', 'No'), ('Yes', 'Yes') ], validators = [InputRequired()])
    sensor = SelectField('Sensor Number', choices = [(None, ''), ('PHMS_1', 'PHMS_1'), ('PHMS_2', 'PHMS_2'), ('PHMS_3', 'PHMS_3')])


class OutboundForm(FlaskForm):
    sale_date = DateField('Date of Purchase', format='%Y-%m-%d')
    sale_time = TimeField('Time', format='%H:%M')
    customer = StringField('Customer', validators=[InputRequired(), Length(min=2, max=30)])
    produce = StringField('Produce', validators=[InputRequired(), Length(min=2, max=20)])
    prod_typ = StringField('Type of Produce', validators=[InputRequired(), Length(min=2, max=30)])
    sellprice = FloatField('Sell Price', validators=[InputRequired()])
    kilos = FloatField('Kilos', validators=[InputRequired()])
    comments = StringField('Comments', validators=[InputRequired(), Length(min=2, max=30)])
    tryx = SelectField('Trial?', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    person = SelectField('Person in Charge', choices = [('Emp_1', 'Employee 1'), ('Emp_2', 'Employee 2')], validators = [InputRequired()])

# =========================================================================================================
# Connecting to www.website.com/home
@app.route("/home", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def index():
    """
       Stock Management Dashboard

       :return:
       """
    return render_template('home.html')

@app.route('/maturity', methods=['GET', 'POST'])
def maturity():
    """
    Maturity Dashboard
    :return:
    """
    data = Rq_table.query.order_by(Rq_table.id.desc()).limit(20)
    return render_template('maturity.html', data=data)

@app.route('/inbound', methods=['GET', 'POST'])
def inbound():
    form = InboundForm()
    if form.validate_on_submit():
        record = Inbound(buy_date=datetime.datetime.combine(form.buy_date.data,form.buy_time.data),
                        supplier=form.supplier.data,
                        produce=form.produce.data,
                        prod_typ=form.prod_typ.data,
                        buyprice=form.buyprice.data,
                        kilos=form.kilos.data,
                        comments=form.comments.data,
                        tryx=form.tryx.data,
                        person=form.person.data,
                        measure=form.measure.data,
                        sensor=form.sensor.data,
                       )
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('inbound'))
    data = Inbound.query.order_by(Inbound.id.desc()).limit(5)
    return render_template('inbound.html', form=form, data=data)

@app.route('/outbound', methods=['GET', 'POST'])
def outbound():
    form = OutboundForm()
    if form.validate_on_submit():
        record = Outbound(sale_date=datetime.datetime.combine(form.sale_date.data,form.sale_time.data),
                          customer=form.customer.data,
                          produce=form.produce.data,
                          prod_typ=form.prod_typ.data,
                          sellprice=form.sellprice.data,
                          kilos=form.kilos.data,
                          comments=form.comments.data,
                          tryx=form.tryx.data,
                          person=form.person.data
                       )
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('outbound'))
    data = Outbound.query.order_by(Outbound.id.desc()).limit(5)
    return render_template('outbound.html', form=form, data=data)

# ================================================================================================================================================================================================
# End of Flask App
if __name__ == "__main__":
#    app.run(host='0.0.0.0')
   app.run(debug=True)
