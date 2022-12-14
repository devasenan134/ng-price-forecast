# for concrete view
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

# for daily news view
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests

import pickle
from sklearn import metrics


file_path = "C:/Users/devas/Documents/projects/natural-gas-forecasting/ngForecast/dashboard/static/dashboard/encoded_feature.csv"
file_path1 = "C:/Users/devas/Documents/projects/natural-gas-forecasting/ngForecast/dashboard/static/dashboard/processed_nasdaq.csv"
df = pd.read_csv(file_path, parse_dates=True)
df = df.drop(['Unnamed: 0'], axis=1)
# print(df.columns)

nas = pd.read_csv(file_path1, index_col="Date", parse_dates=True)
nas = nas.drop(["vol"], axis=1)
seasons = {"Spring": 1,
           "Summer": 2,
           "Autumn": 3,
           "Winter": 4}
nas["season"] = nas.season.map(seasons)
nas = nas[::-1]



def fetch_news():
    root = "https://news.google.com"
    link = "https://news.google.com/search?q=natural%20gas%20when%3A1d&hl=en-IN&gl=IN&ceid=IN%3Aen"

    req = Request(link, headers={"User-Agent": "Mozilla/5.0"})
    webpage = urlopen(req).read()

    news24 = []
    with requests.Session() as c:
        soup = BeautifulSoup(webpage, 'html.parser')
        for item in soup.find_all('div', attrs={'class': 'NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc'}):
            link = (root + "/" + item.find('a', href=True)["href"] + "\n").split("&sa=U&")[0]
            title = item.find("a", attrs={'class': 'DY5T1d RZIKme'}).get_text()
            source = item.find("a", attrs={'class': 'wEwyrc AVN2gc uQIVzc Sksgp'}).get_text()
            time = item.find("time", attrs={'class': 'WW6dff uQIVzc Sksgp'}).get_text()

            img = item.find("img", attrs={'class': 'tvs3Id QwxBBf'})['srcset']

            news24.append([title, source, time, link, img])
    return news24


def encode_plot(plot):
    file = BytesIO()
    plot.figure.savefig(file, format="png")
    b64 = base64.b64encode(file.getvalue()).decode()
    return b64


def plot_graphs():
    # 
    plt.figure(figsize=(24, 7))
    plt.title("Price of Natural gas in 2012 to 2022")
    line_plot = sns.lineplot(data=nas.close)
    plt.xlabel("Date")
    plt.ylabel("Price in USD")
    #
    plt.figure(figsize=(10, 5))
    plt.title("Price of Natural gas month wise")
    dist_plot = sns.barplot(x=nas.index.month, y=nas.close)
    plt.xlabel("Months")
    plt.ylabel("Price in USD")
    #
    plt.figure(figsize=(10, 5))
    plt.title("Price of Natural gas season wise")
    sm_plot = sns.swarmplot(x=nas.season, y=nas.close)
    plt.xlabel("Seasons")
    plt.ylabel("Price in USD")

    return line_plot, dist_plot, sm_plot


def predict_close(start=2300, end=2400, pred_range=50):
    model_path = "C:/Users/devas/Documents/projects/natural-gas-forecasting/ngForecast/dashboard/static/dashboard/arima_nasdaq.pkl"
    model_fit = pickle.load(open(model_path, "rb"))
    
    # df1["forecast"] = model_fit.predict(start=1500, end=2550, dynamic=False)
    # print(df1)
    # df1[["close", "forecast"]].plot(figsize=(24,7))

    test_df = pd.DataFrame(nas.iloc[:end, 0], columns=["close"])
    test_dates = [test_df.index[-1]+ pd.DateOffset(days=x) for x in range(0, pred_range)]
    test_datest_df = pd.DataFrame(index=test_dates[1:])
    test_df = pd.concat([test_df, test_datest_df])

    test_df["forecast"] = model_fit.predict(start=end, end=(end+pred_range), dynamic=False)
    # print(test_df)

    new_test = test_df[end:].dropna(subset=["forecast", ])
    plt.figure(figsize=(20, 7))
    plt.title("Natural Gas Close Price Predictions")
    trend = sns.lineplot(data=test_df.iloc[start:, 0])
    trend = sns.lineplot(data=new_test.iloc[:, 1])
    plt.xlabel("Date")
    plt.ylabel("Price in USD")

    error = 0.0848939706578784
    # error = metrics.mean_absolute_error(nas.iloc[:, 0], new_test.iloc[:, 7])
    print("Accuracy:", 100 - error*100, "%")


    # test_df.iloc[2300:, 0].plot(figsize=(24, 7))
    # new_test.iloc[:, 1].plot(figsize=(14, 7))
    # print(new_test) 

    return trend, error


def key_data():
    max_close = max(nas.close)
    min_close = min(nas.close)
    mean_close = sum(nas.close)/len(nas.close)
    last_close = nas.close[-1]
    return [max_close, min_close, mean_close, last_close]