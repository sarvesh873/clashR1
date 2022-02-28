from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
import json

# Create your models here.

class Question(models.Model):
    question = models.TextField(max_length=500)
    option_1 = models.CharField(max_length=500)
    option_2 = models.CharField(max_length=500)
    option_3 = models.CharField(max_length=500)
    option_4 = models.CharField(max_length=500)
    
    class Answer(models.IntegerChoices):
        option_1 = 1
        option_2 = 2
        option_3 = 3
        option_4 = 4

    correct_ans = models.IntegerField(choices=Answer.choices)

    level = models.CharField(max_length=20, default="1")

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def __str__(self):
        return self.question + ": "+ str(self.correct_ans) 

class UserResponse(models.Model):
    user      = models.ForeignKey(User, on_delete=CASCADE)
    question  = models.ForeignKey(Question, on_delete=CASCADE, null=True)
    class Answer(models.IntegerChoices):
        option_1 = 1
        option_2 = 2
        option_3 = 3
        option_4 = 4

    selected_option = models.IntegerField(choices=Answer.choices, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}: {self.question} - {self.selected_option}"


YEAR_CHOICE=[
    ("FE","FE"),
    ("SE","SE"),
    ("TE","TE"),
    ("BE","BE"),
    ("Others","Others")

]

class extendeduser(models.Model):
    number = models.CharField(max_length=20,null=True,default="")
    year = models.CharField(max_length=20, choices=YEAR_CHOICE,null=True,default="")
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    final_score = models.IntegerField(default=0)
    marking_positive=models.IntegerField(default=4)
    marking_negative=models.IntegerField(default=-2)
    number_of_submits=models.IntegerField(default=0)
    random_ques = models.TextField(null=True)
    active = models.BooleanField(default=True)
    time_counter=models.IntegerField(null=True,default=0)
    time_rz_counter=models.IntegerField(null=True,default=0)
    time_speed = models.IntegerField(null=True,default=1000)
    red_zone_active = models.BooleanField(default=False) 
    correct_ques = models.IntegerField(default=0)
    num_of_lifeline = models.IntegerField(default =0)
    prev_que_correct = models.BooleanField(default=False)
    questions_alloted = models.BooleanField(default=False)
    level = models.CharField(max_length=20,default="1")
    tab = models.IntegerField(default=25)
    redzone_skipped = models.BooleanField(default=False)
    login_time = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.user.username}'


class UserLifelineData(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    lifeline1_credits = models.IntegerField(default=0)
    class LifelineInUse(models.IntegerChoices):
        Lifeline_1 = 1
        Lifeline_2 = 2
        Lifeline_3 = 3

    lifeline_in_use = models.IntegerField(choices=LifelineInUse.choices, null=True, blank=True)