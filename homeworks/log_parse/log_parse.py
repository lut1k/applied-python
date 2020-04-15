# -*- encoding: utf-8 -*-
import re


def parse(
    ignore_files=False,
    ignore_urls=[],
    start_at=None,
    stop_at=None,
    request_type=None,
    ignore_www=False,
    slow_queries=False
):
    probe_string = '[18/Mar/2018 11:19:40] "GET https://www.sys.mail.ru/calendar/config/254/40263/ HTTP/1.1" 200 965'
    regexp_pattern = (r'^\[(?P<day>0[1-9]|[12][0-9]|3[01])/'
                      r'(?P<month>Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)/'
                      r'(?P<year>(19|20)\d\d)\s{1}'
                      r'(?P<hours>0[0-9]|1[0-9]|2[0-3]):'
                      r'(?P<minutes>[0-5][0-9]):'
                      r'(?P<seconds>[0-5][0-9])\]\s{1}"'
                      r'')
    match = re.search(regexp_pattern, probe_string)
    print(match['day'],
          match['month'],
          match['year'],
          match['hours'],
          match['minutes'],
          match['seconds'],
          )

    with open("log.log", "r", encoding='utf8') as file:
        pass
    return []


if __name__ == '__main__':
    parse()
