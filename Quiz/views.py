from django.shortcuts import render,HttpResponse, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import re
import random
import json
import datetime
import pytz

# total_ques = min(Question.objects.filter(level = "1").count(),Question.objects.filter(level = "2").count() )
total_ques = 370

# Quiz View

@login_required(login_url='login')
def quiz(request):
    user=request.user
    try:
        profile = extendeduser.objects.get(user=user)
    except extendeduser.DoesNotExist:
        profile = extendeduser(user = user)
    all_ques = json.loads(profile.random_ques)
    try:
        que_dict = json.loads(all_ques[profile.number_of_submits])
    except:
        que_dict = json.loads(all_ques[profile.number_of_submits-1])
    que = Question.objects.get(pk = que_dict["id"])
    
    if request.method == 'POST':
        selected_option = int(request.POST.get('btnradio', 0))
        time_counter=int(request.POST.get('time_counter'))
        profile.time_counter=time_counter
        profile.popRZModal = False # Changes
        profile.save()
        try:
            lifeline = UserLifelineData.objects.get(user=user)
            if lifeline.lifeline_in_use is not None:
                useLifeline(user, selected_option, que)
                
                # profile.save() #too dangerous
                return redirect("Quiz")
        except:
            pass
        if profile.number_of_submits<total_ques:
            que_dict = json.loads(all_ques[profile.number_of_submits])
            que = Question.objects.get(pk = que_dict["id"])
            profile.number_of_submits+=1

            # Scoring System
            try:
                user_res = UserResponse.objects.get(question = que, user = request.user)
                user_res.selected_option = selected_option
                if(selected_option!=que.correct_ans):
                    profile.final_score+=profile.marking_negative
                    profile.marking_positive=2
                    profile.marking_negative=-1
                    profile.time_speed = 750
                elif(selected_option==que.correct_ans):
                    profile.final_score+=profile.marking_positive
                    profile.marking_positive=4
                    profile.marking_negative=-2
                    profile.correct_ques += 1
                    profile.time_speed = 2000

                # user_res.save()
                profile.save()
                return redirect("Quiz")
            except UserResponse.DoesNotExist:
                if(selected_option!=que.correct_ans):
                    profile.final_score+=profile.marking_negative
                    profile.marking_positive=2
                    profile.marking_negative=-1
                    if profile.time_speed == 1000 or profile.time_speed == 750:
                        profile.time_speed = 750
                    else:
                        profile.time_speed = 1000
                elif(selected_option==que.correct_ans):
                    profile.final_score+=profile.marking_positive
                    profile.marking_positive=4
                    profile.marking_negative=-2 
                    profile.correct_ques += 1
                    if profile.time_speed == 1000 or profile.time_speed == 2000:
                        profile.time_speed = 2000
                    else:
                        profile.time_speed = 1000
                profile.save()
                inst = UserResponse(user = request.user, question = que, selected_option = selected_option)
                inst.save()
                return redirect("Quiz")
   
    utc=pytz.UTC
    
    if datetime.datetime.now().replace(tzinfo=utc) > (profile.login_time.replace(tzinfo=utc) + datetime.timedelta(minutes=60)):
        messages.error(request,"Your Slot has ended!")
        return redirect('result')
        
    
    if profile.number_of_submits >= total_ques:
        return redirect("endquiz")
    else:
        que_dict = json.loads(all_ques[profile.number_of_submits])
    
    if not profile.red_zone_active:
        profile.time_speed = 1000
        profile.save()
    

    try:
        userlifeline = UserLifelineData.objects.get(user = user)
        if userlifeline.lifeline_in_use is not None:
            lifeline_status = "Active"
        else:
            lifeline_status = "Inactive"
    except:
        lifeline_status = "Inactive"

    try:
        accu = round(profile.correct_ques / profile.number_of_submits * 100,2)
    except:
        accu = 0

    if lifeline_status == "Inactive":
        mark_pos = profile.marking_positive
        mark_neg = profile.marking_negative
    else:
        mark_pos = profile.marking_positive + 1
        mark_neg = -int((profile.marking_positive+1) * 2 / 3)

    profiles = extendeduser.objects.filter(level = profile.level).order_by('-final_score','time_counter')

    
    
    try:
        skiplife = UserLifelineData.objects.get(user = user)
        
        if(skiplife.lifeline1_credits == 0):
            
            skip = True
        else:
            
            skip = False
    except:
        skip = False

    if profile.redzone_skipped and skip :
        profile.redzone_skipped = False
        profile.save()
        
        return redirect('skipped_red_zone')

    if profile.number_of_submits == total_ques-1:
        isLastQuestion = True
    else:
        isLastQuestion = False

    question = Question.objects.get(pk = que_dict["id"])
    rank1 = rank(user)
    context = {'question':question,   'title':"Clash Round 1", 'score':profile.final_score, 'profile':profile, 'q_no':profile.number_of_submits+1, 'lifeline_status':lifeline_status, 'accu':accu,
    'canUseLifeline':canUseLifeline(request.user), 'mark_pos':mark_pos, 'mark_neg':mark_neg, 'profiles':profiles, 'rank':rank1,
    'isLastQuestion':isLastQuestion} #'user_res':user_res,'next':next,
    return render(request,'Quiz/Qpage.html', context)


