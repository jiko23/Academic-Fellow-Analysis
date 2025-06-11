import asyncio
import jwt
from typing import List
from pydantic import EmailStr
from cryptography.fernet import Fernet
from MongoServerConnection import DatabaseOperations
from bson.codec_options import CodecOptions


class User_Directory:
	def __init__(self):
		self.dbClient = None
		self.dbInstance = None


	async def dbClientStartup(self):
		try:
			self.dbClient = await DatabaseOperations('mongo_test').dbClientStartup()
		except Exception as e:
			print(e)
		return self.dbClient


	async def connectToDB(self):
		try:
			self.dbInstance = self.dbClient['mongo_test']
		except Exception as e:
			print(e)
		return self.dbInstance


	def getUserSchema(self) -> {}:
		user_schema = {
				'$jsonSchema' : {
							'bsonType' : 'object',
							'required' : ['email', 'role', 'password', 'crypto_key'],
							'properties' : {
										'email' : {
												'bsonType' : 'string',
												'description' : "Register yourself with email."
											},
										'role' : {
												'bsonType' : 'string',
												'description' : "Authorization to access database."
											},
										'password' : {
												'bsonType' : 'bytes',
												'description' : "Password to protect your identity."
											},
										'crypto_key' : {
												'bsonType' : 'bytes',
												'description' : "Key will be used to encrypt and decrypt password."
											}
									}
						}
				}

		return user_schema


	async def createCollection(self) -> bool:
		try:
			self.dbInstance.create_collection(name = 'Users', validator = self.getUserSchema())
			print("{} collection created.".format('Users'))
			return True
		except Exception as e:
			print(e)
		return False


	async def userExist(self, email : EmailStr) -> bool:
		temp = []
		_user = self.dbInstance.Users.find({'email' : email})
		for docs in _user:
			temp.append({
				'email' : docs['email'],
				'password' : docs['password']
				})
		if(len(temp) > 0):
			print("user already exist.")
			return True
		return False


	async def getUserDetails(self, email : EmailStr):
		try:
			_user = self.dbInstance.Users.find({'email' : email})
			for docs in _user:
				temp = {
					'email' : docs['email'],
					'password' : docs['password'],
					'key' : docs['key'],
					'role' : docs['role']
					}
			return temp
		except Exception as e:
			print(e)
		return {}


	async def insertUser(self, user : {}):
		with self.dbClient.start_session() as session:
			session.start_transaction()
			try:
				_id = self.dbInstance.Users.create_index('email', unique = True)
				self.dbInstance.Users.insert_one(user, session = session)
				session.commit_transaction()
				print("_id :", _id)
			except Exception as e:
				print(e)
				session.abort_transaction()
		return "Could not insert user."


	async def deleteUser(self, user : {}):
		with self.dbClient.start_session() as session:
			session.start_transaction()
			try:
				self.dbInstance.Users.delete_one(user, comment = 'deleted {}'.format(user), session = session)
				session.commit_transaction()
			except Exception as e:
				print(e)
				session.abort_transaction()
		return


	async def passwordUpdate(self, email : EmailStr, password : bytes, key : bytes):
		assert(await self.userExist(email) == True)

		with self.dbClient.start_session() as session:
			session.start_transaction()
			try:
				updated_value = {'$set' : {'password' : password, 'key' : key}}
				self.dbInstance.Users.update_many({'email' : email}, updated_value, session = session)
				print("Done.....")
				session.commit_transaction()
			except Exception as e:
				print(e)
				session.abort_transaction()
		return


	async def closeClient(self):
		try:
			self.dbClient.close()
		except Exception as e:
			print(e)
		finally:
			print("Client conection closed...")

	async def main(self):
		await self.dbClientStartup()
		await self.connectToDB()
		await self.createCollection()
		return
				


class User:
	def __init__(self):
		self.user_directory = User_Directory()
		self.userCount = 1

	async def callable(self):
		await self.user_directory.main()
		return


	def generateSecureKey(self) -> str:
		try:
			key = Fernet.generate_key()
		except Exception as e:
			print(e)
		return key


	def encryptPassword(self, key : str, secret : str):
		try:
			f = Fernet(key)
			secret = memoryview(secret.encode('utf-8')).tobytes()
			encrypted_token = f.encrypt(secret)
		except Exception as e:
			print(e)
		return encrypted_token


	def decryptPassword(self, key : bytes, password : bytes):
		try:
			f = Fernet(key)
			decrypted_token = f.decrypt(password)
		except Exception as e:
			print(e)
		return decrypted_token


	async def registerUser(self, email : EmailStr, password : str, role : str):
		try:
			key = self.generateSecureKey()
			record = {'email' : email, 'role' : role, 'password' : self.encryptPassword(key, password), 'key' : key}

			assert(await self.user_directory.userExist(email) == False)

			await self.user_directory.insertUser(record)
			self.userCount += 1
			print("{}. inserted using key {}".format(self.userCount, key))
		except Exception as e:
			print(e)
		return


	async def authenticateUser(self, email : EmailStr, password : str) -> bool:
		print("log {} :{}".format(2.0, self.user_directory.dbClient))
		print("log {} :{}".format(2.1, self.user_directory.dbInstance))
		try:
			assert(await self.user_directory.userExist(email) == True)

			details = await self.user_directory.getUserDetails(email)
			decrypt_psw_check = self.decryptPassword(details['key'], details['password'])
			password = memoryview(password.encode('utf-8')).tobytes()
			if(password == decrypt_psw_check):
				return True
		except Exception as e:
			print(e)
		return False


	async def updateUserPassword(self, email : EmailStr, password : str):
		try:
			key = self.generateSecureKey()
			password = self.encryptPassword(key, password)
			await self.user_directory.passwordUpdate(email, password, key)
			print("password updated...")
		except Exception as e:
			print(e)
		return


	async def createAuthToken(self, email : EmailStr):
		try:
			secret_key = "JAYANTA124"
			algorithm = 'HS256'

			user = await self.user_directory.getUserDetails(email)
			psw = self.decryptPassword(user['key'], user['password']).decode("utf-8")
			role = await self.user_directory.getUserDetails(email)

			user_payload = {'email' : user['email'], 'role' : user['role'], 'password' : psw}
			token = jwt.encode(payload = user_payload, key = secret_key, algorithm = algorithm)
			return token
		except Exception as e:
			print(e)
		return None


	async def decodeAuthToken(self, token : str):
		try:
			secret_key = "JAYANTA124"
			algorithm = 'HS256'
			token_details = jwt.decode(token, key = secret_key, algorithms= algorithm)
			return token_details['role']
		except Exception as e:
			print(e)
		return None


	async def deleteUser(self, user : {}):
		try:
			await self.user_directory.deleteUser(user)
		except Exception as e:
			print(e)
		finally:
			print("deleted {}".format(user))
			self.userCount -= 1
		return