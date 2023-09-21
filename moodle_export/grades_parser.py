#!/usr/bin/python3
import sheets
import requests
import json
import datetime
import csv
import args_parser

HEADERS = {
    "Content-Type": "charset=iso-8859"
}


def main():
    args = args_parser.arg_parser()
    for course_id in args.course_id:
        with requests.Session() as s:
            # get enrolled users
            res_users = s.get(args.url + '/webservice/rest/server.php?wstoken=' + args.moodle_token +
                              '&wsfunction=core_enrol_get_enrolled_users&courseid=' + course_id + '&moodlewsrestformat=json',
                              headers=HEADERS, verify=False)
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
                users_params[str(item["id"])] = {"users_last_accessed": str(lastdate), "username": item.get("username", "-"),  "email": item.get("email", "-")}

                if 'customfields' in item:
                    users_params[str(item["id"])]["github"] = item['customfields'][0].get("value", "-")
                else:
                    users_params[str(item["id"])]["github"] = "-"

            # get grades
            res_grades = s.get(args.url + '/webservice/rest/server.php?wstoken=' + args.moodle_token +
                               '&wsfunction=gradereport_user_get_grades_table&courseid=' + course_id + '&moodlewsrestformat=json',
                               headers=HEADERS, verify=False)

            # check status code
            if res_grades.status_code != 200:
                raise SystemExit("Request error, response status code: " + str(res_grades.status_code))

            grades = json.loads(res_grades.text)

            # check if request is valid
            if "message" in grades:
                raise SystemExit("Error: " + grades["message"])

            # parse needed grades data
            grades_data = []
            for person in grades["tables"]:
                flag = ''
                person_grades = {}
                person_grades["userid"] = person["userid"]
                person_grades["last_access"] = users_params[str(person_grades["userid"])]["users_last_accessed"]
                person_grades["username"] = users_params[str(person_grades["userid"])]["username"]
                person_grades["email"] = users_params[str(person_grades["userid"])]["email"]
                if args.options:
                    for i in args.options:
                        if i == 'github':
                            person_grades["github"] = users_params[str(person_grades["userid"])]["github"]
                person_grades["userfullname"] = person["userfullname"]
                person_grades["activities"] = []
                print("userid: " + str(person_grades["userid"]) + " fullname: " + person_grades["userfullname"])
                for activities in person["tabledata"]:
                    if type(activities) != list:
                        activity = {}
                        activity_name = activities["itemname"]["content"].partition("title=\"")[2].split("\" ")[0]
                        print(activity_name)
                        activity_str1 = "activity "
                        activity_str0 = "» "
                        if activity_name == "Course total":
                            flag = 'en'
                            activity["activity_name"] = "total"
                        elif activity_name == "Итоговая оценка за курс":
                            flag = 'ru'
                            activity["activity_name"] = "total"
                        elif flag == 'en':
                            activity["activity_name"] = activity_name[
                                                        activity_name.find(activity_str1) + len(activity_str1):]
                        elif flag == 'ru':
                            activity["activity_name"] = activity_name[
                                                        activity_name.find(activity_str0) + len(activity_str0):]
                        if flag != '':
                            activity["grade"] = activities["grade"]["content"]
                            activity["percentage"] = activities["percentage"]["content"]
                            activity["contributiontocoursetotal"] = activities["contributiontocoursetotal"]["content"]
                            person_grades["activities"].append(activity)
                grades_data.append(person_grades)
  
            if len(grades_data) == 0:
                print("No solutions in course, nothing to export. Exiting")
                return

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
                if args.options:
                    for i in args.options:
                        if i == 'github':
                            person_grades["github"] = item["github"]
                person_grades["last_access"] = item["last_access"]
                for activity in item["activities"]:
                    person_grades[activity["activity_name"]] = activity[grades_type]
                grades_for_table.append(person_grades)

            # output data to csv file
            csv_path = args.csv_path + '_' + course_id + '.csv'
            with open(csv_path, 'w', encoding='UTF8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=grades_for_table[0].keys())
                writer.writeheader()
                writer.writerows(grades_for_table)

            # if args specified write data to sheets document
            for i in range(0, len(args.table_id)):
                if args.course_id[i] == course_id:
                    table_id = args.table_id[i]
                    break
                elif i == len(args.table_id) - 1:
                    table_id = args.table_id[i]

            if args.sheet_id:
                for i in range(0, len(args.sheet_id)):
                    if args.course_id[i] == course_id:
                        sheet_id = args.sheet_id[i]
                        break
                    else:
                        sheet_id = args.sheet_id[i] + ' ' + course_id
            else:
                sheet_id = 'course ' + course_id

            sheets.write_data_to_table(csv_path, args.google_token, table_id, sheet_id)


if __name__ == "__main__":
    main()
