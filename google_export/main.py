import httpx
import json
import csv
import argparse
import os
import subprocess


def get_name(user_id: str, curl_args):
    try:
        if type(user_id) != str or user_id.isdigit():
            status, output = subprocess.getstatusoutput(
                f'''curl 'https://developerprofiles-pa.clients6.google.com/$rpc/google.internal.developerprofiles.v1.profile.ProfileService/GetPublicProfile' --compressed -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br, zstd' -H 'X-Goog-Api-Key: AIzaSyAP-jjEJBzmIyKR4F-3XITp8yM9T1gEEI8' -H 'X-Goog-AuthUser: 0' -H 'Authorization: ' -H 'Content-Type: application/json+protobuf' -H 'X-User-Agent: grpc-web-javascript/0.1' -H 'Origin: https://developers.google.com' -H 'DNT: 1' -H 'Sec-GPC: 1' -H 'Connection: keep-alive' -H 'Referer: https://developers.google.com/' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-site' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'TE: trailers' -s --data-raw '["{user_id}"]' '''
            )
        else:
            status, output = subprocess.getstatusoutput(
                f'''curl 'https://developerprofiles-pa.clients6.google.com/$rpc/google.internal.developerprofiles.v1.profile.ProfileService/GetPublicProfile'  --compressed -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br, zstd' -H 'X-Goog-Api-Key: {curl_args}' -H 'X-Goog-AuthUser: 0' -H 'Authorization: ' -H 'Content-Type: application/json+protobuf' -H 'X-User-Agent: grpc-web-javascript/0.1' -H 'Origin: https://developers.google.com' -H 'DNT: 1' -H 'Sec-GPC: 1' -H 'Connection: keep-alive' -H 'Referer: https://developers.google.com/' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-site' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -s --data-raw '[null,null,"{user_id}"]' '''
            )  # curl because libs don't work
        user_id = json.loads(
            output
        )
        user_id = user_id[1][4][0]
        return user_id
    except httpx.ConnectError:
        print('ConnectError')
    return ""

def get_link(user_id: str, curl_args):
    try:
        if type(user_id) != str or user_id.isdigit():
            status, output = subprocess.getstatusoutput(
                f'''curl 'https://developerprofiles-pa.clients6.google.com/$rpc/google.internal.developerprofiles.v1.profile.ProfileService/GetPublicProfile' --compressed -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br, zstd' -H 'X-Goog-Api-Key: AIzaSyAP-jjEJBzmIyKR4F-3XITp8yM9T1gEEI8' -H 'X-Goog-AuthUser: 0' -H 'Authorization: ' -H 'Content-Type: application/json+protobuf' -H 'X-User-Agent: grpc-web-javascript/0.1' -H 'Origin: https://developers.google.com' -H 'DNT: 1' -H 'Sec-GPC: 1' -H 'Connection: keep-alive' -H 'Referer: https://developers.google.com/' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-site' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'TE: trailers' -s --data-raw '["{user_id}"]' '''
            )
        else:
            status, output = subprocess.getstatusoutput(
                f'''curl 'https://developerprofiles-pa.clients6.google.com/$rpc/google.internal.developerprofiles.v1.profile.ProfileService/GetPublicProfile'  --compressed -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br, zstd' -H 'X-Goog-Api-Key: {curl_args}' -H 'X-Goog-AuthUser: 0' -H 'Authorization: ' -H 'Content-Type: application/json+protobuf' -H 'X-User-Agent: grpc-web-javascript/0.1' -H 'Origin: https://developers.google.com' -H 'DNT: 1' -H 'Sec-GPC: 1' -H 'Connection: keep-alive' -H 'Referer: https://developers.google.com/' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-site' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -s --data-raw '[null,null,"{user_id}"]' '''
            )  # curl because libs don't work
        user_id = json.loads(
            output
        )
        user_id = user_id[-1][-1]
        return user_id
    except httpx.ConnectError:
        print('ConnectError')
    return ""

