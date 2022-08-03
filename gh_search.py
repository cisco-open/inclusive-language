import config
import calendar
from github import Github
import logging
import time

ACCESS_TOKEN = config.gh_api_key
API_ENDPOINT = config.egh_api_endpoint

g = Github(ACCESS_TOKEN)
eg = Github(base_url=API_ENDPOINT, login_or_token=config.egh_api_key)

def search_github(keyword, filetype):
    logging.basicConfig(filename='githubsearchresultsinfo.log',
                        encoding='utf-8', 
                        format='%(asctime)s %(message)s',
                        filemode='w',
                        level=logging.INFO)
    logger = logging.getLogger()
    rate_limit = g.get_rate_limit()
    rate = rate_limit.search
    if rate.remaining == 0:
        print(f'You have 0/{rate.limit} search API calls remaining. Reset time: {rate.reset}')
        reset_timestamp = calendar.timegm(rate.reset.timetuple())
        sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 15  
        time.sleep(sleep_time)
        return
    else:
        logger.info(f'You have {rate.remaining}/{rate.limit} API calls remaining')
        if filetype == 'any':
            query = f'"{keyword}" org:{config.gh_orgname}'
            searchresults = g.search_code(query, order='desc')
            # search_code returns a paginated_list https://pygithub.readthedocs.io/en/latest/utilities.html?highlight=pagination#pagination
            logger.info(f'Found {searchresults.totalCount} entries with {keyword}')
            # Prints the column labels
            print(f'Keyword,File type,GitHub URL,File match')

            for entry in searchresults:
                try:
                    time.sleep(2)
                    # each entry is a ContentFile https://pygithub.readthedocs.io/en/latest/github_objects/ContentFile.html#github.ContentFile.ContentFile
                    path = entry.path
                    try:
                        actualfiletype = path.rsplit(sep='.')[1]
                    except Exception as e:
                        # Sometimes the string split would find another character, causing an error
                        actualfiletype = path.rsplit(sep='/')[1] 
                    print(f'{keyword},{actualfiletype},{entry.html_url},{entry.path}')
                except Exception as e:
                    print("Error: ", e)
            else:
                for file in searchresults:
                    path = file.path
                    try:
                        actualfiletype = path.rsplit(sep='.')[1]
                    except Exception as e:
                        actualfiletype = path.rsplit(sep='/')[1]
                    print(f'{keyword},{actualfiletype},{file.download_url},{file.path}')

        else:
            # For queries with an exact file type
            query = f'"{keyword}" org:{config.gh_orgname} in:file extension:{filetype}'
            searchresults = g.search_code(query, order='desc')
            
            logger.info(f'Found {searchresults.totalCount} entries(s) with {keyword}')
            print(f'Keyword,File type,GitHub URL,File match')
             
            for entry in searchresults:
                try:
                    # Try to avoid rate limits
                    time.sleep(2)
                    print(f'{keyword},{filetype},{searchresults.html_url},{searchresults.path}')
                except Exception as e:
                    print("Error: ", e)

                    path = file.path
                    try:
                        actualfiletype = path.rsplit(sep='.')[1]
                    except Exception as e:
                        actualfiletype = path.rsplit(sep='/')[1]
                    print(f'{keyword},{actualfiletype},{file.download_url},{file.path}')

def search_enterprise_github(keyword, filetype):
    logging.basicConfig(filename='enterprisesearchresultsinfo.log',
                        encoding='utf-8', 
                        format='%(asctime)s %(message)s',
                        filemode='w',
                        level=logging.INFO)
    logger = logging.getLogger()
    rate_limit = eg.get_rate_limit()
    rate = rate_limit.search
    if rate.remaining == 0:
        print(f'You have 0/{rate.limit} search API calls remaining. Reset time: {rate.reset}')
        reset_timestamp = calendar.timegm(rate.reset.timetuple())
        sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 15  
        time.sleep(sleep_time)
        return
    else:
        logger.info(f'You have {rate.remaining}/{rate.limit} API calls remaining')
        if filetype == 'any':
            query = f'"{keyword}" org:{config.egh_orgname}'
            print("Query is: ", query)
            searchresults = eg.search_code(query, order='desc')
            # search_code returns a paginated_list https://pygithub.readthedocs.io/en/latest/utilities.html?highlight=pagination#pagination
            logger.info(f'Found {searchresults.totalCount} entries with {keyword}')
            # Prints the column labels
            print(f'Keyword,File type,ENGitHub URL,File match')

            for entry in searchresults:
                try:
                    time.sleep(2)
                    # each entry is a ContentFile https://pygithub.readthedocs.io/en/latest/github_objects/ContentFile.html#github.ContentFile.ContentFile
                    path = entry.path
                    try:
                        actualfiletype = path.rsplit(sep='.')[1]
                    except Exception as e:
                        # Sometimes the string split would find another character, causing an error
                        actualfiletype = path.rsplit(sep='/')[1] 
                    print(f'{keyword},{actualfiletype},{entry.download_url},{entry.path}')
                except Exception as e:
                    print("Error: ", e)
            else:
                for file in searchresults:
                    path = file.path
                    try:
                        actualfiletype = path.rsplit(sep='.')[1]
                    except Exception as e:
                        actualfiletype = path.rsplit(sep='/')[1]
                    print(f'{keyword},{actualfiletype},{file.download_url},{file.path}')

        else:
            # For queries with an exact file type
            query = f'"{keyword}" org:{config.egh_orgname} in:file extension:{filetype}'
            searchresults = eg.search_code(query, order='desc')
            
            logger.info(f'Found {searchresults.totalCount} entries(s) with {keyword}')
            print(f'Keyword,File type,ENGitHub URL,File match')
             
            for entry in searchresults:
                try:
                    time.sleep(2)
                    # each entry is a ContentFile https://pygithub.readthedocs.io/en/latest/github_objects/ContentFile.html#github.ContentFile.ContentFile
                    path = entry.path
                    try:
                        actualfiletype = path.rsplit(sep='.')[1]
                    except Exception as e:
                        # Sometimes the string split would find another character, causing an error
                        actualfiletype = path.rsplit(sep='/')[1] 
                    print(f'{keyword},{actualfiletype},{entry.html_url},{entry.path}')
                except Exception as e:
                    print("Error: ", e)
            else:
                for file in searchresults:
                    path = file.path
                    try:
                        actualfiletype = path.rsplit(sep='.')[1]
                    except Exception as e:
                        actualfiletype = path.rsplit(sep='/')[1]
                    print(f'{keyword},{actualfiletype},{file.download_url},{file.path}')

if __name__ == '__main__':
    which_github = input('Enter Enterprise for Enterprise GitHub, otherwise by default search GitHub: ')
    keyword = input('Enter biased keyword such as \"master\", \"slave\", \"blacklist\", \"whitelist\": ')
    filetype = input('Enter extension for files to search within such as \"py\" for Python, \"md\" for Markdown, and enter \"any\" for all file types: ')
    #keyword = 'slave'
    #filetype = 'any'
    #filetype = 'md'
    #filetype = 'py'
    if which_github == "Enterprise":
        search_enterprise_github(keyword, filetype)
    else:
        search_github(keyword, filetype)
    
    logging.basicConfig(filename='allsearchresultsinfo.log',
                        encoding='utf-8', 
                        format='%(asctime)s %(message)s',
                        filemode='w',
                        level=logging.INFO)
    logger = logging.getLogger()
    logger.info(f'Printed entries with {keyword} of {filetype} to output')
