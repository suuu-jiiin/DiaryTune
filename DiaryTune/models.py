from django.db import models

class Diary(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) # 내용들 작성한 날짜
    updated_at = models.DateTimeField(auto_now=True) # 작성한 내용 수정일
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    activities = models.TextField(blank=True, null=True)  # 선택된 활동들
    weather = models.TextField(blank=True, null=True)      # 선택된 날씨들
    diary_content = models.TextField()  # 일기 내용

    def __str__(self):
        return f"{self.year}-{self.month}-{self.day}의 일기"
