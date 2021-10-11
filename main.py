import requests
import sqlalchemy
import pandas as pd
import json
from datetime import datetime
import datetime
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import sqlite3
import requests
import pandas as pd
import pycountry


if __name__ == "__main__":
    DATABASE = 'sqlite:///calendar_holidays.sqlite'
    TABLE = 'holidays'
    TOKEN = 'ad945d10c64052e3a581c2ffda4c251762e6f56e'

    headers = {
        "Accept" : "application/json",
        "Content-Type": "application/json",
        "Authorization" : "Bearer %s"%(TOKEN)
    }

    YEAR = datetime.datetime.now().year

    for country in pycountry.countries:
        COUNTRY_CODE=country.alpha_2
        print(COUNTRY_CODE)
        API_KEY = f"https://calendarific.com/api/v2/holidays?api_key=ad945d10c64052e3a581c2ffda4c251762e6f56e&country={COUNTRY_CODE}&year={YEAR}"
        

        r = requests.get(API_KEY, headers=headers)
        
        data = r.json()
        print(data)
        holiday_name =[]
        description = []
        country_id=[]
        country_name =[]
        year = []
        month =[]
        day =[]
        try:
            for holiday in data['response']['holidays']:
                holiday_name.append(holiday['name'])
                description.append(holiday['description'])
                country_id.append(holiday['country']['id'].upper())
                country_name.append(holiday['country']['name'])
                year.append(holiday['date']['datetime']['year'])
                month.append(holiday['date']['datetime']['month'])
                day.append(holiday['date']['datetime']['day'])

            holidays_dict = {
                'Name':holiday_name,
                'Description':description,
                'Code': country_id,
                'Country Name' : country_name,
                'Year' : year,
                'Month' : month,
                'Day' : day
            }

            print(country_id)
            holidays_frame = pd.DataFrame(holidays_dict)
            engine = sqlalchemy.create_engine(DATABASE)

            if not database_exists(engine.url):
                create_database(engine.url)
            holidays_frame.to_sql(TABLE,engine, if_exists='append', index=False)
        except TypeError:
            pass