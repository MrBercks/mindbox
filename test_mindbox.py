# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 18:13:31 2022

@author: user
"""

import pandas as pd

def add_sessions(df):
    """Метод принимает Pandas DataFrame и добавляет столбец session_id"""
    
    #проверка типа данных
    assert type(df) is pd.DataFrame, "некорректный тип данных"
    
    #проверка количества полей
    assert len(df.count()) == 3, "некорректное число полей"
    
    #перевод дат в формат datetime64[ns]
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    #сортировка DataFrame
    df.sort_values(by=["customer_id", "timestamp"], ascending=True, inplace=True)
    
    #расчет временных интервалов между посещениями
    timediff = [df.iloc[i]["timestamp"] - df.iloc[i-1]["timestamp"] for i in range(len(df))]
    
    #проверка посещений на 3-минутные интервалы
    new_sessions = []
    for i in range(len(df)):
        if timediff[i] < pd.to_timedelta(0):
            new_sessions.append("new")
        elif df.iloc[i]["customer_id"] != df.iloc[i-1]["customer_id"]:
            new_sessions.append("new")
        elif timediff[i] > pd.to_timedelta("00:03:00"):
            new_sessions.append("new")
        else:
            new_sessions.append("old")
    
    #индексация новых сессий
    session_id = []
    tmp_number = 0
    for i in range(len(df)):
        if new_sessions[i] == "new":
            tmp_number = tmp_number + 1
            session_id.append(tmp_number)
        else:
            session_id.append(tmp_number)
          
    #добавление session_id и возвращение порядка следования записей
    df["session_id"] = session_id
    df.sort_index(inplace=True)
    
    #df.to_csv("sessions2.csv", index=False) - проверял для теста, в программе не нужно
    
    return df