# End Quiz on time up and logout
def endquiz(request):
    user = request.user
    if request.method == 'POST':
        try:
            profile = extendeduser.objects.get(user=user)
        except extendeduser.DoesNotExist:
            profile = extendeduser(user = user)
        profile.final_score=profile.final_score
        profile.save()
        if request.POST['end'] == "timeUp":
            messages.info(request, "Oops!! Time's Up. Quiz submitted automatically.")
        elif request.POST['end'] == "submitted":
            messages.success(request, "Quiz Submitted Succesfully.")
    else:
        messages.info(request, "Question Limit reached!!! Quiz Submitted successfully")
    return redirect('result')



# Login View
def login(request):
   
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        user = auth.authenticate(
            username=request.POST['uname'], password=request.POST['pass'])
        if user is not None:
            liveuser = extendeduser.objects.get(user=user)
            if user and liveuser.active == True:
                auth.login(request, user)
                liveuser.active = False
                auth.login(request, user)
                if not liveuser.questions_alloted:
                    all_ques = list_all_questions()
                    random.shuffle(all_ques)
                    user_ques = all_ques[:70]
                    count = 0
                    if liveuser.year == 'TE' or liveuser.year == 'BE':
                        liveuser.level = "2"
                    # for i in all_ques:
                    #     if liveuser.level == i.level:
                            
                    #         user_ques.append(i.toJSON())
                    #         count += 1
                    #     if count == total_ques:
                    #         break

                    liveuser.login_time = datetime.datetime.now()

                
                    liveuser.random_ques = json.dumps(user_ques)
                liveuser.save()
            else:
                messages.error(request, "You have already given the test.")
            return redirect('profile')
        return render(request, 'Quiz/login.html', {'error': "Invaild Crededntials"})
    return render(request, 'Quiz/login.html')


#Register View
def register(request):
        if request.method == "POST":

            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    return render(request, 'Quiz/register.html', {'error': "username already exist"})

                except User.DoesNotExist:
                    number = request.POST['number']
                    year = request.POST['year']


                if (len(request.POST['password1']) < 8):
                    return render(request, 'Quiz/register.html', {'error': "Password too Short, Should Contain ATLEAST 1 Uppercase,1 lowercase,1 special Character and 1 Numeric Value"})

                elif not re.search(r"[\d]+", request.POST['password1']):
                    return render(request, 'Quiz/register.html', {'error': "Your Password must contain Atleast 1 Numeric value "})
                elif not re.findall('[A-Z]', request.POST['password1']):
                    return render(request, 'Quiz/register.html', {'error': "Your Password must contain Atleast 1 UpperCase Letter "})

                elif not re.findall('[a-z]', request.POST['password1']):
                    return render(request, 'Quiz/register.html', {'error': "Your Password must contain Atleast 1 lowercase Letter "})
                elif not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', request.POST['password1']):
                    return render(request, 'Quiz/register.html', {'error': "Your Password must contain Atleast 1 Specail character "})
                elif not re.findall('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', request.POST['email']):
                       return render(request, 'Quiz/register.html', {'error': "Email ID is not Valid"})

                else:
                    
                    if extendeduser.objects.filter(number=number):
                        return render(request, 'Quiz/register.html', {'error': "phonenumber already exist try using another one"})
                    else:
                        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'],email=request.POST['email'],first_name=request.POST['firstname'],last_name=request.POST['lstname'])
                        newextendeduser = extendeduser( number=number, year=year, user=user)
                        newextendeduser.save()
                        auth.login(request, user)
                        messages.success(
                            request, f'Your account has been Created!! Login Now')
                        
                        auth.logout(request)
                        return redirect(login)
            else:
                return render(request, 'Quiz/register.html', {'msg': ["Passwords Don't match"]})
        else:
            return render(request, "Quiz/register.html")


