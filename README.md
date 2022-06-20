Bigmart Store Sales Prediction
This repository is the implementation of the Bigmart store sales prediction that predicts the future sales of the store items.

Installation
Requirements
- Python 3.7+
- DVC
- Flask

Setup
create env

```bash
 conda create -n BigmartSalesPrediction
```

activate env
```bash
conda activate BigmartSalesPrediction
```

created a req file
install the req
```bash
pip install -r requirements.txt
```

download the data

```bash
git init
```

```bash
dvc init
```

```bash
dvc add data_given/Train.csv
```

```bash
git add .
```

```bash
git commit -m "first commit"
```

online updates for readme

```bash
git add . && git commit -m "update Readme.md"
```

```bash
git remote add origin https://github.com/Dhrupti02/BigmartSalesPrediction.git
git branch -M main
git push origin main
```

tox command -

```bash
tox 
```

for rebuilding -
```bash
tox -r
```

pytest command
```bash
pytest -v
```

setup commands -
```bash
pip install -e .
```