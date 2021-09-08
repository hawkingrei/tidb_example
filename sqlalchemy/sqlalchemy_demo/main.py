from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import enum
engine = create_engine(
    'tidb://root:@127.0.0.1:4000/test_sqlalchemy?charset=utf8mb4',
    echo=True)

# The base class which our objects will be defined on.
Base = declarative_base()


class Gender(enum.Enum):
    Female = 1
    Male = 2


class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    name = Column(String(50))
    gender = Column(Enum(Gender))

    def __repr__(self):
        return "<User(name='%s', gender='%s')>" % (
            self.name, self.gender)


class Order(Base):
    __tablename__ = 'orders'

    # Every SQLAlchemy table should have a primary key named 'id'
    oid = Column(Integer, primary_key=True, autoincrement=True)

    uid = Column(Integer)
    price = Column(Float)

    # Lets us print out a user object conveniently.
    def __repr__(self):
        return "<User(oid='%d', uid='%d', price'%f')>" % (
            self.name, self.uid, self.price)


# Create all tables by issuing CREATE TABLE commands to the DB.
Base.metadata.create_all(engine)

# Creates a new session to the database by using the engine we described.
Session = sessionmaker(bind=engine)
session = Session()

# insert users into the database
session.add_all([
    User(name='Alice', gender=Gender.Female),
    User(name='Peter', gender=Gender.Male),
    User(name='Ben', gender=Gender.Male),
])
session.commit()

# insert Order into the database
ed_user = Order(uid=1, price=2.5)

# Let's add the user we've created to the DB and commit.
session.add(ed_user)
session.commit()

# insert Orders into the database
session.add_all([
    Order(uid=1, price=0.5),
    Order(uid=2, price=4.5),
    Order(uid=2, price=2123.87),
    Order(uid=3, price=212.5),
    Order(uid=3, price=8.5),
]
)
session.commit()

# delete order by oid
session.query(Order).filter(Order.oid == 4).delete()
session.commit()

# update order
session.query(Order).filter(Order.oid == 1).update({'price': 3.5})
session.commit()

# join order and user
print(
    session.query(User.name, Order.price)
    .select_from(User)
    .filter(User.uid == Order.uid)
    .filter(Order.uid == 3)
    .all()
)
