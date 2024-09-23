import httpx
import json
import csv
import argparse


def get_awards_by_id(user_id: str | int) -> set:
    c = httpx.get(f'https://developerprofiles-pa.clients6.google.com/v1/awards?access_token&locale&obfuscatedProfileId={user_id}&useBadges=true&key=AIzaSyAP-jjEJBzmIyKR4F-3XITp8yM9T1gEEI8&%24unique=gc537',
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
        }
    ).text
    data = json.loads(c)
    award_titles = {
        award.get('badge', {}).get('title', None)
        for award in data.get('awards', {})
    }
    return award_titles


def get_awards(ids) -> dict[set]:
    awards = {user_id: get_awards_by_id(user_id) for user_id in ids}
    return awards


def write_to_local_csv(awards: dict[set], fname: str = 'result.csv') -> None:
    column_names = set()
    default_columns = ['id', 'public_profile']

    for user_awards in awards.values():
        column_names.update(user_awards)
    column_names = default_columns + list(column_names)
    with open(fname, 'w', newline='') as csvfile:
        award_writer = csv.writer(csvfile)
        award_writer.writerow(
            column_names
        )
        for user_awards in awards.items():
            row = [user_awards[0], 1 if len(user_awards[1]) else 0]
            for award_name in column_names[len(default_columns):]:
                row.append(1 if award_name in user_awards[1] else 0)
            award_writer.writerow(
                row
            )


parser = argparse.ArgumentParser(
    prog='developers.google.com badges exporter',
)
parser.add_argument('-o', '--output', default='result.csv')
parser.add_argument('-i', '--ids')


if __name__ == '__main__':
    args = parser.parse_args()
    ids = map(int, args.ids.split())
    q = get_awards(ids)
    write_to_local_csv(q, args.output)
