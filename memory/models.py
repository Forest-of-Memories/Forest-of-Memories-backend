from django.db import models

class CommonQuestion(models.Model):
    cmn_qst_no = models.IntegerField()
    cmn_qst_txt = models.TextField()

    def __str__(self):
        return self.name

class Family(models.Model):
    family_id = models.IntegerField()
    tree_exp = models.IntegerField()
    tree_skin = models.CharField(max_length=100)
    tree_start_date = models.DateField()
    item_list = models.CharField(max_length=100)
    cmn_qst_no = models.ForeignKey(CommonQuestion, on_delete=models.CASCADE)
    wrt_strg = models.IntegerField()

    def __str__(self):
        return self.name
    
class User(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=30)
    kakao_token = models.CharField(max_length=300)
    lst_cmn_qst_no = models.IntegerField()
    liked_cmn_qst_no = models.IntegerField()
    liked_prsn_no = models.IntegerField()

    def __str__(self):
        return self.name
    
class Memory(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    tree_start_dt = models.DateField()
    tree_end_dt = models.DateField()
    first_feed_id = models.IntegerField()
    second_feed_id = models.IntegerField()
    third_feed_id = models.IntegerField()
    tree_skin = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class ShopItem(models.Model):
    item_id = models.IntegerField()
    item_name = models.CharField(max_length=100)
    item_price = models.IntegerField()
    item_photo = models.ImageField(blank=True, upload_to='shop_items/')
    item_type = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class CommonQuestion(models.Model):
    cmn_qst_no = models.IntegerField()
    cmn_qst_txt = models.TextField()

    def __str__(self):
        return self.name
    
class PersonalQuestion(models.Model):
    prsn_qst_no = models.IntegerField()
    prsn_qst_txt = models.TextField()
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    
    def __str__(self):
      return self.name

class Feed(models.Model):
    feed_id = models.IntegerField()
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.CharField(max_length=30)
    feed_img = models.ImageField(blank=True, upload_to='feeds/')
    feed_txt = models.TextField()
    feed_rgst_dt = models.DateField()

    def __str__(self):
        return self.name
    
class PersonalComment(models.Model):
    prsn_qst = models.ForeignKey(PersonalQuestion, on_delete=models.CASCADE)
    user = models.CharField(max_length=30)
    rgst_time = models.DateTimeField()
    cmt_txt = models.TextField()

    def __str__(self):
        return self.name
    
class FeedComment(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    user = models.CharField(max_length=30)
    rgst_time = models.DateTimeField()

    def __str__(self):
        return self.name