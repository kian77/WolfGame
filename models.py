from django.db import models
import json
from enum import Enum
from datetime import datetime

# Create your models here.

class GameState(str, Enum):
	GAME_NOT_CREATED = "GAME_NOT_CREATED"
	GAME_CREATED = "GAME_CREATED"			#host to configure the game
	GAME_INITIATED = "GAME_INITIATED"		#host has complete configuration (what are the roles for this game), and players can start to join the game
	GAME_STARTED = "GAME_STARTED"			#players had been assigned roles randomly, and being informed of their role

	NIGHT_BEGIN = "NIGHT_BEGIN"
	WOLF_PHASE_BEGIN = "WOLF_PHASE_BEGIN"
	WOLF_PHASE_END = "WOLF_PHASE_END"	#decided on victim

	WITCH_PHASE_BEGIN = "WITCH_PHASE_BEGIN"
	WITCH_PHASE_END = "WITCH_PHASE_END"	#decided on saving, or poison, or neither

	SEER_PHASE_BEGIN = "SEER_PHASE_BEGIN"
	SEER_PHASE_END = "SEER_PHASE_END"	#decided on target to be examined, as well as his/her faction

	NIGHT_END = "NIGHT_END"

	DAY_BEGIN = "DAY_BEGIN"

	ANNOUNCEMENT_OF_NIGHT_OUTCOME = "ANNOUNCEMENT_OF_NIGHT_OUTCOME"
	HUNTER_TRIGGER_BEGIN = "HUNTER_TRIGGER_BEGIN"
	HUNTER_TRIGGER_END = "HUNTER_TRIGGER_END"

	PLAYER_SPEECH_BEGIN = "PLAYER_SPEECH_BEGIN"
	KNIGHT_TRIGGER_BEGIN = "KNIGHT_TRIGGER_BEGIN"
	KNIGHT_TRIGGER_END = "KNIGHT_TRIGGER_END"
	PLAYER_SPEECH_END = "PLAYER_SPEECH_END"

	VOTING_BEGIN = "VOTING_BEGIN"
	VOTING_END = "VOTING_END"

	DAY_END = "DAY_END"

	GAME_END = "GAME_END"


class GoodRole(str, Enum):
	PEASANT = "PEASANT"
	SEER = "SEER"
	WITCH = "WITCH"
	KNIGHT = "KNIGHT"
	HUNTER = "HUNTER"

class BadRole(str, Enum):
	WOLF = "WOLF"
	WOLF_KING = "WOLF_KING"
	SNOW_WOLF = "SNOW_WOLF"

class PlayerState(str, Enum):
	ALIVE = "ALIVE"				#also implied alive with all skills available (eg, for Knight and Witch)
	DEAD = "DEAD"
	ALIVE_WITHOUT_SKILL = "ALIVE_WITHOUT_SKILL"	#also implied witch without antidote and poison
	ALIVE_WITHOUT_ANTIDOTE = "ALIVE_WITHOUT_ANTIDOTE"
	ALIVE_WITHOUT_POISON = "ALIVE_WITHOUT_POISON"


