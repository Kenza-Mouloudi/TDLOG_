import numpy as np
from sqlalchemy import create_engine, select
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

Base.metadata.create_all()

class GameDao:
    def __init__(self):
        Base.metadata.create_all()
        self.db_session = Session()
    def map_to_game_entity(self,game:Game):
        game_entity = GameEntity()
        game_entity.id = game.id
        game_entity.player = game.players
        return game_entity
    def map_to_game(self, game_entity:GameEntity):
        id =game_entity.id
        game = Game(id)
        return game

    def map_to_game_entity(self,game: Game) -> GameEntity:
        game_entity = GameEntity(id=game.id)
        game_entity.players = [self.map_to_player_entity(player) for player in game.players]
        return game_entity

    def map_to_player_entity(self, player: Player) -> PlayerEntity:
        player_entity = PlayerEntity(id=player.id, name=player.name, game_id=player.game.id)
        player_entity.battle_field = self.map_to_battlefield_entity(player.battle_field, player_entity.id)
        return player_entity

    def map_to_battlefield_entity(self, battlefield: Battlefield, player_id: int) -> BattlefieldEntity:
        battlefield_entity = BattlefieldEntity(id=battlefield.id,
                                               min_x=battlefield.min_x,
                                               min_y=battlefield.min_y,
                                               min_z=battlefield.min_z,
                                               max_x=battlefield.max_x,
                                               max_y=battlefield.max_y,
                                               max_z=battlefield.max_z,
                                               max_power=battlefield.max_power,
                                               player_id=player_id)
        battlefield_entity.vessels = [self.map_to_vessel_entity(vessel, battlefield_entity.id) for vessel in
                                      battlefield.vessels]
        return battlefield_entity

    def map_to_vessel_entity(self, vessel: Vessel, battlefield_id: int) -> VesselEntity:
        vessel_entity = VesselEntity(id=vessel.id,
                                     coord_x=vessel.coord_x,
                                     coord_y=vessel.coord_y,
                                     coord_z=vessel.coord_z,
                                     hots_to_be_destroyed=vessel.hots_to_be_destroyed,
                                     type=vessel.type,
                                     battle_field_id=battlefield_id)
        vessel_entity.weapon = self.map_to_weapon_entity(vessel.weapon, vessel_entity.id)
        return vessel_entity

    def map_to_weapon_entity(self, weapon: Weapon, vessel_id: int) -> WeaponEntity:
        weapon_entity = WeaponEntity(id=weapon.id,
                                     ammunitions=weapon.ammunitions,
                                     range=weapon.range,
                                     type=weapon.type,
                                     vessel_id=vessel_id)
        return weapon_entity

    def create_game(self, game: game) :
        game_entity = self.map_to_game_entity(game)
        self.db_session.add(game_entity)
        self.db_session.commit()
        return game_entity.id
    def find_game(self, game_id: int):
        stmt = select(GameEntity).where(GameEntity.id == game_id)
        game_entity = self.db_session.scalars(stmt).one()
        return self.map_to_game(game_entity)
    






