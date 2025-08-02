from sqlalchemy import engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

mysql_url = "mysql+pymysql://root:232918@192.168.113.100:3306/todolist"

engine = engine.create_engine(mysql_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
