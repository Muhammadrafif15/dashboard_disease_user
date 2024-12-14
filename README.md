# dashboard disease prediction - native bayes

## Setup branch
```
git branch -m master main
git fetch origin
git branch -u origin/main main
git remote set-head origin -a
```
## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir disease_dashboard
cd disease_dashboard
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dasboard_user.py
```
