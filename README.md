# Inclusive language resources and tool examples

When you're working on inclusive language use and terminology policies, it helps to have some tools at hand. These are examples we are using to get started on our policy work and are not supported. That said, we welcome feedback and input as we start on our quest to eliminate certain keywords in our code and content.

One script, `gh_search.py`, takes an inventory of which files contain keywords that you no longer want to use, creating a comma-separated listing that you can use for further analysis. You can use this script with either public GitHub (github.com) or Enterprise GitHub (currently tested with 3.3.7).

Another script, `gh_default_branch.py`, looks for repos that still have the default branch set to `master` instead of `main`. You could modify that script to create an Issue automatically in any repo that meets that criteria, or run the script as a report for analysis.

To use these scripts, you must create a `config.py` file that contains a GitHub personal access token. The [GitHub docs describe creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). You'll notice that the `.gitignore` file in this repo ignores any file named `config.py`.

Note that the script can only look for repos that your GitHub user has access to, so private repos that you don't have access to will not be included in the search query.

Example `config.py`:

```python
gh_api_key = "ghp_TotallyaFaKeTok3nIprom1seYouS0d0ntTrYit"
gh_api_endpoint = "https://api.github.com/"
gh_orgname = "cisco-open"
```

## Inventory listing using the GitHub REST API and a personal access token

The `gh_search.py` file is a Python example using the REST API and the `PyGitHub` library. In my testing on a large org like `CiscoDevNet`, I found it necessary to insert sleep pauses when GitHub returns a large list for the query. 

If you want to search Enterprise GitHub, you can add the Enterprise GitHub API Endpoint and access token to the `config.py` file. Here's an example:

```python
egh_orgname = "DevNet-org"
egh_api_endpoint = "https://internal-github.example.com/api/v3"
egh_api_key = "ghp_TotallyaFaKeTok3nIprom1seYouS0d0ntTrYit"
```

To get a list of repos with a keyword in certain files:

1. Create a `config.py` file in the root of the repository with your [GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with "repo" scope.
   ```python
   gh_api_key = "ghp_TotallyaFaKeTok3nIprom1seYouS0d0ntTrYit"
   gh_orgname = "cisco-open"
   ```
2. Create a Python virtual environment:
   ```shell
   python -m venv venv
   ```
3. Source the virtual environment. 
   On Windows: `venv\Scripts\activate.bat` 
   On Mac or Linux: `source venv/bin/activate`
4. Install the dependencies, namely the `PyGitHub` library: 
   ```shell
   pip install -r requirements.txt
   ```
5. Run the script and enter the keyword and file type you want to collect an inventory for. Here's an example:

   ```shell
   python gh_search.py
   ```
   ```
   Enter Enterprise for Enterprise GitHub, otherwise by default search GitHub:  
   Enter biased keyword such as "master", "slave", "blacklist", "whitelist": slave
   Enter extension for files to search within such as "py" for Python, "md" for Markdown, and enter "any" for all file types: md
   Keyword,File type,GitHub URL,File match
   slave,md,https://raw.githubusercontent.com/CiscoDevNet/terraform-provider-intersight/5e7db7ccfd4065f0a5a116c9f357ac690878a25a/intersight_gosdk/docs/VirtualizationBondState.md {'intersight_gosdk/docs/VirtualizationBondState.md'}
   ...
   ```
6. You can copy the output data into a CSV (Comma Separated Values) file if you want to import into Excel for further analysis.

## Identifying repositories in an org that can change their default branch to main

The `gh_default_branch.py` script uses some filtering to get a subset of repositories in a large GitHub org to see if the default branch is still set to "master" rather than "main." The default setting for the script writes out a report listing the repo names. A commented-out line shows an example of creating an Issue in the repo letting the maintainers know that we want them to change their default branch to one named `main` to meet the organization's standards.

To get a list of repos that have a keyword in the repo name that use `master` as the default branch:

1. Create a `config.py` file in the root of the repository with your [GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with "repo" scope.
2. Create a Python virtual environment: `python -m venv venv`.
3. Source the virtual environment. On Windows: `venv\Scripts\activate.bat` On Mac or Linux: `source venv/bin/activate`.
4. Install the dependencies, namely the `PyGitHub` library: `pip install -r requirements.txt`.
5. Run the script and enter the filter for repo name that you want to use in a large organization.

## Development

This project uses [pipenv](https://pipenv.pypa.io/en/latest/install/#installing-pipenv) for managing dependencies.

- Adding a new dependency: 
  - Install the dependency and add it to the Pipfile: `pipenv install <dependency>`
  - Update the Pipfile.lock file: `pipenv lock`
  - Update the requirements.txt file: `pipenv requirements > requirements.txt`

- Updating dependencies:
  - Update the dependency in Pipfile
  - Update the Pipfile.lock file and update the virtualenv: `pipenv update`
  - Update the requirements.txt file: `pipenv requirements > requirements.txt`

- Developing using pipenv:
  - Create the virtualenv (if you haven't already): `pipenv install`
  - Update the virtualenv: `pipenv sync`
  - Enter the virtualenv: `pipenv shell`
