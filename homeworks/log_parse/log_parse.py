# -*- encoding: utf-8 -*-
import re
from collections import Counter


FILE_WITH_LOGS = 'log.log'


def parse(
        ignore_files=False,
        ignore_urls=[],
        start_at=None,
        stop_at=None,
        request_type=None,
        ignore_www=False,
        slow_queries=False
):

    regexp_pattern = (r'^\[(?P<day>0[1-9]|[12][0-9]|3[01])/'
                      r'(?P<month>Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)/'
                      r'(?P<year>(19|20)\d\d)\s{1}'
                      r'(?P<hours>0[0-9]|1[0-9]|2[0-3]):'
                      r'(?P<minutes>[0-5][0-9]):'
                      r'(?P<seconds>[0-5][0-9])\]\s{1}"'
                      r'(?P<method>[A-Z]+)\s{1}'
                      r'(?P<scheme>[a-z]+)://'
                      r'(?P<host>[a-z.]*)'
                      r'(?P<url_path>[\w/.]+)'
                      r'(?P<url_params>[^\s^#]+)?'
                      r'(?P<url_anchor>[^\s]+)?\s{1}'
                      r'(?P<protocol>[\w/.]+)"\s'
                      r'(?P<response_code>\d{3})\s'
                      r'(?P<response_time>\d+)'
                      )
    return returned_top_5_urls(logs, regexp_pattern)


def created_filtered_list_with_logs(list_with_logs: list):
    pass


def returned_top_5_urls(filtered_list_with_logs: list, reg_pattern):
    log_counter = {}
    for log in filtered_list_with_logs:
        match = re.search(reg_pattern, log)
        if match:
            full_url = "{host}{path}{params}{anchor}".format(host=match['host'],
                                                             path=match['url_path'],
                                                             params=match['url_params'] if match['url_params'] else "",
                                                             anchor=match['url_anchor'] if match['url_anchor'] else "",
                                                             )
            if log_counter.get(full_url):
                log_counter[full_url] += 1
            else:
                log_counter[full_url] = 1
    sorted_log_counter = {url: log_counter[url] for url in sorted(log_counter, key=log_counter.get, reverse=True)}
    return [count for count in sorted_log_counter.values()][:5]


if __name__ == '__main__':
    with open(FILE_WITH_LOGS, "r", encoding='utf8') as file:
        logs = [log.rstrip() for log in file.readlines()]

    print(parse(ignore_files=True))
