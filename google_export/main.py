import httpx
import json
import csv
import argparse


def get_awards_by_id(user_id: str | int, key: str, timeout) -> set:
    try:
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
        data = json.loads(c)
        award_titles = {
            award.get('badge', {}).get('title', None)
            for award in data.get('awards', {}) # this line handles bad ids (if err -> no rewards -> 0 on public profile column)
        }
        return award_titles
    except httpx.ConnectError:
        print('ConnectError')
        return set()


def get_awards(ids: [str | int], key: str, timeout) -> dict[set]:
    awards = {user_id: get_awards_by_id(user_id, key, timeout) for user_id in ids}
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='developers.google.com badges exporter',
    )
    parser.add_argument('-o', '--output', default='result.csv')
    parser.add_argument('-i', '--ids_file')
    parser.add_argument('-k', '--key')
    parser.add_argument('-t', '--timeout', type=float, default=1)
    args = parser.parse_args()

    with open(args.ids_file) as file:
        lines = [line.rstrip() for line in file]
    ids = map(int, lines)
    q = get_awards(ids, args.key, args.timeout)
    write_to_local_csv(q, args.output)
