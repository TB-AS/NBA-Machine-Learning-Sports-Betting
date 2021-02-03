import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from tqdm import tqdm

data = pd.DataFrame(pd.read_excel('../../Datasets/More_Data_2021.xlsx'))
margin = data['Home-Team-Win']
data.drop(['Score', 'Home-Team-Win', 'Unnamed: 0', 'TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1', 'OU-Cover', 'OU'],
          axis=1, inplace=True)
print(data.columns.values)
data = data.values

data = data.astype(float)

print(data)

for x in tqdm(range(250)):
    x_train, x_test, y_train, y_test = train_test_split(data, margin, test_size=.1)

    train = xgb.DMatrix(x_train, label=y_train)
    test = xgb.DMatrix(x_test, label=y_test)

    param = {
        'max_depth': 7,
        'eta': 0.1,
        'objective': 'multi:softmax',
        'num_class': 2
    }
    epochs = 250

    model = xgb.train(param, train, epochs)

    predictions = model.predict(test)

    acc = round(accuracy_score(y_test, predictions), 3) * 100
    print(acc)
    model.save_model('../../Models/XGBoost_{}%_ML.json'.format(acc))
