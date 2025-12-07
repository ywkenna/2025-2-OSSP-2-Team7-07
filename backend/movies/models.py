from django.db import models
from django.conf import settings



class MovieData(models.Model):
  
    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=500, null=False)
    title_ko = models.TextField(null=False)
    title_en = models.TextField(null=False, db_column='title_en')
    year = models.IntegerField(null=True)
    plot = models.TextField(null=True)
    runtime = models.IntegerField(null=True)
    genre = models.CharField(max_length=30, null=True)
    difficulty = models.IntegerField(null=True)


    #난이도 분석 사용 지표들
    word_avg_level = models.FloatField(null=True, blank=True) #평균 단어 난이도
    tree_depth = models.FloatField(null=True, blank=True) #구문 트리 깊이
    pron_acc = models.FloatField(null=True, blank=True) #발음 정확도
    real_word = models.FloatField(null=True, blank=True) #실질 단어 비율 (어휘의 다양성)
    clause_ratio = models.FloatField(null=True, blank=True) #평균 절 비율
    overlap_ratio = models.FloatField(null=True, blank=True) #중첩 발화 비율
    phrase_ratio = models.FloatField(null=True, blank=True) #숙어 비율
    pp_ratio = models.FloatField(null=True, blank=True) #평균 과거분사 비율
    rare_word_ratio = models.FloatField(null=True, blank=True) #희귀 단어 비율
    slang_ratio = models.FloatField(null=True, blank=True) #슬랭 비율
    syllable_word = models.FloatField(null=True, blank=True) #단어 당 음절 수
    avg_speed = models.FloatField(null=True, blank=True) #평균 말 빠르기
    lev_distance = models.FloatField(null=True, blank=True) #레벤슈타인 거리

    #OTT 링크 (웨이브, 왓챠, 넷플릭스, 티빙, 쿠팡플레이, 디즈니플러스)
    wavve_url = models.URLField(null=True, blank=True)
    watcha_url = models.URLField(null=True, blank=True)
    netflix_url = models.URLField(null=True, blank=True)
    tiving_url = models.URLField(null=True, blank=True)
    coupang_url = models.URLField(null=True, blank=True)
    disney_url = models.URLField(null=True, blank=True)
    

    def __str__(self):
        return self.title_ko
    



class Comment(models.Model):

    movie = models.ForeignKey(
        MovieData,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True
         
    )
    content = models.TextField()   
    created_time = models.DateTimeField(auto_now_add=True)  
    updated_time = models.DateTimeField(auto_now=True)     

    class Meta:
        ordering = ["-created_time"]  


    def __str__(self):
        return f"{self.user.username} on {self.movie.title_en}: {self.content[:20]}"
    
