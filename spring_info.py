#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import threading
import time
import sys, getopt

requests.packages.urllib3.disable_warnings()
threads = []
thread_max = threading.BoundedSemaphore(500)

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36; ',
    'Connection': 'close;'
}


def scan(url, flag):
    try:
        respon = requests.get(url, headers=header, timeout=3, verify=False)
        respon_size = 0
        if (respon.status_code == 200):
            respon_size = len(respon.content)
            if (respon_size == flag | flag == null):
                sys.exit(0)
            else:
                now = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
                print('[' + now + ']' + " " + 'code:[' + str(respon.status_code) + ']' + " " + 'size:' + '[' + str(
                    respon_size) + ' B]' + " " + url)
    except:
        pass
    thread_max.release()


def flag_size(url):  # 访问一个不存在的路径作为判断标准
    url = url + 'hjahfjksahkfjsakfkjskjfh'
    try:
        respon = requests.get(url, headers=header, timeout=3, verify=False)
        respon_size = len(respon.content)
        return respon_size
    except:
        pass


def info(url):
    if (url == ''):
        print('Usage: spring_info.py -t <target> or -f <urls_file>')
        sys.exit()
    start = time.time()
    now = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    print('strat_time: [' + str(now) + ']' + '  ' + '[' + url + ']')
    if (url[-1] == '/'):
        url = url
    else:
        url = url + '/'

    flag_size_info = flag_size(url)
    # print(flag_size_info)
    dir_spring = [
        'actuator',
        'auditevents',
        '/..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252Fetc%252Fpasswd%23foo/development',
        'autoconfig',
        'beans',
        'caches',
        'conditions',
        'configprops',
        'docs',
        'dump',
        'env',
        'flyway',
        'health',
        # 'heapdump',
        'httptrace',
        'info',
        'intergrationgraph',
        'jolokia',
        'logfile',
        'loggers',
        'liquibase',
        'metrics',
        'mappings',
        'prometheus',
        'refresh',
        'scheduledtasks',
        'sessions',
        'trace',
        'threaddump',
        'actuator/auditevents',
        'actuator/beans',
        'actuator/health',
        'actuator/conditions',
        'actuator/configprops',
        'actuator/env',
        'actuator/info',
        'actuator/loggers',
        # 'actuator/heapdump',
        'actuator/threaddump',
        'actuator/metrics',
        'actuator/scheduledtasks',
        'actuator/httptrace',
        'actuator/mappings',
        'actuator/jolokia',
        'actuator/hystrix.stream',
        'api-docs',
        'v2/api-docs',
        'swagger-ui.html',
        'api.html',
        'sw/swagger-ui.html',
        'api/swagger-ui.html',
        'template/swagger-ui.html',
        'spring-security-rest/api/swagger-ui.html',
        'spring-security-oauth-resource/swagger-ui.html',
        'v2/api-docs',
        'swagger-ui.html',
        'swagger',
        'api/swagger',
        'Swagger/ui/index',
        'api/swaggerui',
        'swagger/ui',
        'api/swagger/ui',
        'api/swagger-ui.html',
        'user/swagger-ui.html',
        'libs/swaggerui',
        'swagger/index.html',
        'swagger-resources/configuration/ui',
        'swagger-resources/configuration/security',
        'api.html',
        'druid/index.html',
        'sw/swagger-ui.html',
        'api/swagger-ui.html',
        'template/swagger-ui.html',
        'spring-security-rest/api/swagger-ui.html',
        'spring-security-oauth-resource/swagger-ui.html',
        'swagger/v1/swagger.json',
        'swagger/v2/swagger.json',
        'api-docs',
        'api/doc',
        'docs/',
        'doc.html',
        'v1/api-docs',
        'v3/api-docs'
    ]
    for i in dir_spring:
        newUrl = url + i
        newUrl = newUrl.strip()
        thread_max.acquire()
        t = threading.Thread(target=scan, kwargs={"url": newUrl, "flag": flag_size_info})
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    end = time.time()
    print('total_time: [' + str(end - start) + ']' + '\n')


def logo():
    logo = '''                                                        
                                                                        ___      
                                        _                   _         /'___)     
                      ___  _ _    _ __ (_)  ___     __     (_)  ___  | (__   _   
                    /',__)( '_`\ ( '__)| |/' _ `\ /'_ `\   | |/' _ `\| ,__)/'_`\ 
                    \__, \| (_) )| |   | || ( ) |( (_) |   | || ( ) || |  ( (_) )
                    (____/| ,__/'(_)   (_)(_) (_)`\__  |   (_)(_) (_)(_)  `\___/'
                          | |                    ( )_) |                         
                          (_)                     \___/'                         @KB-AT

            '''
    print(logo)


def main(argv):
    target = ''
    urls_file = ''
    try:
        opts, args = getopt.getopt(argv, "ht:f:", ["target=", "urls_file="])
    except getopt.GetoptError:
        print('Usage: spring_info.py -t <target> or -f <urls_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: spring_info.py -t <target> or -f <urls_file>')
            sys.exit()
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-f", "--urls_file"):
            urls_file = arg
        else:
            print('Usage: spring_info.py -t <target> or -f <urls_file>')
            sys.exit()

    if (urls_file != ''):
        urls = open(urls_file)
        for url in urls:
            info(url.strip())
    else:
        info(target.strip())


if __name__ == '__main__':
    logo()
    main(sys.argv[1:])
