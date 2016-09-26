#!/usr/bin/env python
#coding:utf-8
"""


"""
import os

from sqlalchemy import Column,create_engine,String,Text,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship

from config import baseDir

engine = create_engine('sqlite:///'+os.path.join(baseDir,'data-dev.db'))
Base = declarative_base()

DBsession = sessionmaker(bind=engine)
session = DBsession()

class Platform(Base):
    __tablename__ = 'platform'

    id = Column(String(48),primary_key=True)
    name = Column(String(48))
    gradeFromThird = Column(String(48))
    profitAverage = Column(String(48))
    dateSale = Column(String(48))
    registeredCapital = Column(String(48))
    area = Column(String(48))
    url = Column(String(48))
    startMoney = Column(String(48))
    managementFee = Column(String(48))
    cashTakingFee = Column(String(48))
    backGround = Column(String(48))
    provisionOfRisk = Column(String(48))
    foundCustodian = Column(String(48))
    safeguardWay = Column(String(48))
    assignmentOfDebt = Column(String(48))
    automaticBidding = Column(String(48))
    cashTime = Column(String(48))
    abstract = Column(Text)
    persons = relationship('Person',backref='platform')

class Person(Base):
    __tablename__='person'

    id = Column(String(48),primary_key=True)
    abstracts = Column(Text)
    platform_id = Column(String(48),ForeignKey('platform.id'))
    
class Product(Base):
    __tablename__ = 'product'

    id = Column(String(48),primary_key=True)
    name = Column(String(48))
    annualizedReturn = Column(String(48)) #年化收益率
    cycle = Column(String(48)) #投资周期
    remainAmount = Column(String(48)) #剩余额度
    platform_id = Column(String(48),ForeignKey('platform.id'))

def init_db():
    pass
    Base.metadata.create_all(engine)
def drop_db():
    pass
    Base.metadata.drop_all(engine)

if __name__ == '__main__':
    pass
    drop_db()
    init_db()
