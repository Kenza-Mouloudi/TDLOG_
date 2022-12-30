from game_dao import GameDao
from bataillenavalemain1.bataillenavalemain2.battlefield import Battlefield
from bataillenavalemain1.bataillenavalemain2.vessel import Vessel
from game_dao import Player
from game_dao import Game
class GameService:
 def __init__(self):
     self.game_dao = GameDao()
 def create_game(self, player_name: str, min_x: int, max_x: int, min_y: int,
     max_y: int, min_z: int, max_z: int) -> int:
     game = Game()
     battle_field = Battlefield(min_x, max_x, min_y, max_y, min_z, max_z)
     game.add_player(Player(player_name, battle_field))
     return self.game_dao.create_game(game)

 def join_game(self, game_id: int, player_name: str) -> bool:
     game = self.game_dao.find_game(game_id)
     if not game:
         return False
     if len(game.players) >= 2:
         return False
     battle_field = Battlefield(0, 0, 0, 0, 0,
                                0)  # Modifiez cette ligne pour initialiser correctement le champ de bataille
     player = Player(player_name, battle_field)
     game.add_player(player)
     self.game_dao.update_game(game)
     return True

 def get_game(self, game_id: int) -> Game:
     return self.game_dao.find_game(game_id)

 def add_vessel(self, game_id: int, player_name: str, vessel_type: str, x: int, y: int, z: int) -> bool:
     game = self.game_dao.find_game(game_id)
     if not game:
         return False
     player = next((player for player in game.players if player.name == player_name), None)
     if not player:
         return False
     battlefield = player.battle_field
     vessel = Vessel(0, x, y, z, 0, vessel_type, None)  # Modifiez cette ligne pour initialiser correctement le vaisseau
     battlefield.vessels.append(vessel)
     self.game_dao.update_player(player)
     return True

 def shoot_at(self, game_id: int, shooter_name: str, vessel_id: int, x: int, y: int, z: int) -> bool:
     game = self.game_dao.find_game(game_id)
     if not game:
         return False
     shooter = next((player for player in game.players if player.name == shooter_name), None)
     if not shooter:
         return False
     target_player = next((player for player in game.players if player.name != shooter_name), None)
     if not target_player:
         return False
     target_vessel = next((vessel for vessel in target_player.battle_field.vessels if vessel.id == vessel_id), None)
     if not target_vessel:
         return False
     shooter_weapon = next((weapon for weapon in shooter.battle_field.vessels if weapon.id == vessel_id), None)
     if not shooter_weapon:
         return False
     # VÃ©rifiez que le vaisseau tireur est Ã  portÃ©e de la cible et infligez des dÃ©gÃ¢ts Ã  la cible si nÃ©cessaire
     # Modifiez Ã©ventuellement les propriÃ©tÃ©s de shooter_weapon et de target_vessel pour reflÃ©ter l'Ã©tat de la partie
     return True

 def get_game_status(self, game_id: int, shooter_name: str) -> str:
     game = self.game_dao.find_game(game_id)
     if not game:
         return "ENCOURS"
     shooter = next((player for player in game.players if player.name == shooter_name), None)
     if not shooter:
         return "ENCOURS"
     target_player = next((player for player in game.players if player.name != shooter_name), None)
     if not target_player:
         return "ENCOURS"
     if all(vessel.hits_to_be_destroyed <= 0 for vessel in target_player.battle_field.vessels):
         return "GAGNE"
     if all(vessel.hits_to_be_destroyed <= 0 for vessel in shooter.battle_field.vessels):
         return "PERDU"
     return "ENCOURS"

#Cette mÃ©thode vÃ©rifie si tous les vaisseaux du joueur cible ont Ã©tÃ© dÃ©truits, auquel cas le joueur tireur a gagnÃ©.
# Si tous les vaisseaux du joueur tireur ont Ã©tÃ© dÃ©truits, le joueur cible a gagnÃ©.