def logout(request):
    auth.logout(request)
    return redirect('login')


# Instruction Page
@login_required(login_url='login')
def startQuiz(request):
    datas = extendeduser.objects.filter(user = request.user)
    return render(request,'Quiz/startQuiz.html',{'data':datas})



# Handle Lifeline 1
def lifeline(request):
    profile = extendeduser.objects.get(user=request.user)
    try:
        accu = profile.correct_ques / profile.number_of_submits * 100
       
    except ZeroDivisionError:
        accu = 0
    if request.method == "POST":
        if (accu < 30):
            messages.error(request, f"Your Accuracy is {accu}%. You need atleast 30% accuracy to use this lifeline.")
        else:
            credits_used = request.POST.get('score-input')
            if int(credits_used) > 5:
                messages.error(request, "You don't have enough credits!!")
                return redirect("Quiz")
            if int(credits_used) > profile.final_score:
                messages.error(request, "You can use 5 credits at max!!")
                return redirect("Quiz")
            messages.success(request, f"Lifeline activated for next {credits_used} questions")
            createLifelineModel(request.user)
            lifeline_data = UserLifelineData.objects.get(user = request.user)
            lifeline_data.lifeline1_credits = credits_used
            lifeline_data.lifeline_in_use = 1
            lifeline_data.save()
            profile = extendeduser.objects.get(user = request.user)
            profile.marking_positive = 3
            profile.marking_negative = -3
            profile.num_of_lifeline += 1
            profile.final_score -= int(credits_used)
            profile.save()

        return redirect("Quiz")

# To create UserLifelineData Model            
def createLifelineModel(user1):
    try:
        lifeline = UserLifelineData.objects.get(user = user1)

    except:
        lifeline = UserLifelineData(user = user1)
        
        lifeline.save()

# Handle Lifeline1 
def useLifeline(user1, selected_option, que):
    lifeline = UserLifelineData.objects.get(user = user1)
    profile = extendeduser.objects.get(user = user1)

    if lifeline.lifeline_in_use == 1 and lifeline.lifeline1_credits:
        profile.marking_positive += 1
        profile.marking_negative = -int(profile.marking_positive*2/3)
        profile.save()
        lifeline.lifeline1_credits -= 1
        if lifeline.lifeline1_credits == 0:
            lifeline.lifeline_in_use = None

        lifeline.save()


    if(selected_option != que.correct_ans):
        profile.final_score+=profile.marking_negative
    elif(selected_option==que.correct_ans):
        profile.final_score+=profile.marking_positive
    profile.number_of_submits+=1
    profile.save()
    inst = UserResponse(user = user1, question = que, selected_option = selected_option)
    inst.save()
    if(lifeline.lifeline_in_use is None):
        profile.marking_positive = 4
        profile.marking_negative = -2

        profile.save()
    return

# Handle Redzone Activation    
def red_zone(request):
    profile = extendeduser.objects.get(user = request.user)
    try:
        lifeline = UserLifelineData.objects.get(user = request.user)
        if(lifeline.lifeline_in_use == 1):
            profile.redzone_skipped = True
            profile.save()
            
            return redirect('Quiz')
    except:
        pass


    timer = request.POST.get("time_counter")
    
    profile.red_zone_active = True
    profile.time_counter = timer
    profile.time_rz_counter =timer
    profile.popRZModal = True
    
    profile.save()
    messages.error(request,"Combat Zone Activated!!!!")
    return redirect('Quiz')

# End Red Zone
def endRZ(request):
    if request.method == 'POST':
        counter = request.POST.get('endRZ')
        profile = extendeduser.objects.get(user = request.user)
        profile.time_counter = counter
        profile.red_zone_active = False  
        profile.time_rz_counter = 0
        profile.time_speed = 1000
        profile.save()
        messages.info(request,"Combat Zone Ended!!!!")
    return redirect('Quiz')

