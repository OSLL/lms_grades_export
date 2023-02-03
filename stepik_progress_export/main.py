import os

import pandas as pd
import requests
from dynaconf import Dynaconf
from tqdm import tqdm

settings = Dynaconf(settings_files=["config.toml"])


def get_access_token():
    response = requests.post(
        "https://stepik.org/oauth2/token/",
        data={"grant_type": "client_credentials"},
        auth=(settings.stepik.client_id, settings.stepik.client_secret),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()
    data = response.json()
    return data["access_token"]


def get_grade_list(access_token):
    results = []
    page = 1
    with tqdm(desc="Grade list") as t:
        while True:
            response = requests.get(
                "https://stepik.org/api/course-grades",
                params={
                    "page": page,
                    "page_size": 10,
                    "course": settings.stepik.course_id,
                    "klass": settings.stepik.class_id,
                },
                headers={"Authorization": f"BEARER {access_token}"},
            )
            response.raise_for_status()
            data = response.json()
            results.extend(data["course-grades"])
            if not data["meta"]["has_next"]:
                break
            t.update()
            page += 1

    return results


def get_submissions(access_token, step_id, user_id):
    page = 1
    results = []
    while True:
        response = requests.get(
            "https://stepik.org/api/submissions",
            params={
                "page": page,
                "page_size": 10,
                "klass": settings.stepik.class_id,
                "order": "desc",
                "step": step_id,
                "search": f"id:{user_id}",
            },
            headers={"Authorization": f"BEARER {access_token}"},
        )
        response.raise_for_status()
        data = response.json()
        results.extend(data["submissions"])
        if not data["meta"]["has_next"]:
            break
        page += 1
    return results


def get_step_ids(data):
    steps_ids = []

    for datum in data:
        for step_datum in datum["results"].values():
            steps_ids.append(step_datum["step_id"])

    return sorted(list(set(steps_ids)))


def get_info(access_token):
    data = get_grade_list(access_token)
    step_ids = get_step_ids(data)

    is_read = {}

    if os.path.exists("res.csv"):
        df = pd.read_csv("res.csv")
        for _, datum in df.iterrows():
            user_id = datum["user_id"]
            for step_id in step_ids:
                if not pd.isna(datum.get(str(step_id), None)):
                    is_read[f"{user_id}-{step_id}"] = datum.get(str(step_id))

    # print(is_read)

    results = []
    for i in range(len(data)):
        datum = data[i]
        user_id = datum["user"]
        print(f"user_id: {user_id} [{i} / {len(data)}]")

        user_datum = {
            "user_id": user_id,
            "score": datum["score"],
            "date_joined": datum["date_joined"],
        }

        for result in tqdm(list(datum["results"].values())):
            step_id = result["step_id"]
            key = f"{user_id}-{step_id}"
            if key in is_read:
                user_datum[str(step_id)] = is_read[key]
                continue
            submissions = get_submissions(access_token, step_id, user_id)
            for submission in submissions:
                if submission["status"] == "correct":
                    user_datum[str(step_id)] = submission["time"]
                    break
        results.append(user_datum)

    df = pd.DataFrame(
        results,
        columns=["user_id", "score", "date_joined", *[str(id_) for id_ in step_ids]],
    )

    return df


if __name__ == "__main__":
    token = get_access_token()
    df = get_info(token)
    df.to_csv("res.csv")
