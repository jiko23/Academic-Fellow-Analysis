import asyncio
import contextlib
import datetime
from enum import Enum
from typing import List, Optional
from typing_extensions import Annotated
from urllib.parse import quote_plus
from pydantic import BaseModel, StrictInt, EmailStr
from MongoServerConnection import DatabaseOperations
from UserRegistry import User
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


#Enums
class Gender(str, Enum):
	male = 'Male'
	female = 'Female'

class TeacherQuality(str, Enum):
	medium = 'Medium'
	high = 'High'
	low = 'Low'

class ParentalInvolvement(str, Enum):
	medium = 'Medium'
	high = 'High'
	low = 'Low'

class AccessToResources(str, Enum):
	medium = 'Medium'
	high = 'High'
	low = 'Low'

class ExtracurricularActivity(str, Enum):
	yes = 'Yes'
	no = 'No'

class FamilyIncome(str, Enum):
	medium = 'Medium'
	high = 'High'
	low = 'Low'

class LearningDisabilities(str, Enum):
	yes = 'Yes'
	no = 'No'

#Student mental health record
	#build Basemodel for sub-schema and final schema.

#Student Records
class SemesterInfo(BaseModel):
	semester : str
	Exam_Score : Optional[float] = 0.0
	Hours_Studied : Optional[float] = 0.0
	Attendence : Optional[int] = 0
	Parental_Involvement : ParentalInvolvement
	Access_to_Resources : AccessToResources
	Extracurricular_Activity : ExtracurricularActivity
	Tutoring_Sessions : Optional[int] = 0
	Teacher_Quality : TeacherQuality
	GPA : Optional[float] = 0.0
	CGPA : Optional[float] = 0.0
	date : Optional[str] = datetime.datetime.now()


class SingleRecord(BaseModel):
	name : str 
	id : str
	Gender : Gender
	course : str
	student_record : List[SemesterInfo]
	Parental_Education_Level : str
	Family_Income : FamilyIncome
	Learning_Disabilities : LearningDisabilities
	email : EmailStr
	contact : str


class QuryModel(BaseModel):
	name : str
	id : str

#updation models	
class SingleUpdate(BaseModel):
	filter : dict
	updated_value : dict

class MultiUpdate(BaseModel):
	filter : dict
	updated_values : dict
	int_update : dict

class StudentRecordUpdate(BaseModel):
	filter : dict
	updated_value : dict


#delete records model
class DeleteQueryFilter(BaseModel):
	filter : dict



async def establishConnection():
	await dbObj.dbClientStartup()
	dbInstance = await dbObj.connectToDB()
	return dbInstance


def convertListToDict(_list) -> []:
	for doc_num in range(0, len(_list), 1):
		_list[doc_num] = _list[doc_num].dict(include = {
					'name' : doc_num['name'],
					'id' : doc_num['id'],
					'Gender' : doc_num['Gender'],
					'course' : doc_num['course'],
					'student_record' : doc_num['student_record'],
					'Parental_Education_Level' : doc_num['Parental_Education_Level'],
					'Family_Income' : doc_num['Family_Income'],
					'Learning_Disabilities' : doc_num['Learning_Disabilities'],
					'email' : doc_num['email'],
					'contact' : doc_num['contact']
				})

	return _list


dbObj = DatabaseOperations('mongo_test')
user = User()

@contextlib.asynccontextmanager
async def lifespan(app : FastAPI):
	try:
		print("Application has started...")
		yield
		print("Application closed successfully...")
	except:
		print("Lifespan creation failed...")


app = FastAPI(title = "Student Record", lifespan = lifespan)

@app.post("/login-token")
async def createToken(form_data : OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
	await user.callable()

	email = form_data.username
	password = form_data.password

	user_authenticated = await user.authenticateUser(email, password)
	if(user_authenticated == False):
		raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)

	token = await user.createAuthToken(email)
	#response.set_cookie(
		#"Access_TOKEN",
		#token,
		#max_age = 10,
		#secure = True,
		#httponly = True,
		#samesite = "lax"
		#)
	return {"access_token" : token, "token_type" : "bearer"}


@app.get('/dbList', dependencies = [Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))])
async def dbList(token : str = Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))):
	role = await user.decodeAuthToken(token)
	allowed_roles = ["admin", "user"]
	if(role not in allowed_roles):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Only admin & user roles allowed.")

	try:
		await establishConnection()
		db_list = await dbObj.databaseNames()
		await dbObj.closeDbConnection()
	except:
		raise HTTPException(status_code = 404, details = "Cannot be found.")
	return {"databases" :db_list}


@app.post('/create-collection', dependencies = [Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))])
async def createCollection(token : str = Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))):
	role = await user.decodeAuthToken(token)
	if( role != "admin"):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Only admin allowed.")

	try:
		await establishConnection()
		message = await dbObj.createCollection()
		await dbObj.closeDbConnection()
	except:
		raise HTTPException(status_code = 422, details = "Unprocessable Entity.")
	return {"message" : message}


@app.get('/collection_schema', dependencies = [Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))])
async def getCollectionSchema():
	try:
		schema = dbObj.getCollectionSchema()
	except:
		raise HTTPException(status_code = 404, details = "Schema not found.")
	return {'schema' : schema}


