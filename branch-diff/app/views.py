"""
Here we go with the app logic that scans two branches to find out commit difference...
"""

from app import app
from flask import render_template, request
from git import Repo
import subprocess
import os
import sys
from pyfiglet import figlet_format
from termcolor import cprint
from datetime import datetime
from subprocess import PIPE

class PrintColor:
    ATTN  =  '\033[35m'
    NOTICE = '\033[32m'
    END = '\033[0m'

banner = 'Automation-Stack-Git'
slogan = PrintColor.NOTICE + '''
Let's automate git ops and the rest...\n''' + PrintColor.END

def run(*args):
    return subprocess.run(['git'] + list(args), stdout=PIPE, stderr=PIPE, universal_newlines=True )

def branchMissingCommits(sbName, tbName, daysAgo, greatAuthors):
    #sourceBranch="master"
    localRepoDir="repo"
    __sourceBranch__ = f'{sbName}'
    # targetBranch = input("Name of release branch, e.g. release-202201: ")
    #targetBranch="release-202201"
    __targetBranch__ = f'{tbName}'
    #lastNdays = input("Number of days to check cherry-picks: ")
    __lastNdays__ = f'{daysAgo}'

    #devopsau='"Provungshu Arhant\|John First\|John Second"'
    devopsau = f'{greatAuthors}'

    if not os.path.exists(localRepoDir):
        print("\nLocal git repo not found. Creating repo under '" + localRepoDir + "' dir...\n")
        clone(localRepoDir)
    else:
        print("\nLocal git Repo already exists under '" + localRepoDir + "' dir. Refreshing when running local...\n")

    homeDir = os.getcwd();
    os.chdir("./" + localRepoDir)

    if os.path.isfile('/.dockerenv'):
        print ("\nGitOps using package...")       
        myRepo =  Repo()
        myRepo.git.checkout(__sourceBranch__)
        #All pull from live deployment
        #myRepo.git.pull()
        myRepo.git.checkout(__targetBranch__)
        myRepo.git.checkout(__sourceBranch__)
    else:
        # To be depreccated in next version
        run("checkout", __sourceBranch__)
        run("pull")
        run("checkout", __targetBranch__)
        run("pull")
        run("checkout", __sourceBranch__)
    
    print("\n...\n" + "Scanning git repo for commits cherry-picked by: " + devopsau)
    print("\n...\n" + __sourceBranch__ + ": commit    VS " + __targetBranch__  + ": commit\n...")
    print("\n...\n" + PrintColor.ATTN + "Press CONTROL+C to terminate this Flask instance..." + PrintColor.END + "\n")

    result = subprocess.getoutput('sourceCommits=`git log ' +  __sourceBranch__ + ' -i --after="' \
        + __lastNdays__ + ' days ago"' + ' --author=' + devopsau + ' --pretty=format:"%h"`; \
        for commit in $(echo $sourceCommits); do \
           echo "'+ __sourceBranch__ + ': ${commit}  ' + __targetBranch__ + ': \
`git log ' + __targetBranch__  + ' --grep="${commit}" --pretty=format:"%h %ad %an %s"`\
`git log ' + __targetBranch__ + ' --oneline --pretty=format:"%h %ad %an %s" | grep -i ${commit}`"; \
        done')

    #print(result)

    os.chdir(homeDir)
    original_stdout = sys.stdout
    with open("app/templates/index.html", 'w+') as f:
        sys.stdout = f
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        print("<pre>\n")
        print("Scanning to find out if any of the", __sourceBranch__ ,"commits [from last", __lastNdays__ ,"days] need to be in the", __targetBranch__ ,"branch...\n")
        print("As of now: ", now_str)
        print('Author(s): ', devopsau)
        print('\n...')
        print(__sourceBranch__ ,': commit   VS ', __targetBranch__ , ': commit')
        print('...\n')
        print(result)
        print("\n</pre>")
    f.close()
    sys.stdout = original_stdout

def clone(localDir):
    localRepoDir = localDir
    run("clone", "https://github.com/proarhant/branch-diff.git", localRepoDir)

@app.route("/")
@app.route("/git/scan")
def main():
    sourceBranchName = request.args.get('sb', default = 'master', type = str) 
    targetBranchName = request.args.get('tb', default = 'release-202201', type = str)
    daysAgo = request.args.get('since', default = 31, type = int)
    author = request.args.get('an', default = 'Pro Arhant\|John First\|John Second', type = str)

    if os.path.isfile('/.dockerenv'):
        cprint(figlet_format(banner, width=150, font='slant'), 'green')
        print(slogan)    
    else:
        print ("\nThe app is running in local mode... No fancy visual stuff included!")

    CurrentFeatures = 'scan'
    print("\nAvailable " + PrintColor.ATTN + "commands" + PrintColor.END + ": " + "\n")
    print(PrintColor.ATTN + "scan" + PrintColor.END + "    : Displays the commit(s) that may need to be cherry-picked from the master branch.")
    print(PrintColor.ATTN + "history" + PrintColor.END + " : Displays the last commit summary of any asset in the repo.")

    #choice = input("Type the command to execute e.g. bmc: ")
    choice="SCAN"
    choice = choice.lower()

    if choice == "scan":
        branchMissingCommits(sourceBranchName, targetBranchName, daysAgo, author)
        return render_template('index.html')

    elif choice == "history":
        history()

    elif choice == "deepScan":
        dreamSearch()

    else:
        print("\nPlease pick from the available commands: " + CurrentFeatures)
