import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.address import AddressUrl

load_dotenv()


DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_PASS = os.getenv('DB_PASS')
DB_USER = os.getenv('DB_USER')
YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')
YANDEX_URL = os.getenv('YANDEX_URL')



DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
DB = sessionmaker(autocommit=False, autoflush=False, bind=engine)


if __name__ == '__main__':
    s = DB()
    data = s.query(AddressUrl).all()
    for i in data:
        print(i.point_id)

