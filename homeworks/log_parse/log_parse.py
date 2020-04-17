# -*- encoding: utf-8 -*-
import datetime
import re

FILE_WITH_LOGS = 'log.log'
REGEXP_PATTERN = (r'^\[(?P<day>0[1-9]|[12][0-9]|3[01])/'
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


def parse(
        ignore_files=False,
        ignore_urls=[],
        start_at=None,
        stop_at=None,
        request_type=None,
        ignore_www=False,
        slow_queries=False
):
    with open(FILE_WITH_LOGS, "r", encoding='utf8') as file:
        all_logs_from_file = [log.rstrip() for log in file.readlines()]
    # TODO почитать про определение флагов True or None
    if ignore_files and not ignore_urls and not request_type and not ignore_www and not slow_queries:
        logs = ignores_files(all_logs_from_file)
        return top_5_urls(logs)
    elif ignore_urls and not ignore_files and not request_type and not ignore_www and not slow_queries:
        logs = ignores_urls(all_logs_from_file, ignore_urls)
        return top_5_urls(logs)
    elif start_at and stop_at and not ignore_files and not ignore_urls and not request_type and not ignore_www and not slow_queries:  # noqa
        logs = limit_by_date(all_logs_from_file, start_at, stop_at)
        return top_5_urls(logs)
    elif request_type and not ignore_files and not ignore_urls and not ignore_www and not slow_queries:
        logs = filtered_request_type(all_logs_from_file, request_type)
        return top_5_urls(logs)
    elif ignore_www and not ignore_files and not ignore_urls and not request_type and not slow_queries:
        logs = ignored_www(all_logs_from_file)
        return top_5_urls(logs)
    elif slow_queries and request_type:
        logs = filtered_request_type(all_logs_from_file, request_type)
        return top_5_slow_urls(logs)
    elif slow_queries:
        logs = without_parameters(all_logs_from_file)
        return top_5_slow_urls(logs)
    else:
        logs = without_parameters(all_logs_from_file)
        return top_5_urls(logs)


def get_full_url(match):
    return "{host}{path}{params}{anchor}".format(host=match['host'],
                                                 path=match['url_path'],
                                                 params=match['url_params'] if match['url_params'] else "",
                                                 anchor=match['url_anchor'] if match['url_anchor'] else "",
                                                 )


def ignored_www(logs: list):
    result_list = []
    for log in logs:
        match = re.search(REGEXP_PATTERN, log)
        log = re.sub(r"www.", "", log)
        if match:
            result_list.append(log)
    return result_list


def filtered_request_type(logs: list, method: str) -> list:
    result_list = []
    for log in logs:
        match = re.search(REGEXP_PATTERN, log)
        if match and match['method'] == method:
            result_list.append(log)
    return result_list


def limit_by_date(logs: list, started_at=None, stopped_at=None) -> list:
    datetime_obj_started_at = datetime.datetime.strptime(started_at, '%d/%b/%Y %H:%M:%S')
    datetime_obj_stopped_at = datetime.datetime.strptime(stopped_at, '%d/%b/%Y %H:%M:%S')
    result_list = []
    for log in logs:
        match = re.search(REGEXP_PATTERN, log)
        if match:
            datetime_from_log = datetime.datetime.strptime("{d}/{m}/{y} {h}:{min}:{s}".format(d=match['day'],
                                                                                              m=match['month'],
                                                                                              y=match['year'],
                                                                                              h=match['hours'],
                                                                                              min=match['minutes'],
                                                                                              s=match['seconds'],
                                                                                              ),
                                                           '%d/%b/%Y %H:%M:%S',
                                                           )
            if datetime_obj_started_at <= datetime_from_log <= datetime_obj_stopped_at:
                result_list.append(log)
    return result_list


def ignores_urls(logs: list, list_with_ignored_urls) -> list:
    result_list = []
    for log in logs:
        match = re.search(REGEXP_PATTERN, log)
        full_url = get_full_url(match)
        if match and full_url not in list_with_ignored_urls:
            result_list.append(log)
    return result_list


def ignores_files(logs: list) -> list:
    postfix_files = ".js", ".svg", ".gif", ".jpg", ".png", ".css"
    result_list = []
    for log in logs:
        match = re.search(REGEXP_PATTERN, log)
        if match and not match['url_path'].endswith(postfix_files):
            result_list.append(log)
    return result_list


def without_parameters(logs: list) -> list:
    result_list = []
    for log in logs:
        match = re.search(REGEXP_PATTERN, log)
        if match:
            result_list.append(log)
    return result_list


def top_5_urls(filtered_list_with_logs: list):
    log_counter = {}
    for log in filtered_list_with_logs:
        match = re.search(REGEXP_PATTERN, log)
        full_url = get_full_url(match)
        if log_counter.get(full_url):
            log_counter[full_url] += 1
        else:
            log_counter[full_url] = 1
    sorted_log_counter = {url: log_counter[url] for url in sorted(log_counter, key=log_counter.get, reverse=True)}
    return [count for count in sorted_log_counter.values()][:5]


def top_5_slow_urls(filtered_list_with_logs: list) -> list:
    response_time = {}
    for log in filtered_list_with_logs:
        match = re.search(REGEXP_PATTERN, log)
        full_url = get_full_url(match)
        if response_time.get(full_url):
            response_time[full_url][0] += 1
            response_time[full_url][1] += int(match['response_time'])
        else:
            response_time[full_url] = [1, int(match['response_time'])]
    top_slow_urls = {}
    for key, value in response_time.items():
        top_slow_urls[key] = int(value[1] / value[0])
    return sorted(top_slow_urls.values(), reverse=True)[:5]


if __name__ == '__main__':
    print(parse(slow_queries=True, request_type='GET'))
