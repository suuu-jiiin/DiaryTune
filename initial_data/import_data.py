import csv, os, sys, django

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) # BASE_DIR은 manage.py가 있는 최상위 디렉토리
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from DiaryTune.models import csv_file 
CSV_PATH = os.path.join(BASE_DIR, 'initial_data') 
with open(os.path.join(CSV_PATH, 'new_song_info.csv'), 'r',  encoding='utf-8-sig') as csvfile:
    for row in csv.DictReader(csvfile):
        csv_file.objects.create(
            title=row['title'],
            artist=row['artist'],
            description=row['description']
            )
