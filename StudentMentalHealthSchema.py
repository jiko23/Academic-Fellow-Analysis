import json

##sub-schemas for major schema "student_mental_health_schema"
#sub-schema for student_appearance.#
student_appearance = {
				'bsonType' : 'object',
				'description' : 'sub-schema for student appearance record.',
				'required' : [
						'physical_determinents',
						'intellectual_determinents',
						'social_determinents'
						],
				'properties' : {
									'physical_determinents' : {
													'bsonType' : 'array',
													'description' : 'student physical determinents.',
													'properties' : {
																"sociability" : {
																			'bsonType' : 'string',
																			'description' : 'how good is the student social mixing capability.',
																			'enum' : ["worst", "average", "good", "very_good"]
																	},
																"impulsivity_level" : {
																				'bsonType' : 'string',
																				'description' : 'is the student impulsive or not.',
																				'enum' : ["high", "average", "normal"]
																		},
																"emotional_intelligence_level" : {
																					'bsonType' : 'string',
																					'description' : 'is the student able to handle emotions.',
																					'enum' : ["worst", "average", "good", "very_good"]
																			},
																"physical_features" : {
																				'bsonType' : 'array',
																				'description' : 'physical features of the student.',
																				'properties' : {
																							"height" : {
																									'bsonType' : 'number',
																									'description' : 'student height.'
																								},
																							"weight" : {
																									'bsonType' : 'number',
																									'description' : 'student weight.'
																								}
																					}
																		},
																"medical_test_report" : {
																				'bsonType' : 'string',
																				'description' : 'combined medical report pdf of the student.'
																		}
														}
											},
									'intellectual_determinents' : {
														'bsonType' : 'array',
														'description' : 'intellectual capability of the student.',
														'properties' : {
																	"reasoning_skills" : {
																				'bsonType' : 'string',
																				'description' : 'student reasoning ability.',
																				'enum' : ['worst', 'good', 'bad', 'average', 'very_good']
																			},
																	"problem_solving_skill" : {
																					'bsonType' : 'string',
																					'description' : 'student problem solving ability.',
																					'enum' : ['worst', 'good', 'bad', 'average', 'very_good']
																			},
																	"decision_making_skill" : {
																					'bsonType' : 'string',
																					'description' : 'student decision making style.',
																					'enum' : ['worst', 'good', 'bad', 'average', 'very_good']
																				},
																	"critical_thinking_skill" : {
																				'bsonType' : 'string',
																				'description' : 'student critical thinking capability.',
																				'enum' : ['worst', 'good', 'bad', 'average', 'very_good']
																			},
																	"memory_capacity" : {
																				'bsonType' : 'string',
																				'description' : 'student memory capacity.',
																				'enum' : ['worst', 'good', 'bad', 'average', 'very_good']
																			},
																	"belief" : {
																			'bsonType' : 'string',
																			'description' : 'student beliefs.',
																			'enum' : ['worst', 'good', 'bad', 'average', 'very_good']
																		}
															}
												},
									'social_determinents' : {
													'bsonType' : 'array',
													'description' : 'student social skills.',
													'properties' : {
																"friendcircle" : {
																			'bsonType' : 'string',
																			'description' : 'friend circle of the student.'
																		},
																"socialmedia/ott_access" : {
																				'bsonType' : 'array',
																				'description' : 'student indulgence in social media or ott.',
																				'properties' : {
																							"yes/no?" : {
																									'bsonType' : 'bool',
																									'description' : 'do student access social media excessively?',
																									'enum' : ['yes', 'no']
																								},
																							"sites" : {
																									'bsonType' : 'array',
																									'description' : 'list of sites student access'
																								},
																							"content_types" : {
																										'bsonType' : 'array',
																										'description' : 'list of types of contents.'
																									}
																						}
																			},
																"speech_style" : {
																			'bsonType' : 'string',
																			'description' : 'speech style of the student.'
																		},
																"judgement_capability" : {
																				'bsonType' : 'string',
																				'description' : 'student situational judgement capability.'
																		},
																"nature" : {
																		'bsonType' : 'string',
																		'description' : 'student nature.'
																	}
														}
													
											}
							}
}


#sub-schema for level of conciousness of student.#
level_of_conciousness = {
							'bsonType' : 'object',
							'description' : 'Student level of conciousness record sub-schema',
							'required' : [
									"eye_response",
									"verbal_response",
									"motor_response",
									"facial_trauma"
								],
							'properties' : {
										"eye_response" : {
													'bsonType' : 'int',
													'description' : 'student eye response score.',
													'minimum' : 3,
													'maximum' : 15
											},
										"verbal_response" : {
													'bsonType' : 'int',
													'description' : 'student verbal respnse score.',
													'minimum' : 3,
													'maximum' : 15
												},
										"motor_response" : {
													'bsonType' : 'int',
													'description' : 'student motor response score.',
													'minimum' : 3,
													'maximum' : 15
												},
										"facial_trauma" : {
													'bsonType' : 'bool',
													'description' : 'if student has/had any facial trauma.'
												}
				}
}

