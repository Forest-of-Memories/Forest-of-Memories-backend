from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CommonQuestion(models.Model):
    cmn_qst_no = models.AutoField(primary_key=True)
    cmn_qst_txt = models.TextField()

    def __str__(self):
        return f"{self.cmn_qst_no}"

class Family(models.Model):
    family_id = models.AutoField(primary_key=True)
    tree_exp = models.IntegerField(default=0)
    tree_skin = models.CharField(max_length=100, default='', null=True, blank=True)
    tree_start_date = models.DateField(default=timezone.now)
    item_list = models.CharField(max_length=100, default='', null=True, blank=True)
    first_feed = models.ForeignKey('Feed', related_name='first_feed', null=True, blank=True, on_delete=models.SET_NULL)
    second_feed = models.ForeignKey('Feed', related_name='second_feed', null=True, blank=True, on_delete=models.SET_NULL)
    third_feed = models.ForeignKey('Feed', related_name='third_feed', null=True, blank=True, on_delete=models.SET_NULL)
    cmn_qst_no = models.ForeignKey(CommonQuestion, on_delete=models.CASCADE, null=True, blank=True)
    wrt_strg = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.family_id}"
        
    
class User(AbstractUser): 
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)
    user_name = models.CharField(max_length=30)
    user_id = models.CharField(max_length=20, unique=True)  # 구글 로그인에서 받아오는 user_id
    email = models.EmailField(unique=True)  # 구글 로그인에서 받아오는 email
    lst_cmn_qst_no = models.IntegerField(default=0)
    liked_cmn_qst_no = models.CharField(max_length=255, default='', null=True, blank=True)  
    liked_psn_qst_no = models.CharField(max_length=255, default='', null=True, blank=True)

    def __str__(self):
        return f"{self.user_name}"

    def save(self, *args, **kwargs):
        if not self.family:
            self.family = Family.objects.create()
        super().save(*args, **kwargs)
    
class Memory(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    tree_start_dt = models.DateField()
    tree_end_dt = models.DateField()
    first_feed_id = models.IntegerField(null=True, blank=True)
    second_feed_id = models.IntegerField(null=True, blank=True)
    third_feed_id = models.IntegerField(null=True, blank=True)
    tree_skin = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.family.family_id}"
    
class ShopItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=50)
    item_price = models.IntegerField()
    item_photo = models.ImageField(blank=True, upload_to='shop_items/')
    item_type = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.item_id}"
    
    
class PersonalQuestion(models.Model):
    prsn_qst_no = models.AutoField(primary_key=True)
    prsn_qst_txt = models.TextField()
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    
    def __str__(self):
      return f"{self.prsn_qst_no}"

class Feed(models.Model):
    feed_id = models.AutoField(primary_key=True)
    family = models.ForeignKey('Family', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed_img = models.ImageField(blank=True, upload_to='feeds/')
    feed_txt = models.TextField()
    feed_rgst_dt = models.DateField()

    def __str__(self):
        return f"{self.feed_id}"
    
class CommonComment(models.Model):
    cmn_qst = models.ForeignKey(CommonQuestion, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey로 변경
    rgst_time = models.DateTimeField(auto_now_add=True)
    cmt_txt = models.TextField()

    def __str__(self):
        return self.cmt_txt

class PersonalComment(models.Model):
    prsn_qst = models.ForeignKey(PersonalQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rgst_time = models.DateTimeField(auto_now_add=True)
    cmt_txt = models.TextField()

    def __str__(self):
        return self.cmt_txt
    
class FeedComment(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rgst_time = models.DateTimeField()
    cmt_txt = models.TextField(default="")

    def __str__(self):
        return self.cmt_txt
    
class CommonAnswer(models.Model):
    cmn_qst = models.ForeignKey(CommonQuestion, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey로 변경
    rgst_time = models.DateTimeField(auto_now_add=True)
    ans_txt = models.TextField()

    def __str__(self):
        return self.ans_txt

class PersonalAnswer(models.Model):
    prsn_qst = models.ForeignKey(PersonalQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rgst_time = models.DateTimeField(auto_now_add=True)
    ans_txt = models.TextField()

    def __str__(self):
        return self.ans_txt