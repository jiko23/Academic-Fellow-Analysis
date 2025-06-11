import sys
import asyncio
import json
import jsonschema
import pymongo
import gridfs
import datetime
from typing import List
from loguru import logger
from bson.codec_options import CodecOptions
from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus
from Schemas.StudentSchema import students_collection_schema
from Schemas.StudentMentalHealthSchema import student_mental_health_schema
from SampleInput import input1, semester1, emergency_mental_health_record
from MongoFile_Upload_and_Download import *
from jsonschema import validate

#logging setup
logger.remove()
logger.add(sys.stdout, format="<green>{time}</green> --> <cyan>{line}</cyan>:: {level} : {message}", level="SUCCESS")
logger.add(sys.stdout, format="<green>{time}</green> --> <red>{line}</red>:: {level} : {message}", level="INFO")
logger.add(sys.stdout, format="<red>{time}</red> --> <green>{line}</green>:: {level} : {message}", level="ERROR")
logger.add("logs\\file_{time}.log", rotation="1 week", compression="zip")


class DatabaseOperations:
	def __init__(self, dbName):
		self.dbs = []
		self.dbName = dbName
		self.client = None
		self.dbInstance = None
		self.gridFs_bucket = None
		self.username = quote_plus('mongodb-username')
		self.password = quote_plus('mongodb-password')
		self.uri = "mongodb+srv://{}:{}@your-mongo-cluster".format(self.username, self.password)

	async def dbClientStartup(self):
		try:
			self.client = MongoClient(self.uri)
			logger.success("Connection established...")
			return self.client
		except Exception as e:
			logger.error("Could not establish connection. -> {}".format(e))
		return


	async def databaseNames(self)->[]:
		try:
			self.dbs = self.client.list_database_names()
			logger.info("dbs : {}".format(self.dbs))
			return self.dbs
		except Exception as e:
			logger.error("Could not fetch dbs.")
		return []


	def checkDBExistance(self) -> bool:
		if self.dbName in self.dbs:
			logger.info("{} exists.".format(self.dbName))
			return True
		else:
			logger.error("{} does not exist.Create it.".format(self.dbName))
			return False


	async def connectToDB(self):
		try:
			if(self.checkDBExistance() == False):
				self.dbInstance = self.client[self.dbName]
				return self.dbInstance
			else:
				self.dbInstance = self.client[self.dbName]
				logger.success("Connection to {} has been extablished...".format(self.dbName))
		except Exception as e:
			logger.exception("connect to {} failed.".format(self.dbName))
		return


	async def countDocsInCollection(self) -> int:
		try:
			docs_count = self.dbInstance.Students.count_documents({})
			logger.info("num docs = {}".format(docs_count))
			return docs_count
		except Exception as e:
			logger.exception("docs count failed : {}".format(e))
		return


	def getCollectionSchema(self, collectionSchema = {}):
		try:
			collectionSchema = students_collection_schema
			return collectionSchema
		except Exception as e:
			logger.exception(e)
		return collectionSchema


	async def createCollection(self):
		try:
			self.dbInstance.create_collection(name = "Students", validator = self.getCollectionSchema())
			logger.success("Successfully created collection named {} in DB.".format("Students"))
		except Exception as e:
			logger.exception(e)
		return "Collection successfully created..."


	async def structureRecordToInsert(self, recordToInsert):
		try:
			self.gridFs_bucket = gridfs.GridFS(self.dbInstance, collection = "Students")
			if(self.gridFs_bucket == None):
				sys.exit()

			recordToInsert["student_psyciatrist_meet_video"] = await uploadFileIntoBucket(
													self.gridFs_bucket,
													recordToInsert["student_psyciatrist_meet_video"]
													)
			logger.info("uploaded 1...")
			recordToInsert["student_appearance"]["physical_determinents"]["medical_test_report"] = await uploadFileIntoBucket(
																		self.gridFs_bucket,
																		recordToInsert["student_appearance"]["physical_determinents"]["medical_test_report"]
																	)
			logger.info("uploaded 2...")
			recordToInsert["psyciatrist_details"]["aadhar/pan/passport"] = await uploadFileIntoBucket(
															self.gridFs_bucket,
															recordToInsert["psyciatrist_details"]["aadhar/pan/passport"]
														)
			logger.info("uploaded 3...")
			recordToInsert["psyciatrist_details"]["signature"] = await uploadFileIntoBucket(
													self.gridFs_bucket,
													recordToInsert["psyciatrist_details"]["signature"]
													)
			logger.info("uploaded 4...")
			recordToInsert["session_monitoring_faculty"]["faculty_id_image"] = await uploadFileIntoBucket(
															self.gridFs_bucket,
															recordToInsert["session_monitoring_faculty"]["faculty_id_image"]
															)
			logger.info("uploaded 5...")
			recordToInsert["session_monitoring_faculty"]["aadhar/pan/passport_image"] = await uploadFileIntoBucket(
																self.gridFs_bucket,
																recordToInsert["session_monitoring_faculty"]["aadhar/pan/passport_image"]
																)
			logger.info("uploaded 6...")
			recordToInsert["session_monitoring_faculty"]["signature_image"] = await uploadFileIntoBucket(
															self.gridFs_bucket,
															recordToInsert["session_monitoring_faculty"]["signature_image"]	
															)
			logger.info("uploaded 7...")
			recordToInsert["session_monitoring_faculty"]["faculty_passport_size_image"] = await uploadFileIntoBucket(
																self.gridFs_bucket,
																recordToInsert["session_monitoring_faculty"]["faculty_passport_size_image"]
																)
			logger.info("uploaded 8...")
		except Exception as e:
			logger.exception(e)
		return recordToInsert


	async def insertSingleRecordIntoCollection(self, record):
		with self.client.start_session() as session:
			session.start_transaction()
			try:
				self.dbInstance.Students.create_index('name', unique = True)
				self.dbInstance.Students.insert_one(record, session = session)
				session.commit_transaction()
				logger.success("single record inserted...")
			except Exception as e:
				logger.error("Transaction to be aborted...")
				session.abort_transaction()
				logger.exception(e)
		return


	async def insertManyRecordIntoCollection(self, record_Json):
		with self.client.start_session() as session:
			session.start_transaction()
			try:
				self.dbInstance.Students.create_index('name', unique = True)
				self.dbInstance.Students.insert_many(record_Json, ordered = True, session = session)
				session.commit_transaction()
				logger.success("Multiple records inserted.")
			except Exception as e:
				logger.error("Transaction to be aborted...")
				session.abort_transaction()
				logger.exception(e)
		return


	async def insertSemesterInStudentRecord(self, filter, semester_Json):
		#semester_Json = await self.structureRecordToInsert(semester_Json)
		with self.client.start_session() as session:
			session.start_transaction()
			try:
				self.dbInstance.Students.update_one(filter, {'$push' : {"student_record" : semester_Json}}, session = session)
				session.commit_transaction()
				logger.success("New semester has been added.")
			except Exception as e:
				logger.error("Transaction to be aborted...")
				session.abort_transaction()
				logger.exception(e)
		return

	def validateJsonSchema(self, psyciatrist_meet_record):
		err_list = []
		try:
			validator = jsonschema.Draft7Validator(student_mental_health_schema)
			#_validate = validate(instance = psyciatrist_meet_record, schema = student_mental_health_schema)
			errors = validator.iter_errors(psyciatrist_meet_record)
			err_list = [err_list.append(error) for error in errors]
		except jsonschema.exceptions.ValidationError as e:
			logger.exception(e.message)
		return err_list
			

	async def insertStudentPsyciatristMeetRecord(self, filter, meet_record):
		psyciatrist_meet_record = await self.structureRecordToInsert(meet_record)
		schema_validation_errors = self.validateJsonSchema(meet_record)

		with self.client.start_session() as session:
			session.start_transaction()
			try:
				assert(len(schema_validation_errors) == 0)
				##issue here to insert into 'student_mental_health_record' field.
				self.dbInstance.Students.update_one(filter, {'$push' : {"student_record.$.student_mental_health_record" : psyciatrist_meet_record}}, session = session)
				session.commit_transaction()
				logger.success("Psyciatrist meet record has been added...")
			except Exception as e:
				logger.error("Psyciatrist meet record upload aborted...")
				session.abort_transaction()
				logger.exception(e)
		return


	async def updateOneRecord(self, filter, updated_value):
		#field_to_update = [key for key in filter.keys()]
		#updatedValue = {'$set' : {field_to_update[0] : new_value}}

		with self.client.start_session() as session:
			session.start_transaction()
			try:
				self.dbInstance.Students.update_one(filter, {'$set' : updated_value}, session = session)
				session.commit_transaction()
				logger.success("single field value updated successfully.")
			except Exception as e:
				logger.error("Transaction to be aborted...")
				session.abort_transaction()
				logger.exception(e)
		return


	async def updateManyRecords(self, filter, updatedValue, intUpdatedValue):
		with self.client.start_session() as session:
			session.start_transaction()
			try:
				#have issue with applying set and inc at a time
				self.dbInstance.Students.update_many(filter, {'$set' : updatedValue, '$inc' : intUpdatedValue}, session = session)
				session.commit_transaction()
				logger.success("multiple field values updated successfully.")
			except Exception as e:
				logger.error("Transaction to be aborted...")
				session.abort_transaction()
				logger.exception(e)
		return


	async def nestedArrayObjectUpdate(self, filter, property_update):
		with self.client.start_session() as session:
			session.start_transaction()
			try:
				self.dbInstance.Students.update_one(filter, {'$set' : property_update})
				session.commit_transaction()
				logger.success("Array Obj updated.")
			except Exception as e:
				logger.error("Transaction to be aborted...")
				session.abort_transaction()
				logger.exception(e)
		return


	async def findRecordFromCollection(self, search_query):
		recordList = []
		try:
			docs_count = await self.countDocsInCollection()
			record = self.dbInstance.Students.find(search_query)

			for docs in record:
				temp = {'name' : docs['name'],
					'id' : docs['id'],
					'Gender' : docs['Gender'],
					'course' : docs['course'],
					'student_record' : docs['student_record'],
					'Parental_Education_Level' : docs['Parental_Education_Level'],
					'Family_Income' : docs['Family_Income'],
					'Learning_Disabilities' : docs['Learning_Disabilities'],
					'email' : docs['email'],
					'contact' : docs['contact']
					}
				recordList.append(temp)
				print(recordList)
			record.close()
		except Exception as e:
			logger.exception(e)
		return recordList


	async def deleteOneRecord(self, filter):
		with self.client.start_session() as session:
			session.start_transaction()
			try:
				self.dbInstance.Students.delete_one(filter, comment = "deleting a student record.", session = session)
				session.commit_transaction()
				logger.info("{} left.".format(await self.countDocsInCollection()))
			except Exception as e:
				logger.error("Transaction to be aborted...")
				session.abort_transaction()
				logger.exception(e)
			return


	async def deleteManyRecords(self, filter):
		with self.client.start_session() as session:
			session.start_transaction()
			try:
				self.dbInstance.Students.delete_many(filter, comment = "deleting multiple student records.", session = session)
				session.commit_transaction()
				logger.info("{} left.".format(await self.countDocsInCollection()))
			except Exception as e:
				logger.error("Transaction to be aborted...")
				session.abort_transaction()
				logger.exception(e)
			return


	async def dropCollection(self):
		with self.client.start_session() as session:
			session.start_transaction()
			try:
				self.dbInstance.Students.drop()
				session.commit_transaction()
				logger.success("Successfully deleted collection.")
			except Exception as e:
				logger.error("Transaction has been aborted...")
				session.abort_transaction()
				logger.exception(e)
			return


	async def closeDbConnection(self):
		try:
			self.client.close()
			logger.success("DB connection has been closed successfully.")
		except Exception as e:
			logger.exception(e)
		return


	async def main(self):
		await self.dbClientStartup()

		await self.databaseNames()

		await self.connectToDB()

		#await self.createCollection()

		#await self.insertSingleRecordIntoCollection(input1)

		#filter = {"id" : "GEU23"}
		#await self.insertSemesterInStudentRecord(filter, semester1)

		#uploading a new psyciatrist meet
		#logger.info("inserting a psyciatrist meet record...")
		#filter = {"id" : "GEU23", "student_record.semester" : "1"}
		#await self.insertStudentPsyciatristMeetRecord(filter, emergency_mental_health_record)

		await self.downloadFileFromBucket()

		await self.closeDbConnection()
		return


if __name__ == '__main__':
	dbObj = DatabaseOperations('mongo_test')

	#db operations
	asyncio.run(dbObj.main())
