import bson
import datetime
#from FramesList import createFramesList

input1 = {
				'name' : "Jayanta Roy",
				'id' : "GEU23",
				'Gender' : "Male",
				'course' : "M.Tech(CSE)",
				'student_record' : [],
				'Parental_Education_Level' : "PostGraduation",
				'Family_Income' : "Medium",
				'Learning_Disabilities' : "No",
				'email' : "jayanta.roy@outlook.com",
				'contact' : "7308994920"
	}


mental_health_record = {
			'_id' : bson.objectid.ObjectId(),
			'student_psyciatrist_meet_video' : r"C:\Users\Jayanta\Videos\VSDC Free Screen Recorder\FairCompute-Assignment.mp4",
			'type_of_councelling' : "scheduled",
			'student_appearance' : {
							'physical_determinents' : {
											'sociability' : "good",
											'impulsivity_level' : "average",
											'emotional_intelligence_level' : "good",
											'physical_features' : {'height' : 5.8, 'weight' : 72},
											'medical_test_report' : r"C:\Users\Jayanta\Downloads\dokumen.pub_quantum-information-processing-quantum-computing-and-quantum-error-correction-an-engineering-approach-2nbsped-9780128219829.pdf"
										},
							'intellectual_determinents' : {
											'reasoning_skills' : "good",
											'problem_solving_skill' : "good",
											'decision_making_skill' : "good",
											'critical_thinking_skill' : "good",
											'memory_capacity' : "average",
											'belief' : "average"
										},
							'social_determinents' : {
											'friendcircle' : "large",
											'socialmedia/ott_access' : {
															'yes/no?' : "yes",
															'sites' : ["fb", "tik-tok"],
															'content_types' : ["horror","action"]
															},
											'speech_style' : "polite",
											'judgement_capability' : "good",
											'nature' : "jolly"
										}
						},
			'level_of_conciousness' : {
							'eye_response' : 6,
							'verbal_response' : 7,
							'motor_response' : 8,
							'facial_trauma' : False
						},
			'speech_and_mood' : {
						'speech_status' : "positive",
						'mood_status' : "positive"
					},
			'attitude_and_insights' : {
							'responsibilities': "low",
							'communication_engagement': "good",
							'aggression_control': "good",
							'distractive_nature': False
						},
			'psyciatrist_details' : {
							'psycriatist_name' : "Dr. Arijit Sankar",
							'aadhar/pan/passport' : r"C:\Users\Jayanta\Downloads\dokumen.pub_quantum-information-processing-quantum-computing-and-quantum-error-correction-an-engineering-approach-2nbsped-9780128219829.pdf",
							'license_num' : "NSG-055-210",
							'practice_org' : "Narciat Psyco Agency Hospitals",
							'signature' : r"C:\Users\Jayanta\Downloads\dokumen.pub_quantum-information-processing-quantum-computing-and-quantum-error-correction-an-engineering-approach-2nbsped-9780128219829.pdf",
							'_timestamp' : datetime.datetime.now()
						},
			'session_monitoring_faculty' : {
									'faculty_name' : "Ms. Arpita Kishor",
									'faculty_id_image' : r"C:\Users\Jayanta\Downloads\dokumen.pub_quantum-information-processing-quantum-computing-and-quantum-error-correction-an-engineering-approach-2nbsped-9780128219829.pdf",
									'aadhar/pan/passport_image' : r"C:\Users\Jayanta\Downloads\dokumen.pub_quantum-information-processing-quantum-computing-and-quantum-error-correction-an-engineering-approach-2nbsped-9780128219829.pdf",
									'signature_image' : r"C:\Users\Jayanta\Downloads\dokumen.pub_quantum-information-processing-quantum-computing-and-quantum-error-correction-an-engineering-approach-2nbsped-9780128219829.pdf",
									'faculty_passport_size_image' : r"C:\Users\Jayanta\Downloads\dokumen.pub_quantum-information-processing-quantum-computing-and-quantum-error-correction-an-engineering-approach-2nbsped-9780128219829.pdf"
								}
	}

