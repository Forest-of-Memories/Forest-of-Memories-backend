# 신호 핸들러 정의
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Family, CommonQuestion

@receiver(post_save, sender=User)
def create_user_family(sender, instance, created, **kwargs):
    if created and not instance.family:
        common_question = CommonQuestion.objects.first()
        
        if not common_question:
            common_question = CommonQuestion.objects.create(cmn_qst_txt="Default question text")

        family = Family.objects.create(cmn_qst_no=common_question)
        instance.family = family
        instance.save()