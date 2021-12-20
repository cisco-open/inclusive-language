# Content in repos - search for master

Get a list of all repos names where you want to search in text files
for a term. In this case, we are searching for `master` to look for branch names and links containing `master`.

For DevNet Learning Labs, use the Learning Labs API to get a list of all the repos using the `learning_lab_api.py` script from the `docs-helpers` folder. 

With a personal access token with rights to private repos, you can get a list of repos from a GitHub org using the `gh-pager-list-repos.py` script. You need the org name, username, and a personal access token in a separate config.py file. 

## Using Bash with grep

Clone all those repos locally so you can search within the text files locally using Bash loops. 

Once you have copies of all the repos locally, run this script to search for the string `/master/` (including the backslashes, you would remove the backslashes if you are not searching only for links to the `master` branch, for example).

```
for dir in */; do
    cd $dir
    length=$((${#dir} - 1));
    reponame="${dir:0:$length}"
    echo $reponame
    grep -rl  "/master/" labs > "$reponame"-master-links-list.txt
    cd ..
done

```

Then, in each folder/repo locally, you'll have a `.txt` file that indicates any mentions of `/master/` in that repo. You can then run another script that'll put all those repos and files together into one long inventory list:

```
for dir in */; do
    echo "$dir"
    cd $dir
    length=$((${#dir} - 1));
    reponame="${dir:0:$length}"
    echo $reponame
    cat "$reponame"-master-list.txt >> ../all-master-links-lists.txt
    cd ..
done
```

## Using the GitHub REST API

Here's a Python example using the REST API and the `requests` library. However on a large org like Cisco DevNet, I got rate limits after 18 pages of results. 

```
import configvar
import requests
from urllib.parse import urlparse
from urllib.parse import parse_qs
"""
With a GitHub API Key, orgname, username, topic, search through a list of repos
In an org for a keyword or key phrase.
Hits rate limits after page 18 of results
"""

def github_api_get(gh_api_endpoint, gh_orgname, gh_username, gh_api_key):
    search_keyword1 = "master"
    search_keyword2 = "slave"
    doc_qualifier = "markdown"
    code_qualifier = "python"
    api_uri = "{}search/code?q=org:{}+{}+language:{}&type=code+&page=1".format(gh_api_endpoint, gh_orgname, search_keyword1, doc_qualifier)
    headers = {'User-Agent': '{}'.format(gh_username),
               'Content-Type': 'application/json',
               'Authorization': 'token {}'.format(gh_api_key),
               'Accept': 'application/vnd.github.mercy-preview+json'
               }
    
    responseobj = requests.get(api_uri, headers=headers)
    responsejson = responseobj.json()
    #print(responsejson)
    pagevalue = 1
    while responsejson['items'] is not []:
        pagevalue = pagevalue + 1
        print("Page: ", pagevalue)
        next_page_api_uri = api_uri = "{}search/code?q=org:{}+{}+language:{}&type=code+&page=1".format(gh_api_endpoint, gh_orgname, search_keyword1, doc_qualifier, pagevalue)
        print("URL: ", next_page_api_uri)
        nextresponse = requests.get(next_page_api_uri, headers=headers)
        print(nextresponse)
        data = nextresponse.json()
        print("Next page: ", data)
        if "422" in nextresponse:
            print(nextresponse.reason())
            print("All pages done.")

github_api_get(configvar.gh_api_endpoint, configvar.gh_orgname, configvar.gh_username, configvar.gh_api_key)

```