semester1 = {
		'_id': bson.objectid.ObjectId(),
		'semester' : "1",
		'Exam_Score' : 0,
		'Hours_Studied' : 0,
		'Attendence' : 0,
		'Parental_Involvement' : "Yes",
		'Access_to_Resources' : "Low",
		'Extracurricular_Activity' : 3,
		'Tutoring_Sessions' : 7,
		'Teacher_Quality' : 'Medium',
		'GPA' : 0,
		'CGPA' : 0,
		'student_mental_health_record' : [],
		'date' : datetime.datetime.now()
	}


###upload emergency mental health meet with psyciatrist
emergency_mental_health_record = {
			'_id' : bson.objectid.ObjectId(),
			'student_psyciatrist_meet_video' : r"C:\Users\Jayanta\Videos\VSDC Free Screen Recorder\FairCompute-Assignment.mp4",
			'type_of_concelling' : "emergency",
			'student_appearance' : {
							'physical_determinents' : {
											'sociability' : "good",
											'impulsivity_level' : "average",
											'emotional_intelligence_level' : "good",
											'physical_features' : {'height' : 5.8, 'weight' : 72},
											'medical_test_report' : r"C:\Users\Jayanta\Downloads\dokumen.pub_quantum-information-processing-quantum-computing-and-quantum-error-correction-an-engineering-approach-2nbsped-9780128219829.pdf"
										},
							'intellectual_determinents' : {
											'reasoning_skills' : "good",
											'problem_solving_skill' : "good",
											'decision_making_skill' : "good",
											'critical_thinking_skill' : "good",
											'memory_capacity' : "average",
											'belief' : "average"
										},
							'social_determinents' : {
											'friendcircle' : "large",
											'socialmedia/ott_access' : {
															'yes/no?' : "yes",
															'sites' : ["fb", "tik-tok"],
															'content_types' : ["horror","action"]
															},
											'speech_style' : "polite",
											'judgement_capability' : "good",
											'nature' : "jolly"
										}
						},
			'level_of_conciousness' : {
							'eye_response' : 6,
							'verbal_response' : 7,
							'motor_response' : 8,
							'facial_trauma' : False
						},
			'speech_and_mood' : {
						'speech_status' : "positive",
						'mood_status' : "positive"
					},
			'attitude_and_insights' : {
							'responsibilities': "low",
							'communication_engagement': "good",
							'aggression_control': "good",
							'distractive_nature': False
						},
			'psyciatrist_details' : {
							'psycriatist_name' : "Dr. Arijit Sankar",
							'aadhar/pan/passport' : r"C:\Users\Jayanta\Downloads\dokumen.pub_quantum-information-processing-quantum-computing-and-quantum-error-correction-an-engineering-approach-2nbsped-9780128219829.pdf",
							'license_num' : "NSG-055-210",
							'practice_org' : "Narciat Psyco Agency Hospitals",
							'signature' : r"C:\Users\Jayanta\Downloads\dokumen.pub_quantum-information-processing-quantum-computing-and-quantum-error-correction-an-engineering-approach-2nbsped-9780128219829.pdf",
							'_timestamp' : datetime.datetime.now()
						},
			'session_monitoring_faculty' : {
									'faculty_name' : "Ms. Arpita Kishor",
									'faculty_id_image' : r"C:\Users\Jayanta\Downloads\dokumen.pub_quantum-information-processing-quantum-computing-and-quantum-error-correction-an-engineering-approach-2nbsped-9780128219829.pdf",
									'aadhar/pan/passport_image' : r"C:\Users\Jayanta\Downloads\dokumen.pub_quantum-information-processing-quantum-computing-and-quantum-error-correction-an-engineering-approach-2nbsped-9780128219829.pdf",
									'signature_image' : r"C:\Users\Jayanta\Downloads\dokumen.pub_quantum-information-processing-quantum-computing-and-quantum-error-correction-an-engineering-approach-2nbsped-9780128219829.pdf",
									'faculty_passport_size_image' : r"C:\Users\Jayanta\Downloads\dokumen.pub_quantum-information-processing-quantum-computing-and-quantum-error-correction-an-engineering-approach-2nbsped-9780128219829.pdf"
								}
	}