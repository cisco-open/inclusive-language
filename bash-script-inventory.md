# Content in repos - search for master using Bash

You can `git clone` all the repos you want to analyze, then use Bash scripts to loop through all the repos, searching in the files for the keyword you want to revise. This method means you will have a local copy of multiple repos but does not require creating a GitHub personal access token.

First, get a list of all repos names where you want to search in text files
for a term. In this case, we are searching for `master` to look for branch names and links containing `master`.

For DevNet Learning Labs, we use the Learning Labs API to get a list of all the repos using the `learning_lab_api.py` script from the `docs-helpers` folder. 

## Using Bash with grep to look for keywords

Clone all those repos locally so you can search within the text files locally using Bash loops. Often I will create a list in an Excel spreadsheet and then use the CONCATENATE function in Excel to create a list of `git clone <git url>` commands to use in a Bash script.

Once you have copies of all the repos locally, run this script to search for the string `/master/` (include the backslashes when looking for master in a URL). You would remove the backslashes if you are searching for any use of the word "master".

This script searches for the keyword in a "labs" directory in each repo, then it adds any hits it finds to a text file within the root of the repo folder. 

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

Now, in each folder/repo locally, you have a `.txt` file that indicates any mentions of `/master/` in that repo. You can then run another script that puts all those repos and files together into one long inventory list:

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

Now you can look at the `all-master-links-lists.txt` file to see which repos have a reference to "/master/" in any file in the "labs" directory:
```
cat all-master-links-lists.txt
```

One way that we could compare how many references to "master" were in URLs versus how many references to "master" were in code comands or text was by looking at the difference between running these scripts with and without the backslashes surrounding "master." It's safe to estimate that any use of master without backslashes was in a command or text rather than in a URL. We ran these on more than 100 repos as a data point for reference. 