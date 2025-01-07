import json

students_collection_schema = {
				'$jsonSchema' : {
					'bsonType' : 'object',
					'required' : [
							"name",
							"id",
							"Gender",
							"course",
							"student_record",
							"Parental_Education_Level",
							"Family_Income",
							"Learning_Disabilities",
							"email",
							"contact"
						],
					'properties' : {
							"name" : {
									'bsonType' : 'string',
									'description' : 'Set name of the student.'
								},
							"id" : {
								'bsonType' : 'string',
								'description' : 'Set id number provided by university.'
								},
							"Gender" : {
									'bsonType' : 'string',
									'description' : 'Student is male/female/trans'
								},
							"course" : {
									'bsonType' : 'string',
									'description' : 'Set name of the course.'
								},
							"student_record" : {
										'bsonType' : 'array',
										'description' : 'Record of this student.',

										'properties' : {
												"semester" : {
														'bsonType' : 'string',
														'description' : 'Set the current semester.'
														},
												"Exam_Score" : {
														'bsonType' : 'number',
														'description' : 'Marks secured in present semester.',
														'maximum' : 800.00
														},
												"Hours_Studied" : {
															'bsonType' : 'number',
															'description' : 'Total time studied in this semester.'
														},
												"Attendence" : {
														'bsonType' : 'int',
														'description' : 'Total attendence in this semester.',
														'maximum' : 100
														},
												"Parental_Involvement" : {
															'bsonType' : 'string',
															'description' : 'Was parent involved in success/failure?'
															},
												"Access_to_Resources" : {
															'bsonType' : 'string',
															'description' : 'How much resource has been used for topics study.'	
															},
												"Extracurricular_Activities" : {
																'bsonType' : 'string',
																'description' : 'Was student inveolved in extracurricular activities?'
															},
												"Physical_Activity" : {
															'bsonType' : 'int',
															'description' : 'how many sports played by student.',
															'maximum' : 6
															},
												"Tutoring_Sessions" : {
															'bsonType' : 'int',
															'description' : 'How many tution sessions did the student attended'
															},
												"Teacher_Quality" : {
															'bsonType' : 'string',
															'description' : 'Quality of teachers in this semester.'
															},	
												"GPA" : {
													'bsonType' : 'number',
													'description' : 'gpa of this semester.',
													'maximum' : 4.0
													},
												"CGPA" : {
													'bsonType' : 'number',
													'description' : 'cgpa of this course.',
													'maximum' : 4.0
												},
												"time_stamp" : {
														'bsonType' : 'string',
														'description' : 'Time stamp of the record.'
													}
									}
								},
							"Parental_Education_Level" : {
											'bsonType' : 'string',
											'description' : 'Education qualification of parent.'
										},
							"Family_Income" : {
										'bsonType' : 'string',
										'description' : 'Income level of family.'
									},
							"Learning_Disabilities" : {
											'bsonType' : 'string',
											'description' : 'Is student face physical problem while studying.'
										},
							"email" : {
									'bsonType' : 'string',
									'description' : 'Set the active email'
								},
							"contact" : {
									'bsonType' : 'string',
									'description' : 'Set active contact number.'
								}
						}

				}
			}
