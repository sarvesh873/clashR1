from django.contrib import admin
from .models import *

class QuestionAdmin(admin.ModelAdmin):
    list_display=('question','option_1','option_2','option_3','option_4','correct_ans')
class UserAdmin(admin.ModelAdmin):
    list_display=('user','question','selected_option')

admin.site.register(Question,QuestionAdmin)
admin.site.register(UserResponse,UserAdmin)
admin.site.register(extendeduser)
admin.site.register(UserLifelineData)