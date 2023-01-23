import requests, json, threading, bs4
import sqlalchemy
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import INTEGER, Text, Column

Base = declarative_base()

engine = sqlalchemy.create_engine('sqlite:///famous_people.db')
connection = engine.connect()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
session = Session(engine)

class famous_people(Base):
    __tablename__ = 'Famous People'

    id = Column(INTEGER, primary_key=True, autoincrement = True)
    profession = Column(Text)
    name = Column(Text)
    born = Column(Text)
    birthplace = Column(Text)
    died = Column(Text)
    description = Column(Text)

def strip_str(str:str):
    return str.split('>')[1].split('<')[0].strip()

def fill_tables(page, profession):
    soup = bs4.BeautifulSoup(page.text, 'html.parser')

    res = soup.find_all('article', {'class':'feature'})
    for el in res:
        with session as db:
            _temp = famous_people()

            profession_info = profession
            _temp.profession = profession_info

            name = el.findChild('div', {'class':'ptitle-internal'}).findChild('a').string
            _temp.name = name

            main_info = el.findChild('div', {'class':'rt-text-display'}).findChildren('div', {'class':'desc-q'})
            birthdate = main_info[0].contents[1]
            _temp.born = birthdate

            if len(main_info) == 2:
                birthplace = None
            else:
                birthplace = main_info[2].contents[1]
            _temp.birthplace = birthplace

            if len(main_info) == 4:
                deathdate = main_info[3].contents[1]
            else:
                deathdate = None
            _temp.died = deathdate
            
            short_desc = el.findChild('div', {'class':'rt-text-display'}).findChild('div', {'class':'descEvent'})
            if len(short_desc.contents) == 0:
                _temp.description = None
            else:
                short_desc_text = short_desc.findChild('p')
                if short_desc_text is None:
                    short_desc_text = short_desc.contents
                else:
                    short_desc_text = short_desc_text.contents
                for i in range(len(short_desc_text)):
                    if not isinstance(short_desc_text[i], str):
                        short_desc_text[i] = str(short_desc_text[i])
                        short_desc_text[i] = strip_str(short_desc_text[i])
                desc = ' '.join(short_desc_text)
                _temp.description = desc
            
            db.add(_temp)
            db.commit()

URL = ['https://www.thefamouspeople.com/21st-century-writers.php', 'https://www.thefamouspeople.com/21st-century-physicists.php', 'https://www.thefamouspeople.com/football-players.php']
professions = ['writer', 'physicist', 'football player']

def create_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    for url, prof in list(zip(URL, professions)):
        page = requests.get(url)
        if page.status_code != 200:
            print('Network error')
            break
        fill_tables(page, prof)

def get_data_by_profession(profession:str):
    with session as db:
        res = db.query(famous_people).filter(famous_people.profession == profession).all()
        return res

def get_person_info(person):
    info = []
    name = f'*Name*: {person.name}'
    date_born = f'*Born*: {person.born}'
    info.append(name)
    info.append(date_born)

    if person.birthplace:
        birthplace = f'*Birthplace*: {person.birthplace}'
        info.append(birthplace)
    
    if person.died:
        date_died = f'*Died*: {person.died}'
        info.append(date_died)

    if person.description:
        desc = f'*Description*: {person.description}'
        info.append(desc)
    
    res_info = '\n'.join(info)
    return res_info

if __name__ == '__main__':
    for url, prof in list(zip(URL, professions)):
        page = requests.get(url)
        if page.status_code != 200:
            print('Network error')
            break
        fill_tables(page, prof)