from flask import Flask, render_template, request
import pickle
import numpy as np

from sklearn.preprocessing import StandardScaler

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application
# Home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')



# Prediction route
@app.route('/predictdata', methods=['GET','POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        # getting and defining data
        data = CustomData(
            gender = request.form['gender'],
            race_ethnicity = request.form['ethnicity'],
            parental_level_of_education = request.form['parental_level_of_education'],
            lunch = request.form['lunch'],
            test_preparation_course = request.form['test_preparation_course'],
            writing_score = int(request.form['writing_score']),
            reading_score = int(request.form['reading_score']),
        )
        # converting to df
        pred_df = data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        predict_pipeline.predict(pred_df)
        results=predict_pipeline.predict(pred_df)
    return render_template('home.html', results=results[0])

if __name__ == "__main__":
    app.run(debug=True)
