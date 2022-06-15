import config
import calendar
from github import Github
import time

ACCESS_TOKEN = config.gh_api_key

g = Github(ACCESS_TOKEN)

def convert_entries_to_pages(total_entries):
    PAGE_SIZE = 100
    leftover_entries = total_entries % PAGE_SIZE
    pages = total_entries // PAGE_SIZE
    print("extra entries: ", leftover_entries)
    if pages > 1:
        pages = pages + 1
        return pages
    else:
        return 1

def search_github(keyword, filetype):
    PAGE_SIZE = 100
    c = 0
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
        if filetype == 'any':
            query = f'"{keyword}" org:{config.gh_orgname}'
            result = g.search_code(query, order='desc')

            print(f'Found {result.totalCount} file(s) with {keyword}')
            
            print(f'Keyword,File type,GitHub URL,File match')
            pages = convert_entries_to_pages(result.totalCount)
            for i in range(pages):
                tempResult = result[c:c+PAGE_SIZE]
                c += PAGE_SIZE
                try:
                    print(f"Page: {i+1} of {pages}")
                    time.sleep(10)
                    for file in tempResult:
                        path = file.path
                        try:
                            actualfiletype = path.rsplit(sep='.')[1]
                        except Exception as e:
                            actualfiletype = path.rsplit(sep='/')[1] 
                        print(f'{keyword},{actualfiletype},{file.download_url},{file.path}')
                except Exception as e:
                    print(e)

        else:  
            query = f'"{keyword}" org:{config.gh_orgname} in:file extension:{filetype}'
            result = g.search_code(query, order='desc')
            
            print(f'Found {result.totalCount} file(s) with {keyword}')
            print(f'Keyword,File type,GitHub URL,File match')
            pages = convert_entries_to_pages(result.totalCount)
             
            for i in range(0, pages, 100):
                print("i is now: ", i)
                tempResult = result[c:c+PAGE_SIZE]
                c += PAGE_SIZE
                print("Count is now: ",c)
                try:
                    print(f"Page: {i+1} of {pages}")
                    time.sleep(10)
                    for file in tempResult:
                        print(f'{keyword},{filetype},{file.download_url},{file.path}')
                except Exception as e:
                    print(e)
            

if __name__ == '__main__':
    #keyword = input('Enter biased keyword such as \"master\", \"slave\", \"blacklist\", \"whitelist\": ')
    #filetype = input('Enter extension for files to search within such as \"py\" for Python, \"md\" for Markdown, and enter \"any\" for all file types: ')
    #keyword = 'whitelist'
    keyword = 'slave'
    filetype = 'any'
    #filetype = 'py'
    search_github(keyword, filetype)
