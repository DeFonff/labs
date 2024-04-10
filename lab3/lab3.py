from spyre import server
import pandas as pd
import os
import matplotlib.pyplot as plt
class Mysite(server.App):
    title = "NOAA DATA VIZUALIZATION"
    inputs = [
        {
            "type": "dropdown",
            "label": "NOAA data dropdown",
            "options": [{"label": "VHI", "value": "VHI"},
                         {"label": "TCI", "value": "TCI"},
                         {"label": "VCI", "value": "VCI"}
                         ],
            "key": "ticker",
            "action_id": "update_data"
        },
                {
            "type": "dropdown",
            "label": "Region",
            "options": [{"label": "Вінницька", "value": "Вінницька"},
                         {"label": "Волинська", "value": "Волинська"},
                         {"label": "Дніпропетровська", "value": "Дніпропетровська"},
                         {"label": "Донецька", "value": "Донецька"},
                         {"label": "Житомирська", "value": "Житомирська"},
                         {"label": "Закарпатська", "value": "Закарпатська"},
                         {"label": "Запорізька", "value": "Запорізька"},
                         {"label": "Івано-Франківська", "value": "Івано-Франківська"},
                         {"label": "Київська", "value": "Київська"},
                         {"label": "Кіровоградська", "value": "Кіровоградська"},
                         {"label": "Луганська", "value": "Луганська"},
                         {"label": "Львівська", "value": "Львівська"},
                         {"label": "Миколаївська", "value": "Миколаївська"},
                         {"label": "Одеська", "value": "Одеська"},
                         {"label": "Полтавська", "value": "Полтавська"},
                         {"label": "Рівенська", "value": "Рівенська"},
                         {"label": "Сумська", "value": "Сумська"},
                         {"label": "Тернопільська", "value": "Тернопільська"},
                         {"label": "Харківська", "value": "Харківська"},
                         {"label": "Херсонська", "value": "Херсонська"},
                         {"label": "Хмельницька", "value": "Хмельницька"},
                         {"label": "Черкаська", "value": "Черкаська"},
                         {"label": "Чернівецька", "value": "Чернівецька"},
                         {"label": "Чернігівська", "value": "Чернігівська"},
                         {"label": "Республіка Крим", "value": "Республіка Крим"}
                         ],
            "key": "region",
            "action_id": "update_data"
        },
        {
            "type":"text",
            "label":"range for weeks (1 - 52)",
            "key":"range",
            "value":"9-10",
            "action_id":"getweeks"
        },
        {
            "type": "slider",
            "key": "year",
            "label": "Years",
            "value": 2000,
            "min": 1982,
            "max": 2024,
            "action_id": "update_data"
        }
    ]

    controls = [
        {
            "type": "button",
            "label": "update",
            "id": "button_id",
            "action_id": "update_data"
        }
    ]

    outputs = [
        { 
            "type" : "plot",
            "id" : "plot",
            "control_id" : "button_id",
            "tab" : "Plot"
        },
        { 
            "type" : "table",
            "id" : "table_id",
            "control_id" : "button_id",
            "tab" : "Table",
            "on_page_load" : True
        }]

    tabs = ["Plot", "Table"]

    def getweeks(self, params):
        rang = params["range"]
        weeks = rang.split("-")
        start, end = int(weeks[0]), int(weeks[1])
        return start, end

    def getData(self, params):
        file_list = os.listdir('C:/Users/dddddd/Desktop/ad/lab3/data')
        file_list = sorted(file_list, key=lambda filename: int(filename.split("_")[1]))
        headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'index']
        df = pd.DataFrame(columns=headers)
        index = 1              
        for i in file_list:
            temp_df = pd.read_csv(os.path.join('C:/Users/dddddd/Desktop/ad/lab3/data', i), header=1, names=headers)
            temp_df.fillna({"index":index}, inplace=True)
            df = pd.concat([df, temp_df], ignore_index=True)
            index += 1
        indexs = {1:'Черкаська', 2:'Чернігівська', 3:'Чернівецька', 4:'Республіка Крим', 5:'Дніпропетровська', 6:'Донецька', 7:'Івано-Франківська', 8:'Харківська', 9:'Херсонська', 10:'Хмельницька', 11:'Київська', 12:'Кіровоградська', 13:'Луганська', 14:'Львівська', 15:'Миколаївська', 16:'Одеська', 17:'Полтавська', 18:'Рівенська', 19:'Сумська', 20:'Тернопільська', 21:'Закарпатська', 22:'Вінницька', 23:'Волинська', 24:'Запорізька', 25:'Житомирська'}
        df["index"].replace(indexs, inplace=True)
        start, end = self.getweeks(params)
        df = df[(df["index"]==params['region'])&(df["Week"]>=start)&(df["Week"]<=end)&(df["Year"]==params["year"])]
        return df[['index', 'Week', 'Year', params["ticker"]]]


    def getPlot(self, params):
        x1, x2 = self.getweeks(params)
        x_values = range(x1, x2+1)
        df = self.getData(params)
        y_values_1 = df[params["ticker"]].tolist() 
        plt_obj = plt.figure() 
        plt.grid(True, linestyle='--', color='gray')
        plt.plot(x_values, y_values_1, marker='.', label=params["ticker"])
        plt.xlabel("Неділі")
        plt.ylabel(params["ticker"])
        i = params["ticker"]
        plt.title(f"{i} for week")
        plt.legend()
        return plt_obj

app = Mysite()
app.launch(port=9090)
