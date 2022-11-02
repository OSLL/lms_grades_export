#!/usr/bin/python3
import re

import sheets
import requests
import json
import datetime
import csv
import args_parser
from bs4 import BeautifulSoup

HEADERS = {
    "Content-Type": "charset=iso-8859"
}

def sort_id(cats, modules):
    sorted_ids = [0]
    for module in modules:
        for i in range(len(cats)):
            if module == cats[i]:
                sorted_ids.append(i+1)
                continue
    return sorted_ids

def sort_modules(acts, sorted_steps):
    sorted_acts = []
    for i in sorted_steps:
        sorted_acts.append(acts[i])
    return sorted_acts

def main():
    args = args_parser.arg_parser()
    for course_id in args.course_id:
        with requests.Session() as s:
            # get enrolled users
            print('Get users data')
            res_users = s.get(args.url + '/webservice/rest/server.php?wstoken=' + args.moodle_token +
                              '&wsfunction=core_enrol_get_enrolled_users&courseid=' + course_id + '&moodlewsrestformat=json',
                              headers=HEADERS)

            # check status code
            if res_users.status_code != 200:
                raise SystemExit("Request error, response status code: " + str(res_users.status_code))

            users = json.loads(res_users.text)
            # check if request is valid
            if type(users) != list:
                raise SystemExit("Error: " + users["message"])

            # save last accessed time for each user
            print('Parse users data')
            users_params = {}
            for item in users:
                lastdate = datetime.datetime.fromtimestamp(item['lastcourseaccess']).strftime('%Y-%m-%d %H:%M:%S')
                users_params[str(item["id"])] = {"users_last_accessed": str(lastdate), "username": item.get("username", "-"),  "email": item.get("email", "-")}

                if 'customfields' in item:
                    users_params[str(item["id"])]["github"] = item['customfields'][0].get("value", "-")
                else:
                    users_params[str(item["id"])]["github"] = "-"

            # get grades
            print('Get grades data')
            res_grades = s.get(args.url + '/webservice/rest/server.php?wstoken=' + args.moodle_token +
                               '&wsfunction=gradereport_user_get_grades_table&courseid=' + course_id + '&moodlewsrestformat=json',
                               headers=HEADERS)

            # check status code
            if res_grades.status_code != 200:
                raise SystemExit("Request error, response status code: " + str(res_grades.status_code))

            grades = json.loads(res_grades.text)

            # check if request is valid
            if "message" in grades:
                raise SystemExit("Error: " + grades["message"])

            # get modules
            if args.options:
                for i in args.options:
                    if i == 'sort':
                        print('Get modules')
                        course_content = s.get(args.url + '/webservice/rest/server.php?wstoken=' + args.moodle_token +
                                               '&wsfunction=core_course_get_contents&courseid=' + course_id + '&moodlewsrestformat=json',
                                               headers=HEADERS)

                        # check status code
                        if course_content.status_code != 200:
                            raise SystemExit("Request error, response status code: " + str(course_content.status_code))

                        content = json.loads(course_content.text)

                        # check if request is valid
                        if "message" in content:
                            raise SystemExit("Error: " + content["message"])

                        # get sorted modules
                        modules = []
                        for topics in content:
                            for module in topics['modules']:
                                modules.append(str(module['id']))

            # parse needed grades data
            print('Parse grades data')
            grades_data = []
            cats = []
            sorted_steps = []
            if_sorted = False
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
                person_grades_activities = []
                person_grades["activities"] = []
                for activities in person["tabledata"]:
                    if type(activities) != list:
                        activity = {}
                        activity_name = activities["itemname"]["content"].partition("title=\"")[2].split("\" ")[0]
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
                            if not if_sorted and args.options and activity["activity_name"] != "total":
                                for i in args.options:
                                    if i == 'sort':
                                        a = activities["itemname"]["content"].split('php?id=')[1]
                                        cats.append(re.split(r'"|&', a)[0])
                            activity["grade"] = activities["grade"]["content"]
                            activity["percentage"] = activities["percentage"]["content"]
                            activity["contributiontocoursetotal"] = activities["contributiontocoursetotal"]["content"]
                            person_grades_activities.append(activity)
                if args.options:
                    for i in args.options:
                        if i == 'sort' and not if_sorted:
                            print('Sort modules')
                            sorted_steps = sort_id(cats, modules)
                            person_grades["activities"] = sort_modules(person_grades_activities, sorted_steps)
                            if_sorted = True
                        elif i == 'sort':
                            person_grades["activities"] = sort_modules(person_grades_activities, sorted_steps)
                        else:
                            person_grades["activities"] = person_grades_activities
                else:
                    person_grades["activities"] = person_grades_activities
                grades_data.append(person_grades)

            # form suitable structure for output to sheets
            print('Prepare data for publishing')
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

            print('Data published! Check list: ' + sheet_id)
            sheets.write_data_to_table(csv_path, args.google_token, table_id, sheet_id)


if __name__ == "__main__":
    main()
