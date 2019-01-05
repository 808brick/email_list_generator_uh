import requests
import pandas as pd

def get_class_info(crn):

	# url = requests.get("https://www.sis.hawaii.edu/uhdad/avail.class?i=MAN&t=201930&c=80237")
	url = requests.get("https://www.sis.hawaii.edu/uhdad/avail.class?i=MAN&t=201930&c="+str(crn))
	htmltext = url.text
	# print(htmltext)

	department_start_index = htmltext.find("Subject:")
	department = htmltext[department_start_index:]
	department_start_index = department.find("(")+1
	department_end_index = department.find(")")
	department = department[department_start_index:department_end_index]

	htmltext = htmltext[department_end_index:]

	course_number_start_index = htmltext.find("Course Number:")
	course_number = htmltext[course_number_start_index:]
	course_number_start_index = course_number.find("<b>")+3
	course_number_end_index = course_number.find("</b>")
	course_number = course_number[course_number_start_index:course_number_end_index]

	course_title_start_index = htmltext.find("Course Title:")
	course_title = htmltext[course_title_start_index:]
	course_title_start_index = course_title.find("<b>")+3
	course_title_end_index = course_title.find("</b>")
	course_title = course_title[course_title_start_index:course_title_end_index]

	days_start_index = htmltext.find("Meeting Times:")
	days = htmltext[days_start_index:]
	course_time_start_index = days_start_index
	days_start_index = days.find("<b>")+3
	days_end_index = days.find("</b>")
	days = days[days_start_index:days_end_index].strip()

	course_time = htmltext[course_time_start_index:]
	course_time_start_index = course_time.find("</b>")+4
	course_time = course_time[course_time_start_index:]
	course_time_start_index = course_time.find("&nbsp")+6
	course_time_end_index = course_time.find("</b>")
	course_time = course_time[course_time_start_index:course_time_end_index].strip()

	room_start_index = htmltext.find("Meeting Times:")
	room = htmltext[room_start_index:]
	room_start_index = room.find("&nbsp")
	room = room[room_start_index:]
	room_start_index = room.find("<b>")+3
	room = room[room_start_index:].strip()
	room_start_index = room.find("<b>")+10
	room = room[room_start_index:].strip()
	room_end_index = room.find("</b>")
	room = room[:room_end_index].strip()


	email_start_index = htmltext.find("mailto:")

	email = htmltext[email_start_index:]
	instructor = email
	instructor_start_index = instructor.find(">")+1
	instructor_end_index = instructor.find("<")
	instructor = instructor[instructor_start_index:instructor_end_index]
	email = email.split('"')[0]
	email = email.replace("mailto:", "").lower()

	# print(department)
	# print(course_number)
	# print(course_title)
	# print(email)
	# print(instructor)
	# print(days)
	# print(course_time)
	# print(room)

	return [department, course_number, course_title, days, course_time, room, instructor, email]




crn = []

spreadsheet_data = []
number = 0

def get_crn():
	department = input("\n\nEnter the department abbrviation: (ex: BUS, PHYS)\n").upper()

	print("\n\nPlease wait while the UH class database is being accessed ...\n\n")
	url = requests.get("https://www.sis.hawaii.edu/uhdad/avail.classes?i=MAN&t=201930&s="+department)


	
	courses = []
	number = 0

	print("Enter in a course number, to specify multiple course numbers use a '-' to specify the range ex: 100-396\n")

	while number != "":
		number = input()
		if number == "":
			print("Course CRN numbers found: ")

		elif "-" in number:
			courses.extend(range(int(number.split('-')[0]), int(number.split('-')[1])+1))
			# for num in range(number.split('-')[0], number.split('-')[1]):
			# 	courses.append(num)
		else:
			courses.append(int(number))


	# department_start_index = htmltext.find("Subject:")

	htmltext = url.text

	# print(courses)
	for course in courses:
		num_of_sections = htmltext.count(department + " " + str(course)+'</td>')

		for section in range(num_of_sections):
			# print(num_of_sections)
			section_start_index = htmltext.find(department + " " + str(course)+'</td>')-65
			section_string = htmltext[section_start_index:]
			crn_start_index = section_string.find('</a>')-5
			print(course, " : ", section_string[crn_start_index:crn_start_index+5])
			crn.append(section_string[crn_start_index:crn_start_index+5])
			# print(section_string[:100])
			htmltext = htmltext[section_start_index+75:]

	return crn

indicator = True

while indicator:
	crn = get_crn()
	indicator_prompt = input("\n\nDo you want to add more classes from another department? (y/n)\n")
	if indicator_prompt != "y":
		indicator = False

print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nGathering infromation on classes given, please wait ...\n\n\n\n\n\n\n\n\n\n")
# print(crn)

# print("Enter the CRN number for the courses you want the info of. To select multiple courses use a '-' between the number range. ex: 87543-87548\n\n")
# while number != "":
# 	number = input()
# 	if number == "":
# 		print("\nEnd of input Reached ...\n")

# 	elif "-" in number:
# 		crn.extend(range(int(number.split('-')[0]), int(number.split('-')[1])+1))
# 		# for num in range(number.split('-')[0], number.split('-')[1]):
# 		# 	crn.append(num)
# 	else:
# 		crn.append(int(number))

# print("List: ")
# print(crn)

# checker = input("\n\nAre these CRN numbers correct? (y/n)")

# if checker != 'y':
# 	assert False, 'Please restart the script with the correct CRN numbers'

for course in crn:
	spreadsheet_data.append(get_class_info(course))


pd.DataFrame(spreadsheet_data).to_excel('output.xlsx', header=False, index=False)

print("Finished. Data saved to output.xlsx")
