import config
from github import Github

ACCESS_TOKEN = config.gh_api_key

g = Github(ACCESS_TOKEN)

def repo_default_branch(filterkey):
    orgname = config.gh_orgname
    repositories = g.search_repositories(query='org:{}'.format(orgname))
    for repo in repositories:
        rate_limit = g.get_rate_limit()
        corerate = rate_limit.core
        if corerate.remaining == 0:
            print(f'You have 0/{corerate.limit} core API calls remaining. Reset time: {corerate.reset}')
            return
        else:
            print(f'Your API call rate for core: {corerate.remaining}/{corerate.limit}')
        if repo.private == False:
            if filterkey in repo.full_name:
                repo = g.get_repo(repo.full_name)
                defaultbranch = repo.default_branch
                if defaultbranch == 'master':
                    print('Repo: ', repo.full_name, 'has a default branch named master.')
                    # You could automatically log an Issue asking maintainers to change default branch to main
                    # repo.create_issue(title="Make the default branch main instead of master", 
                    #                    body="Our required terminology policy makes the main branch the default
                    #                          as standard for all our organization repositories. Here's a link
                    #                          to the [GitHub documentation on renaming a branch](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/changing-the-default-branch).")

if __name__ == '__main__':
    filterkey = input('Enter a keyword such as ansible, labs, to filter a list of repo names in an org: ')
    #filterkey = 'ansible'
    repo_default_branch(filterkey)

