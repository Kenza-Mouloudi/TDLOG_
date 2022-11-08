from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:////tmp/tdlog.db', echo=True, future=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


class GameEntity(Base):
 __tablename__ = 'game'
 id = Column(Integer, primary_key=True)
 players = relationship("PlayerEntity", back_populates="game",
 cascade="all, delete-orphan")


class PlayerEntity(Base):
 __tablename__ = 'player'
 id = Column(Integer, primary_key=True)
 name = Column(String, nullable=False)
 game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
 game = relationship("GameEntity", back_populates="players")
 battle_field = relationship("BattlefieldEntity",
 back_populates="player",
 uselist=False, cascade="all, delete-orphan")

 class BattlefieldEntity(Base):
 __tablename__ = 'battlefield'
 id = Column(Integer, primary_key=True)
 min_x = Column(Integer)
 min_y = Column(Integer)
 min_z = Column(Integer)
 max_x = Column(Integer)
 max_y = Column(Integer)
 max_z = Column(Integer)
 max_power = Column(Integer)
 player = relationship("PlayerEntity", back_populates="battle_field",
          uselist=False)
 player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
 battle_field = relationship("BattlefieldEntity",
 back_populates="player",
 uselist=False, cascade="all, delete-orphan")

