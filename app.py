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

def crop_prediction(n,p,k,temp,humidity,ph,rainfall):
  a=np.array([[n,p,k,temp,humidity,ph,rainfall]])
  a=scaler.transform(a)
  predict_x=np.argmin(model.predict(a,verbose=0,batch_size=None,steps=None),axis=1)


  c=None

  for i in predict_x:
    c=i

  return mapping[c]

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        n = request.form['n']
        p = request.form['p']
        k = request.form['k']
        temp = request.form['temp']
        humidity = request.form['humidity']
        ph = request.form['pH']
        rainfall = request.form['rainfall']
        crop_yield = crop_prediction(n,p,k,temp,humidity,ph,rainfall)

    else:
        return render_template('newindex.html', crop_yield=crop_yield)


if __name__ == "__main__":
    app.run(debug=True)
