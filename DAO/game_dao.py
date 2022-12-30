import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from model.air_missile_launcher import AirMissileLauncher
from model.battlefield import Battlefield
from model.cruiser import Cruiser
from model.destroyer import Destroyer
from model.frigate import Frigate
from model.game import Game
from model.player import Player
from model.submarine import Submarine
from model.surface_missile_launcher import SurfaceMissileLauncher
from model.toredos_launcher import TorpedoLauncher
from model.vessel import Vessel
from model.weapon import Weapon
engine = create_engine('sqlite:////tmp/tdlog.db', echo=True, future=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

class GameDao:
 def _init_(self):
 Base.metadata.create_all()
 self.db_session = Session()

 def create_game(self, game: Game) -> int:
 game_entity = map_to_game_entity(game)
 self.db_session.add(game_entity)
 self.db_session.commit()
 return game_entity.id

 def find_game(self, game_id: int) -> Game:
 stmt = select(GameEntity).where(GameEntity.id == game_id)
 game_entity = self.db_session.scalars(stmt).one()
 return map_to_game(game_entity)one()

 def create_or_update_player(self, game_id: int, player: Player) -> bool:
  stmt = select(GameEntity).where(GameEntity.id == game_id)
  game_entity = self.db_session.scolars(start).one()
  for player_entity in game_entity.player:
   if player_entity.name=player.name:
    game_entity.player.remove(player_entity)
    break
  game_entity.player.append(map_to_player_entity(player))
  self.db_session.flush()
  self.db_session.comit()
  return True


def create_or_update_vessel(self, game_id: int, player: Player) -> bool:
 stmt_find_player = select(PlayerEntity).where(PlayerEntity.id == player_id)
 player_entity = self.db_session.scolars(start).one()
 vessel_entity_updated = map_to_vessel_entity(player.get_battlefield().id, vessel)

 for vessel_entity in player_entity.battle_field.vessels:
  if vessel_entity.id= vessel_entity_updated.id:
   player_entity.battle_field.vessel.remove(vessel_entity)
   break
 player_entity.battle_field.vessel.append(vessel_entity_updated)

 self.db_session.flush()
 self.db_session.comit()
 return True


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
 vessels = relationship("VesselEntity", back_populates="battlefield",
                        cascade="all, delete-orphan")
 class VesselEntity(Base):
  __tablename__ = 'vessel'
  id = Column(Integer, primary_key=True)
  coord_x = Column(Integer)
  coord_y = Column(Integer)
  coord_z = Column(Integer)
  hits_to_be_destroyed = Column(Integer)
  type = Column(String)
  battle_field = relationship("BattlefieldEntity",back_populates="vessels")
  battle_field_id = Column(Integer, ForeignKey("battlefield.id"),
                           nullable=False)
  weapon = relationship("WeaponEntity", back_populates="vessels",
                        uselist=Flase, cascade="all, delete-orphan")

  class WeaponEntity(Base):
   tablename = 'weapon'
   id = Column(Integer, primary_key=True)
   ammunitions = Column(Integer)
   range = Column(Integer)
   type = Column(String)
   vessel = relationship("VesselEntity", back_populates="weapon")
   vessel_id = Column(Intger, ForeinKey("vessel.id"), nullable=False)

  class VesselTypes:
         CRUISER = "Cruiser"
         DESTROYER = "Destroyer"
         FRIGATE = "Frigate"
         SUBMARINE = "Submarine"


  class WeaponsTypes:
         AIRMISSILELAUnCHER = "AirMissileLauncher"
         SurfaceMISSILELAUnCHER = "SurfaceMissileLauncher"
         TORPEDOLAUnCHER = "TorpedoLauncher"

  def map_to_game_entity(game: Game) -> GameEntity:
   game_entity = GameEntity()
   if game.get_id() is not None:
    game_entity.id = game.get_id():
    for player in game.get_player():
     player_entity = PlayerEntity()
     player_entity.id = player.id
     player_entity.name = player.get_name()
     Battlefield_entity = map_to_battlefield_entity(player.get_battlefield())
     vessel_entity = \
      map_to_vessel_entity(player.get_battlefield().id,
                           player.get_battlefield().vessels)
     battlefield_entity.vessels = vessel_entity
     player_entity.battle_field = battlefield_entity
     game_entity.players.append(player_entity)
    










