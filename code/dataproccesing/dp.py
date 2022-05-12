import numpy as np
import torch
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader
import pandas_datareader as web
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


def get_data(ticker, start):
    data = web.DataReader(ticker, "yahoo", start, datetime.now())

    return data[["Close"]]


def split_data(ticker, start, lookback, test_ratio=0.2):
    data_raw = web.DataReader(ticker, "yahoo", start, datetime.now())
    data_raw = data_raw[["Close"]].values.reshape(-1, 1)
    scaler = MinMaxScaler()

    data_raw = scaler.fit_transform(data_raw)
    data = []

    # create all possible sequences of length seq_len
    for index in range(len(data_raw) - lookback):
        data.append(data_raw[index: index + lookback])

    data = np.array(data)
    test_set_size = int(np.round(test_ratio * data.shape[0]))
    train_set_size = data.shape[0] - test_set_size

    x_train = data[:train_set_size, :-1, :]
    y_train = data[:train_set_size, -1, :]

    x_test = data[train_set_size:, :-1]
    y_test = data[train_set_size:, -1, :]

    return [x_train, y_train, x_test, y_test]


def prepare_data(ticker, start, lookback):
    x_train, y_train, x_test, y_test = split_data(ticker, start, lookback)
    x_train = torch.from_numpy(x_train).type(torch.Tensor)
    x_test = torch.from_numpy(x_test).type(torch.Tensor)
    y_train_gru = torch.from_numpy(y_train).type(torch.Tensor)
    y_test_gru = torch.from_numpy(y_test).type(torch.Tensor)
    return x_train.reshape(-1, lookback -1 ), x_test.reshape(-1, lookback-1), y_train_gru.reshape(-1, 1), y_test_gru.reshape(-1, 1)


def get_dataloaders(ticker, start, lookback, batch_size):
    x_train, x_test, y_train_gru, y_test_gru = prepare_data(ticker, start, lookback)
    train_ds = TensorDataset(x_train, y_train_gru)
    train_dl = DataLoader(train_ds, shuffle=False)
    test_ds = TensorDataset(x_test, y_test_gru)
    test_dl = DataLoader(test_ds, shuffle=False)
    return train_dl, test_dl