@app.post('/insertSingleRecord', dependencies = [Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))])
async def singleRecordInsert(record : SingleRecord, token : str = Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))):
	role = await user.decodeAuthToken(token)
	if( role != "admin"):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Only admin allowed.")
	print(SingleRecord)

	record = record.dict(include = {
					"name" : ...,
					"id" : ...,
					"Gender" : ...,
					"course" : ...,
					"student_record" : ...,
					"Parental_Education_Level" : ...,
					"Family_Income" : ...,
					"Learning_Disabilities" : ...,
					"email" : ...,
					"contact" : ...
			})

	try:
		await establishConnection()
		await dbObj.insertSingleRecordIntoCollection(record)
		await dbObj.closeDbConnection()
	except:
		raise HTTPException(status_code = 400, details = "Schema not found.")
	return {'message' : "record has been inserted!!!"}



@app.post('/insertMany', dependencies = [Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))])
async def multiRecordInsert(records : List[SingleRecord], token : str = Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))):
	role = await user.decodeAuthToken(token)
	if( role != "admin"):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Only admin allowed.")

	records = convertListToDict(records)
	try:
		await establishConnection()
		await dbObj.insertManyRecordIntoCollection(records)
		await dbObj.closeDbConnection()
	except:
		raise HTTPException(status_code = 400, details = "Schema not found.")
	return {'message' : "records has been inserted!!!"}


@app.post('/insertSemester', dependencies = [Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))])
async def addSemesterToStudentRecord(filter : dict,semester : SemesterInfo, token : str = Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))):
	role = await user.decodeAuthToken(token)
	if( role != "admin"):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Only admin allowed.")

	try:
		await establishConnection()
		print(type(semester))
		await dbObj.insertSemesterInStudentRecord(filter, semester.dict())
		await dbObj.closeDbConnection()
	except:
		raise HTTPException(status_code = 400, details = "Schema not found.")
	return {'message' : "semester added!!!"}

## ADD A ENDPOINT TO INSERT STUDENT MENTAL HEALTH RECORD.

@app.post('/getRecord', dependencies = [Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))])
async def getDocument(query : QuryModel, token : str = Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))):
	query = query.dict(include = {"name" : ..., "id" : ...})
	try:
		await establishConnection()
		record = await dbObj.findRecordFromCollection(query)
		await dbObj.closeDbConnection()
	except:
		raise HTTPException(status_code = 400, details = "Record not found.")
	return {'message' : record}


@app.patch('/updateOne', dependencies = [Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))])
async def updateSingleRecord(update_query : SingleUpdate, token : str = Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))):
	role = await user.decodeAuthToken(token)
	if( role != "admin"):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Only admin allowed.")

	try:
		await establishConnection()
		record = await dbObj.updateOneRecord(update_query.filter, update_query.updated_value)
		await dbObj.closeDbConnection()
	except:
		raise HTTPException(status_code = 204, details = "Record not updated.")
	return {'message' : "Record updated."}


@app.put('/updateMany', dependencies = [Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))])
async def updateMultipleRecord(update_query : MultiUpdate, token : str = Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))):
	role = await user.decodeAuthToken(token)
	if( role != "admin"):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Only admin allowed.")

	try:
		await establishConnection()
		record = await dbObj.updateManyRecords(update_query.filter, update_query.updated_values, update_query.int_update)
		await dbObj.closeDbConnection()
	except:
		raise HTTPException(status_code = 204, details = "Record not updated.")
	return {'message' : "Record updated."}


@app.put('/update_student_record', dependencies = [Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))])
async def updateNestedArrayObject(update_body : StudentRecordUpdate, token : str = Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))):
	role = await user.decodeAuthToken(token)
	if( role != "admin"):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Only admin allowed.")

	try:
		await establishConnection()
		record = await dbObj.nestedArrayObjectUpdate(update_body.filter, update_body.updated_value)
		await dbObj.closeDbConnection()
	except:
		raise HTTPException(status_code = 204, details = "Record not updated.")
	return {'message' : "Record updated."}


@app.delete('/delete_one_record', dependencies = [Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))])
async def deleteSingleRecord(delete_query : DeleteQueryFilter, token : str = Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))):
	role = await user.decodeAuthToken(token)
	if( role != "admin"):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Only admin allowed.")

	try:
		await establishConnection()
		result = await dbObj.deleteOneRecord(delete_query.filter)
		await dbObj.closeDbConnection()
	except:
		raise HTTPException(status_code = 204, details = "Record not deleted.")
	return {'record deleted' : result}


@app.delete('/delete_many_records', dependencies = [Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))])
async def deleteMultipleRecords(delete_query : DeleteQueryFilter, token : str = Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))):
	role = await user.decodeAuthToken(token)
	if( role != "admin"):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Only admin allowed.")

	try:
		await establishConnection()
		result = await dbObj.deleteManyRecords(delete_query.filter)
		await dbObj.closeDbConnection()
	except:
		raise HTTPException(status_code = 204, details = "Records not deleted.")
	return {'records deleted' : result}


@app.delete('/delete_collection', dependencies = [Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))])
async def dropCollection(token : str = Depends(OAuth2PasswordBearer(tokenUrl="/login-token"))):
	role = await user.decodeAuthToken(token)
	if( role != "admin"):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Only admin allowed.")

	try:
		await establishConnection()
		result = await dbObj.dropCollection()
		await dbObj.closeDbConnection()
	except:
		raise HTTPException(status_code = 204, details = "Records not deleted.")
	return {'records deleted' : result}