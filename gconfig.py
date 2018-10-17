import multiprocessing
import os
mem_mb = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / 1024 **2
w = multiprocessing.cpu_count() * 2 + 1
need_mem = w * 50
while(need_mem > mem_mb):
    w = w -1
    need_mem = w * 45
workers = w
secure_scheme_headers = {'X-FORWARDED-PROTOCOL': 'ssl', 'X-FORWARDED-PROTO': 'https', 'X-FORWARDED-SSL': 'on'}
timeout = 300
