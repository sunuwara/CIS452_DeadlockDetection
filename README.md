# CIS452_DeadlockDetection

## Setup:

1. Download zip or clone: `git clone https://github.com/sunuwara/CIS452_DeadlockDetection.git`
2. Install poetry: `curl -SSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python`
3. Navigate to projects local repository from Terminal
4. Install project dependencies: `poetry install`

## How to run:

Deadlock Detection without recovery:

`poetry run python simulateRM.py`

Deadlock Detection with recovery(EXTRA CREDIT):

`poetry run python simulateRM_EC.py`

Note: While running plot window will pop up at each action, to continue close the window.
