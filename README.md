# taxonomic-classification
Hierarchical Classification using SVM

### To executre.
1. create a virtual env and install libraries from requiments.txt
```
virtualenv hsvm
source hsvm/bin/activate

pip install -r requirements.txt
```
2. make migrations.
```
python manange.py makemigrations
python manange.py migrate
```

3. run the django server
```
python manage.py runserver
```
