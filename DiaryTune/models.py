from django.db import models
import json

class Diary(models.Model):
    # 기존 필드들
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시 자동으로 설정되는 날짜
    updated_at = models.DateTimeField(auto_now=True)      # 수정 시 자동으로 설정되는 날짜
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    activities = models.TextField(blank=True, null=True)  # 선택된 활동들
    weather = models.TextField(blank=True, null=True)      # 선택된 날씨들
    diary_content = models.TextField()  # 일기 내용
    
    # 좋아요 기능 필드
    like = models.BooleanField(default=False)  # 기본값은 False

    # New
    selected_sentiment = models.CharField(max_length=100, blank=True, null=True)  # 감정 종류
    similar_words = models.JSONField(blank=True, null=True)  # 감정과 유사한 단어들 (JSON 형식)

    # 음악 추천 관련 필드
    song_title = models.CharField(max_length=255, blank=True, null=True)  # 추천된 노래 제목
    song_artist = models.CharField(max_length=255, blank=True, null=True)  # 추천된 노래 아티스트)
    song_description = models.CharField(max_length=255, blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)


    def set_activities(self, activities_list):
        if activities_list:  # 리스트가 비어 있지 않으면 JSON으로 저장
            self.activities = json.dumps(activities_list)
        else:
            self.activities = '[]'  # 빈 리스트로 저장

    def get_activities(self):
        try:
            return json.loads(self.activities) if self.activities else []  # 올바르게 파싱
        except json.JSONDecodeError:
            return []  # 잘못된 JSON일 경우 빈 리스트 반환

    def set_weather(self, weather_list):
        if weather_list:  # 리스트가 비어 있지 않으면 JSON으로 저장
            self.weather = json.dumps(weather_list)
        else:
            self.weather = '[]'  # 빈 리스트로 저장

    def get_weather(self):
        try:
            return json.loads(self.weather) if self.weather else []  # 올바르게 파싱
        except json.JSONDecodeError:
            return []  # 잘못된 JSON일 경우 빈 리스트 반환
    
    def __str__(self):
        return f"{self.year}-{self.month}-{self.day}의 일기"

class csv_file(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    description = models.TextField()  # 새로운 필드 추가

    def __str__(self):
        return f"{self.artist} - {self.title}"
    
