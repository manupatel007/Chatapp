from django.shortcuts import render
from .models import ChatData, ChatRelation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json

dict1 = {}

# Create your views here.
@csrf_exempt
def chat_home(request):
    #if request.method == 'POST':
    personp = request.user.username
    #personp2 = request.POST.get('text2')
    #dbba = ChatData.objects.filter( (Q(person_head=personp) & Q(person_tail=personp2)) | (Q(person_head=personp2) & Q(person_tail=personp))).order_by('date')
    dbba = ChatData.objects.filter(Q(person_head=personp) | Q(person_tail=personp)).order_by('date')
    if(len(dbba)==0):
        chtdt = ChatData(person_head="Chatapp", person_tail=personp, body="Hey! " + personp + "Warm welcome to this chatapp...")
        chtdt.save()
        dbba = ChatData.objects.filter(Q(person_head=personp) | Q(person_tail=personp)).order_by('date')
    #dbba = ChatData.objects.all().order_by('date')
    l=[]
    for dbb in dbba:
        if dbb.person_head not in l and dbb.person_head!=personp:
            l.append(dbb.person_head)
            dict1[dbb.person_head]=1
        elif dbb.person_head!=personp:
            dict1[dbb.person_head]+=1
        if dbb.person_tail not in l and dbb.person_tail!=personp:
            l.append(dbb.person_tail)
            dict1[dbb.person_tail]=1
        elif dbb.person_tail!=personp:
            dict1[dbb.person_tail]+=1

    context = {
        'dbba':dbba,
        'personp':personp,
        'human':l,
    }
    return render(request, 'chat.html', context)

@csrf_exempt
def create(request, personp, personp2):
    #print("hello")
    ResponseData = {}
    if request.POST.get('action')=='post':
        body = request.POST.get('body')
        chtdt = ChatData(person_head=personp, person_tail=personp2, body=body)
        chtdt.save()
        ResponseData['body'] = body
        ResponseData['date'] = chtdt.date.strftime("%B %d, %Y | %H:%M %p")
        if personp2 not in dict1:
            dict1[personp2]=1
        else:
            dict1[personp2]+=1
        #Unread_msg code start(jha inko fetch krna h.. wha query ulti likhna)
        info = ChatRelation.objects.filter(person_head=personp2, person_tail=personp)
        if(len(info)==0):
            chtr = ChatRelation(person_head=personp2, person_tail=personp)
            chtr.save()
            chtr.unread_msg_present+=1
            chtr.save()
        else:
            #info[0].update(unread_msg_previous=info[0].unread_msg_present)
            #previous ko ajax update k time hi use krenge
            info[0].unread_msg_present+=1
            info[0].save()
        #Unread_msg code ends
        #print("hi")
        return JsonResponse(ResponseData)

@csrf_exempt
def who(request):
    return render(request, 'who.html', {})

'''def ajax_update(request, personp, personp2):
    dbba = ChatData.objects.filter( (Q(person_head=personp) & Q(person_tail=personp2)) | (Q(person_head=personp2) & Q(person_tail=personp))).order_by('date')
    #dbba = ChatData.objects.filter(person_head=personp, person_tail=personp2)
    #dbba2 = ChatData.objects.filter(person_head=personp2, person_tail=personp)
    #dbba.union(dbba,dbba2)
    #print(dbba)
    responsedbba = {}
    responsedbba['dbba'] = []
    #responsedbba['dbba2'] = []
    a={}
    for dbb in dbba:
        a={}
        a['person_head']=dbb.person_head
        a['body']=dbb.body
        a['date']=dbb.date.strftime("%B %d, %Y | %H:%M %p")

        responsedbba['dbba'].append(a)
    #print(responsedbba)
    return JsonResponse(responsedbba)'''

@csrf_exempt
def ajax_update(request, personp, personp2):
    #dbba = ChatData.objects.filter( (Q(person_head=personp) & Q(person_tail=personp2)) | (Q(person_head=personp2) & Q(person_tail=personp))).order_by('date')
    #dbba = ChatData.objects.filter(person_head=personp, person_tail=personp2)
    #dbba2 = ChatData.objects.filter(person_head=personp2, person_tail=personp)
    #dbba.union(dbba,dbba2)

    #ajax_update se ane wale data k saath khel shuru

    arr = request.POST.get('body')
    data = json.loads(arr)
    #print(data)

    #ajax_update se ane wale data k saath khel khtm

    dbba_info = ChatRelation.objects.filter(person_head=personp).order_by('date')
    dbba = ChatData.objects.filter(Q(person_head=personp) | Q(person_tail=personp)).order_by('date')
    #print(dbba)
    responsedbba = {}
    responsedbba['saman'] = {}
    responsedbba['kitna_msg'] = {}
    l=[]
    w={}    #wil be compared with dict1
    cnt=0
    for dbb in dbba:
        #cnt+=1
        if dbb.person_head not in responsedbba['saman'] and dbb.person_head!=personp:
            responsedbba['saman'][dbb.person_head] = []
            w[dbb.person_head]=1
        elif dbb.person_head!=personp:
            w[dbb.person_head]+=1

        if dbb.person_tail not in responsedbba['saman'] and dbb.person_tail!=personp:
            responsedbba['saman'][dbb.person_tail] = []
            w[dbb.person_tail]=1
        elif dbb.person_tail!=personp:
            w[dbb.person_tail]+=1

    '''for x in w:
        if x not in dict1:
            dict1[x]=0
        responsedbba['kitna_msg'][x] = w[x]-dict1[x]
        dict1[x] = w[x]'''

    

    #print("cnt:"+str(cnt))
    #print(dict1,w)
    #del responsedbba[personp]
    #responsedbba['dbba'] = []
    #responsedbba['dbba2'] = []
    a={}
    for dbb in dbba:
        a={}
        a['person_head']=dbb.person_head
        a['body']=dbb.body
        a['date']=dbb.date.strftime("%B %d, %Y | %H:%M %p")
        if(dbb.person_head!=personp):
            responsedbba['saman'][dbb.person_head].append(a)
        else:
            responsedbba['saman'][dbb.person_tail].append(a)

    for dbb in dbba_info:
        if dbb.person_tail in data:
            responsedbba['kitna_msg'][dbb.person_tail]= dbb.unread_msg_present-dbb.unread_msg_previous
            dbb.unread_msg_present -= dbb.unread_msg_previous
            dbb.unread_msg_previous = dbb.unread_msg_present+0
            dbb.save()
        else:
            responsedbba['kitna_msg'][dbb.person_tail]= dbb.unread_msg_present
            dbb.unread_msg_previous = dbb.unread_msg_present+0
            dbb.save()
        #responsedbba['kitna_msg'][dbb.person_tail]=
    #print(responsedbba)
    #print(dict1)
    return JsonResponse(responsedbba)

@csrf_exempt
def check_username(request):
    dbba = ChatData.objects.all()
    l=[]
    for dbb in dbba:
        if dbb.person_head not in l:
            l.append(dbb.person_head)
        if dbb.person_tail not in l:
            l.append(dbb.person_tail)
    data = request.POST.get('username')
    #print(data, l)
    if data not in l:
        return JsonResponse({'result':'yes'})
    else:
        return JsonResponse({'result':'no'})

def register(request):
    return render(request,'register.html',{})
