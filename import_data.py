import csv
from DiaryTune.models import csv_file

with open('new_song_info.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        csv_file.objects.create(
            title=row['title'],  # 정확한 컬럼 이름 사용
            artist=row['artist'],
            description=row['New Description']  # 대소문자 일치
    )