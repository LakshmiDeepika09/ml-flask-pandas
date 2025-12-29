import pandas as pd
from sklearn.linear_model import LinearRegression

def train_and_predict(csv_path, exp):
    df = pd.read_csv(csv_path)

    X = df[['experience']]
    y = df['salary']

    model = LinearRegression()
    model.fit(X, y)

    prediction = model.predict([[exp]])
    return round(prediction[0], 2), X, y, model