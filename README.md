# branch-diff
Scan to compare branches using this Python Flask micro web framework.

Currently availble features:

1. Finds out if any of the commits [created since last N days] from a source branch e.g. master branch, needs to be cherry-picked onto another target branch e.g. release-202201 branch.

## Installation with Docker

Requires:

Nothing but `docker`

```bash
git clone https://github.com/proarhant/branch-diff.git
cd branch-diff && ./branch-diff-app-deploy.sh
```

To run this Flask app in deatached mode in the background:

```bash
cd branch-diff && ./branch-diff-app-deploy.sh -m detached
```

## Installation without Docker

Requires:

`python3` `pip3` or `pip`

```bash
git clone https://github.com/proarhant/branch-diff.git
# These three packages are required in your venv: 
#   pip3 install flask pyfiglet termcolor
cd branch-diff && ./branch-diff-app-deploy.sh -m local
```

## Usage

```bash

http://0.0.0.0/git/scan?sb=<SourceBranch>&tb=<TargetBranch>&since=<Days>&an=<Author's Name>

sb     = Source Branch name   [ default is master ]
tb     = Target Branch name   [ default is release-202201 ]
since  = days                 [ default is 31 days ]
an     = author's name        [ default is devops-au ]

Examples:

http://0.0.0.0/git/scan
http://0.0.0.0/git/scan?sb=master&tb=release-202201&since=21&an=provun
http://0.0.0.0/git/scan?tb=release-202201&since=18&an=provungs
http://0.0.0.0/git/scan?tb=release-202201&an=provun
http://0.0.0.0/git/scan?tb=release-202112&since=23
http://0.0.0.0/git/scan?sb=featureBranch&since=18&an=Provungshu

```

## Cleaning up Docker things

```bash
docker rm -f git-flask_1
docker image rm git-flask
```
Or, simply execute:

```bash
./branch-diff/branch-diff-app-cleanup.sh
```

## Notes

1. Date displayed on the browser is in UTC.

## Contributing
Contribution needed for more features...

```bash
http://0.0.0.0/git/*
http://0.0.0.0/aws/*
http://0.0.0.0/azure/*
http://0.0.0.0/gcp/*
```
