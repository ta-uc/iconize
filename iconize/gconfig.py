import multiprocessing
workers = multiprocessing.cpu_count() * 2 + 1
secure_scheme_headers = {'X-FORWARDED-PROTOCOL': 'ssl', 'X-FORWARDED-PROTO': 'https', 'X-FORWARDED-SSL': 'on'}
timeout = 300