#!/usr/bin/python3
import sheets
import requests
import json
import datetime
import csv
import args_parser

HEADERS = {
    "Content-Type" : "charset=iso-8859"
}


def main():
    args = args_parser.arg_parser()
    with requests.Session() as s:
        # get enrolled users
        res_users = s.get(args.url + '/webservice/rest/server.php?wstoken=' + args.moodle_token +
                '&wsfunction=core_enrol_get_enrolled_users&courseid='+ str(args.course_id) +'&moodlewsrestformat=json',
                headers=HEADERS)
        # check status code
        if res_users.status_code != 200:
            raise SystemExit("Request error, response status code: " + str(res_users.status_code))

        users = json.loads(res_users.text)
        # check if request is valid
        if type(users) != list:
            raise SystemExit("Error: " + users["message"])

        # save last accessed time for each user
        users_params = {}
        for item in users:
            lastdate = datetime.datetime.fromtimestamp(item['lastcourseaccess']).strftime('%Y-%m-%d %H:%M:%S')
            users_params[str(item["id"])] = {"users_last_accessed": str(lastdate),
                                             "username": item['username'], "email": item['email'],
                                             "github": item['customfields'][0]["value"]}
        #print(users_params)

        # get grades
        grades = ''
        res_grades = s.get(args.url + '/webservice/rest/server.php?wstoken=' + args.moodle_token +
                '&wsfunction=gradereport_user_get_grades_table&courseid='+ str(args.course_id) +'&moodlewsrestformat=json',
                headers=HEADERS)
        # check status code 
        if res_grades.status_code != 200:
            raise SystemExit("Request error, response status code: " + str(res_grades.status_code))

        grades = json.loads(res_grades.text)
        #print(grades)
        # check if request is valid
        if "message" in grades:
            raise SystemExit("Error: " + grades["message"])

        # parse needed grades data
        grades_data = []
        for person in grades["tables"]:
            person_grades = {}
            person_grades["userid"] = person["userid"]
            person_grades["last_access"] = users_params[str(person_grades["userid"])]["users_last_accessed"]
            person_grades["username"] = users_params[str(person_grades["userid"])]["username"]
            person_grades["email"] = users_params[str(person_grades["userid"])]["email"]
            for i in args.options:
                if i == 'github':
                    person_grades["github"] = users_params[str(person_grades["userid"])]["github"]
            person_grades["userfullname"] = person["userfullname"]
            person_grades["activities"] = []
            print("userid: " + str(person_grades["userid"]) + " fullname: " + person_grades["userfullname"])
            for activities in person["tabledata"]:
                if type(activities) != list:
                    activity_name = activities["itemname"]["content"].partition("title=\"")[2].split("\" ")[0]
                    activity_str = "activity "
                    if activity_name.find(activity_str) != -1 or activity_name == "Course total":
                        activity = {}
                        if activity_name == "Course total":
                            activity["activity_name"] = "total"
                        else:
                            activity["activity_name"] = activity_name[activity_name.find(activity_str) + len(activity_str) :]
                        activity["grade"] = activities["grade"]["content"]
                        activity["percentage"] = activities["percentage"]["content"]
                        activity["contributiontocoursetotal"] = activities["contributiontocoursetotal"]["content"]
                        person_grades["activities"].append(activity)
            grades_data.append(person_grades)

        # form suitable structure for output to sheets
        grades_for_table = []
        grades_type = "grade"
        if args.percentages:
            grades_type = "percentage"

        for item in grades_data:
            person_grades = {}
            person_grades["fullname"] = item["userfullname"]
            person_grades["username"] = item["username"]
            person_grades["email"] = item["email"]
            for i in args.options:
                if i == 'github':
                    person_grades["github"] = item["github"]
            person_grades["last_access"] = item["last_access"]
            for activity in item["activities"]:
                person_grades[activity["activity_name"]] = activity[grades_type]
            grades_for_table.append(person_grades)

        # output data to csv file
        with open(args.csv_path, 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=grades_for_table[0].keys())
            writer.writeheader()
            writer.writerows(grades_for_table)  

        # if args specified write data to sheets document
        sheets.write_data_to_table(args.csv_path, args.google_token, args.table_id, args.sheet_id)


if __name__ == "__main__":
    main()
