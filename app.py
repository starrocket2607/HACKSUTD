from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.externals import joblib
import numpy as np
import streamlit as st
import pickle


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    

    def __repr__(self):
        return '<Task %r>' % self.id


model=load_model('yield_predictions.h5')
scaler = joblib.load('scaler.save') 

def predict(Area,Rainfall,Temperature,pH,Nitrogen,ElectricalConductivity):
  a=np.array([[Area,Rainfall,Temperature,pH,Nitrogen,ElectricalConductivity]])
  a=scaler.transform(a)
  for i in abs(model.predict(a)):
    return np.math.floor(float(i))

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        Area = request.form['Area']
        Rainfall = request.form['Rainfall']
        Temperature = request.form['Temperature']
        ph = request.form['pH']
        Nitrogen = request.form['Nitrogen']
        ElectricalConductivity =request.form['ElectricalConductivity']
        crop_yield = predict(Area,Rainfall,Temperature,pH,Nitrogen,ElectricalConductivity)
#         task_content = request.form['content']
#         new_task = Todo(content=task_content)

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue adding your task'

    else:
#         tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('newindex.html', crop_yield=crop_yield)


if __name__ == "__main__":
    app.run(debug=True)
