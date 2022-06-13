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