class WolfGame:

	def __init__(self):
		self.currentGameState = GameState.GAME_NOT_CREATED

		self.numberOfPlayers = 0
		self.gameName = ""
		self.hostName = ""

		#roles used for this game
		self.roles = []

		self.players = []	# {"name":value, "timeJoined":value}

		#after randomization
		self.playerRoleAssignments = []
				# {"playerNumber":value, "name":value, "role":value, "state":value }

		self.actionCounter = 0
		self.actions = []	# {"id":value, "actor":value, "actorRole":value, "actionType":value, "action":value, "timestamp":value}
		
		self.eventCounter = 0
		self.eventLogs = []	# {"id":value, "description":value, "timestamp":value}


	def addLog(self, newEventLog):
		self.eventLogs.append(newEventLog)

	def getLog(self, startFrom):
		copy = self.eventLogs.copy()
		for i in range(0,startFrom):
			#print(">>>"+str(i)+"<<<?>>>"+str(startFrom)+"<<<")
			copy.pop(0)
		return copy

	def getLogAsString(self, startFrom):
		return json.dumps(self.getLog(startFrom))

	def getGameModel(self):
		return json.dumps(self.__dict__)

	def evalCommand(self, command):
		try:
			print("Trying to execute command:["+command+"]")
			eval(command)
		except BaseException as err:
			print("Unable to execute command:["+command+"]")
			print(err)

	def setCurrentGameState(self, newState):
		self.currentGameState = newState

	def setNumberOfPlayers(self, num):
		self.numberOfPlayers = num

	def sendActionViaPost(self, requestBody):

		actionResponse = {}

		request = json.loads(requestBody)

		if (request['action']=="openGame"):
			actionResponse = self.openGame(request['rolesSelected'])

		#startFrom = str(request['latest'])
		#startFrom2 = int(startFrom) + 1
		#startFrom2 = startFrom2 - 1
		#print(type(startFrom2))
		actionResponse['eventLogs'] = self.getLog(int(request['latest']))
		return json.dumps(actionResponse)


	def sendAction(self, startFrom, action, p1, p2, p3):

		actionResponse = {}

		if (action=="createGame"):
			actionResponse = self.createGame(p1, p2, p3)
		elif (action=="joinGame"):
			actionResponse = self.joinGame(p1, p2)
		elif (action=="openGame"):
			actionResponse = self.openGame(p1, p2)

		actionResponse['eventLogs'] = self.getLog(int(startFrom))
		#print(json.dumps(actionResponse))
		return json.dumps(actionResponse)

	def openGame(self, rolesSelected):

		actionResponse = {}

		self.roles.append(rolesSelected)

		now = datetime.now()
		currentTime = now.strftime("%H:%M:%S")
		self.eventLogs.append({"id":self.eventCounter, "description":"Game Initiated", "timestamp":currentTime})
		self.eventCounter = self.eventCounter + 1

		self.currentGameState = GameState.GAME_INITIATED
		actionResponse['systemMessage'] = "Success"
		actionResponse['gameState'] = self.currentGameState
		return actionResponse

	def createGame(self, p1, p2, p3):

		actionResponse = {}

		#state must be in GAME_NOT_CREATED, throw error otherwise
		if (self.currentGameState!=GameState.GAME_NOT_CREATED):

			actionResponse['systemMessage'] = "User Error (incorrect game state)"

		elif (p1=="" or p2=="" or p3==""):			#validate values
			actionResponse['systemMessage'] = "User Error (input vaidation fail)"

		else:
			self.hostName = p1
			self.gameName = p2
			self.numberOfPlayers = int(p3)

			now = datetime.now()
			currentTime = now.strftime("%H:%M:%S")
			self.eventLogs.append({"id":self.eventCounter, "description":"Game Created", "timestamp":currentTime})
			self.eventCounter = self.eventCounter + 1

			self.currentGameState = GameState.GAME_CREATED
			actionResponse['systemMessage'] = "Success"


		#selectively include number of players in game model in response
		actionResponse['numberOfPlayers'] = self.numberOfPlayers
		actionResponse['gameState'] = self.currentGameState
		return actionResponse


	def joinGame(self, p1, p2):

		actionResponse = {}

		#state must be in GAME_INITIATED, throw error otherwise
		if (self.currentGameState!=GameState.GAME_INITIATED):
			actionResponse['systemMessage'] = "User Error. Cannot join game (incorrect game state)"
		else:
			actionResponse['systemMessage'] = "Join Successfully"

		actionResponse['gameState'] = self.currentGameState
		return actionResponse


#		self.currentGameState = GameState.GAME_NOT_CREATED

#		self.numberOfPlayers = 0
#		self.gameName = "Game 3 of 2021 10 09"
#		self.hostName = "Kian"

		#roles used for this game
#		self.goodRoles = [GoodRole.SEER, GoodRole.WITCH, GoodRole.PEASANT]
#		self.badRoles = [BadRole.WOLF, BadRole.WOLF_KING]

#		self.players = [ {"name":"Sam", "timeJoined":"123"} ]	# {"name":value, "timeJoined":value}

		#after randomization
#		self.playerRoleAssignments = [ {"playerNumer":1, "name":"Sam", "role":GoodRole.SEER}, {"playerNumber":2, "name":"Zotong", "role":BadRole.WOLF_KING}]
				# {"playerNumber":value, "name":value, "role":value, "state":value }

#		self.actions = []	# {"id":value, "actor":value, "actorRole":value, "actionType":value, "action":value, "timestamp":value}
#		self.eventLogs = [ 	{"id":1, "description":"Seer has chosen to examine Player 3 (Jane)", "timestamp":"10:03:42pm"}, 
#							{"id":2, "description":"Demon Hunter has chosen to kill Player 7 (Mary)", "timestamp":"10:05:11pm"}]	# {"id":value, "description":value, "timestamp":value}