def get_id_by_name(user_id: str, curl_args):
    if type(user_id) != str or user_id.isdigit():
        return user_id
    status, output = subprocess.getstatusoutput(
        f'''curl 'https://developerprofiles-pa.clients6.google.com/$rpc/google.internal.developerprofiles.v1.profile.ProfileService/GetPublicProfile'  --compressed -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br, zstd' -H 'X-Goog-Api-Key: {curl_args}' -H 'X-Goog-AuthUser: 0' -H 'Authorization: ' -H 'Content-Type: application/json+protobuf' -H 'X-User-Agent: grpc-web-javascript/0.1' -H 'Origin: https://developers.google.com' -H 'DNT: 1' -H 'Sec-GPC: 1' -H 'Connection: keep-alive' -H 'Referer: https://developers.google.com/' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-site' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -s --data-raw '[null,null,"{user_id}"]' '''
    )  # curl because libs don't work
    user_id = json.loads(
        output
    )
    user_id = user_id[1][31]
    return user_id

def get_awards_by_id(user_id: str | int, key: str, curl_args, timeout) -> dict:
    print(f'Processing id {user_id}')
    try:
        if not (type(user_id) != str or user_id.isdigit()):
            user_id = get_id_by_name(user_id, curl_args)
            
        c = httpx.get(f'https://developerprofiles-pa.clients6.google.com/v1/awards?access_token&locale&obfuscatedProfileId={user_id}&useBadges=true&key={key}',
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'X-JavaScript-User-Agent': 'google-api-javascript-client/1.1.0',
                'X-Requested-With': 'XMLHttpRequest',
                'X-Goog-Encode-Response-If-Executable': 'base64',
                'X-ClientDetails': '''appVersion=5.0%20(X11)&platform=Linux%20x86_64&userAgent=Mozilla%2F5.0%20(X11%3B%20Linux%20x86_64%3B%20rv%3A128.0)%20Gecko%2F20100101%20Firefox%2F128.0''',
                'Origin': 'https://developers.google.com',
                'DNT': '1',
                'Sec-GPC': '1',
                'Connection': 'keep-alive',
                'Referer': 'https://developers.google.com',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'TE': 'trailers',
            },
            timeout=timeout
        ).text
        # print(
        #     c
        # )
        data = json.loads(c)
        award_titles = {
            award.get('badge', {}).get('title', None): award.get('createTime', {})
            for award in data.get('awards', {}) # this line handles bad ids (if err -> no rewards -> 0 on public profile column)
        }
        return award_titles
    except httpx.ConnectError:
        print('ConnectError')
        return {}


def get_awards(ids: [str | int], key: str, curl_args, timeout) -> dict[set]:
    awards = {user_id: get_awards_by_id(user_id, key, curl_args, timeout) for user_id in ids}
    return awards


def write_to_local_csv(awards: dict[set], curl_args, fname: str = 'result.csv') -> None:
    column_names = set()
    default_columns = [
        'id', 
        'name', 
        'link',
        'public_profile', 
        'profile created', 
    ]

    for user_awards in awards.values():
        column_names.update(user_awards)
    column_names = default_columns + list(column_names)
    with open(fname, 'w', newline='') as csvfile:
        award_writer = csv.writer(csvfile)
        award_writer.writerow(
            column_names
        )
        rows = []
        for user_awards in awards.items():
            row = [
                get_id_by_name(user_awards[0], curl_args),
                get_name(user_awards[0], curl_args),
                get_link(user_awards[0], curl_args),
                1 if len(user_awards[1]) else 0, 
                user_awards[1].get('Joined the Google Developer Program'), 
            ]
            for award_name in column_names[len(default_columns):]:
                row.append(user_awards[1][award_name] if award_name in user_awards[1] else 'No')
            rows.append(tuple(row))
        for row in set(rows):
            award_writer.writerow(
                row
            )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='developers.google.com badges exporter',
    )
    parser.add_argument('-o', '--output', default='result.csv')
    parser.add_argument('-i', '--ids_file')
    parser.add_argument('-k', '--key')
    parser.add_argument('-c', '--curl_args')
    parser.add_argument('-t', '--timeout', type=float, default=1)
    args = parser.parse_args()

    with open(args.ids_file) as file:
        lines = [line.rstrip() for line in file]
    # ids = lines
    q = get_awards(lines, args.key, args.curl_args, args.timeout)
    write_to_local_csv(q, args.curl_args, args.output)
