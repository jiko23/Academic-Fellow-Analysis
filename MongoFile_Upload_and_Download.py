import asyncio
from pathlib import Path

async def uploadFileIntoBucket(gridFs_bucket, file):
	file_name = None
	try:
		if(gridFs_bucket != None):
			file_name = Path(file).stem

		with open(file, "rb") as file_data:
			data = file_data.read()
		gridFs_bucket.put(data, filename = file_name)

		return {"filename" : file_name}
	except Exception as e:
		print(e)
	return "None"


async def downloadFileFromBucket(grid_bucket, file_name):
	try:
		data = db.grid_bucket.find_one({filename : file_name})
		file_id = data['_id']
		#check here to get file id
		output_data = grid_bucket.get(file_id).read()
		return output_data
	except Exception as e:
		print(e)
	return "None"		