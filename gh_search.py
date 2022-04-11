import config
import calendar
from github import Github
import time

ACCESS_TOKEN = config.gh_api_key

g = Github(ACCESS_TOKEN)

def search_github(keyword, filetype):
    rate_limit = g.get_rate_limit()
    rate = rate_limit.search
    if rate.remaining == 0:
        print(f'You have 0/{rate.limit} search API calls remaining. Reset time: {rate.reset}')
        reset_timestamp = calendar.timegm(rate.reset.timetuple())
        sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 15  # add 5 seconds to be sure the rate limit has been reset
        time.sleep(sleep_time)
        return
    else:
        print(f'You have {rate.remaining}/{rate.limit} API calls remaining')
        query = f'"{keyword}" org:{config.gh_orgname} in:file extension:{filetype}'
        result = g.search_code(query, order='desc')

        max_size = 100
        print(f'Found {result.totalCount} {filetype} file(s) with {keyword}')
        print(f'Keyword,File type,GitHub URL,File match')
        if result.totalCount > max_size:
            result = result[:max_size]
            try:
                time.sleep(10)
                for file in result:
                    print(f'{keyword},{filetype},{file.download_url},{file.path}')
            except Exception as e:
                print(e)
        else:
            for file in result:
                print(f'{keyword},{filetype},{file.download_url},{file.path}')
    

if __name__ == '__main__':
    keyword = input('Enter biased keyword such as master, slave, blacklist, whitelist: ')
    filetype = input('Enter extension for files to search within such as py for Python, md for Markdown: ')
    #keyword = 'slave'
    #filetype = 'js'
    search_github(keyword, filetype)