#sub-schema for speech & mood#
speech_and_mood = {
						'bsonType' : 'object',
						'description' : 'sub-schema for student speech and mood.',
						'required' : [
								"speech_status",
								"mood_status"
							],
						'properties' : {
									"speech_status" : {
												'bsonType' : 'string',
												'description' : 'student speech skill status.'
											},
									"mood_status" : {
												'bsonType' : 'string',
												'description' : 'student mood status. '
										}
		}
}

#sub-schema for attitude and insight#
attitude_and_insight = {
						'bsonType' : 'object',
						'description' : 'student attitude and insights record.',
						'required' : [
								"responsibilities",
								"communication_engagement",
								"aggression_control",
								"distractive_nature"
							],
						'properties' : {
									"responsibilities" : {
												'bsonType' : 'string',
												'description' : 'if the student has responsibilities.',
												'enum' : ['low', 'average', 'high']
											},
									"communication_engagement" : {
													'bsonType' : 'string',
													'description' : 'student ability to engage in communication.',
													'enum' : ['low', 'average', 'good']
												},
									"aggression_control" : {
												'bsonType' : 'string',
												'description' : 'student ability to control aggretion.',
												'enum' : ['low', 'average', 'good'] 
											},
									"distractive_nature" : {
												'bsonType' : 'bool',
												'description' : 'is the student pron to distraction.',
										}
							}
}

#sub-schema for psyciatrist details#
psyciatrist_details = {
						'bsonType' : 'object',
						'description' : 'Psyciatrist details',
						'required' : [
								"psycriatist_name",
								"aadhar/pan/passport",
								"license_num",
								"practice_org",
								"signature",
								"_timestamp"
							],
						'properties' : {
									"psycriatist_name" : {
											'bsonType' : 'string',
											'description' : 'name of the psyciatriest'
										},
									"aadhar/pan/passport" : {
													'bsonType' : 'string',
													'description' : 'psyciatrist aadhar/pan/passport clear image.'
											},
									"license_num" : {
												'bsonType' : 'string',
												'description' : 'psyciatrist unique license num.'
											},
									"practice_org" : {
												'bsonType' : 'string',
												'description' : 'organization name in which psyciatrist is working.'
											},
									"signature" : {
											'bsonType' : 'string',
											'description' : 'handwritten signature image as per bank passbook.'
										},
									"_timestamp" : {
												'bsonType' : 'timestamp',
												'description' : 'meeting time.'
										}
							}
}

#sub-schema for psycriatist session monitoring faculty#
psycriatist_session_monitoring_faculty = {
									'bsonType' : 'object',
									'description' : 'faculty details for monitoring psycriatist session.',
									'required' : [
											"faculty_name",
											"faculty_id_image",
											"aadhar/pan/passport_image",
											"signature_image",
											"faculty_passport_size_image" 
										],
									'properties' : {
												"faculty_name" : {
															'bsonType' : 'string',
															'description' : 'session monitoring faculty name.'
														},
												"faculty_id_image" : {
															'bsonType' : 'string',
															'description' : 'faculty work id image.'
														},
												"aadhar/pan/passport_image" : {
																'bsonType' : 'string',
																'description' : 'faculty national id clear image.'
														},
												"signature_image" : {
															'bsonType' : 'string',
															'description' : 'handwritten signature image as per bank passbook.'
														},
												"faculty_passport_size_image" : {
																	'bsonType' : 'string',
																	'description' : 'current passport size image of faculty.'
															}
										}
}

##main schema
student_mental_health_schema = {
								'bsonType' : 'object',
								'description' : 'student mental health record.',
								'required' : [
										"_id",
										"student_psyciatrist_meet_video",
										"type_of_concelling",
										"student_appearance",
										"level_of_conciousness",
										"speech_and_mood",
										"attitude_and_insights",
										"psyciatrist_details",
										"session_monitoring_faculty"
									],
								'properties' : {
											"_id" : {
													'bsonType' : 'objectId',
													'description' : 'unique id for each psyciatrist session.'
												},
											"student_psyciatrist_meet_video" : {
																'bsonType' : 'string',
																'description' : 'student & psyciatrist meeting video.'
															},
											"type_of_councelling" : {
															'bsonType' : 'string',
															'description' : 'type of councelling.',
															'enum' : ['scheduled', 'emergency']
													},
											"student_appearance" : student_appearance,
											"level_of_conciousness" : level_of_conciousness,
											"speech_and_mood" : speech_and_mood,
											"attitude_and_insights" : attitude_and_insight,
											"psyciatrist_details" : psyciatrist_details,
											"session_monitoring_faculty" : psycriatist_session_monitoring_faculty
									}
}