# Save timer using Ajax
def saveTimer(request):
    if request.method == 'POST':
        profile = extendeduser.objects.get(user = request.user)
        profile.time_counter = request.POST.get("timer")
        profile.save()
        return HttpResponse("Timer Saved!")
 

    
# Result Page View  
    
def result(request):

    try:
        
        profile = extendeduser.objects.get(user=request.user)

        try:
            accu = round(profile.correct_ques / profile.number_of_submits * 100,2)
        except:
            accu = 0
        
        context = {'profile': profile , 'user':request.user, 'accu':accu}
        auth.logout(request)
        return  render(request,'Quiz/result.html',context)
    except:
        return redirect('login')
    
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
#Leaderboard View  
def leaderboard(request):

        # profiles = extendeduser.objects.all()
        profiles = extendeduser.objects.filter(level = "1").order_by('-final_score','time_counter')
        context = {'profile': profiles , 'user':request.user}
        return  render(request,'Quiz/leaderboard.html',context)

@staff_member_required
def leaderboard2(request):
        # profiles = extendeduser.objects.all()
        profiles = extendeduser.objects.filter(level = "2" ).order_by('-final_score','time_counter')
        context = {'profile': profiles , 'user':request.user}
        return  render(request,'Quiz/leaderboard2.html',context)



@staff_member_required
# Allow user to login again
def emerglogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        admin_username = request.POST['admin_username']
        admin_password = request.POST['admin_password']
        extra_tab=request.POST['extra_tab']
        super_user =auth.authenticate(request, username=admin_username, password=admin_password)
        
        try:
            profile = auth.authenticate(username=username, password=password )
            if profile and super_user :
                liveuser = extendeduser.objects.get(user=profile)
                
                if liveuser.time_counter >= 1680:
                    messages.info(request,"The Player has Completed All Question..!!!")
                    return render(request, 'Quiz/emerglogin.html')
                liveuser.active = True
                liveuser.tab += int(extra_tab)
                liveuser.save()
                messages.info(request,"successfull!!")
                return render(request, 'Quiz/emerglogin.html')
            messages.info(request,"Invalid Credentials!!")
            return render(request, 'Quiz/emerglogin.html')
        except:
            messages.info(request,"not valid Credentials!!")
            return render(request, 'Quiz/emerglogin.html')
    return render(request, 'Quiz/emerglogin.html')




#Handle Tab Switch
from django.http import JsonResponse
def switchtab(request):
    profile = extendeduser.objects.get(user=request.user)
    profile.tab -= 1
    profile.save()
    context = {'changed': int(profile.tab)}
    return JsonResponse(context)


# Resolve Lifeline Redzone Clash
def skipped_red_zone(request):
    profile = extendeduser.objects.get(user = request.user)
    
    profile.red_zone_active = True
    profile.time_rz_counter = profile.time_counter
    
    
    profile.save()
    messages.error(request,"Red Zone Started!!!!")
    return redirect('Quiz')


# -------------------Utility functions--------------------

def list_all_questions():
    all_ques = []
    for que in Question.objects.all():
        all_ques.append(que.toJSON())
    return all_ques

def rank(user):
    exuser  = extendeduser.objects.get(user = user)
    all_users = extendeduser.objects.filter(level = exuser.level).order_by('final_score','-time_counter').reverse()
    for i in range(len(all_users)):
        if all_users[i].user == user:
            return i+1
    return 0

#Check if user can use lifeline 1
def canUseLifeline(user1):
    profile = extendeduser.objects.get(user = user1)
    try:
        accu = round(profile.correct_ques / profile.number_of_submits * 100,2)
    except:
        accu = 0
    try:
        lifeline = UserLifelineData.objects.get(user = user1)
        inuse =lifeline.lifeline_in_use
    except:
        inuse = None
    if profile.num_of_lifeline < 2 and inuse == None and accu >=30 and not profile.red_zone_active and profile.final_score >= 5:
        return True
    return False


def errorhandle(request,exception):
    return render(request,'Quiz/login.html')

def webteam(request):
    return render(request,'Quiz/webteam.html')