from django.shortcuts import render
from .models import ChatData
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

# Create your views here.
@csrf_exempt
def chat_home(request):
    if request.method == 'POST':
        personp = request.POST.get('text')
        #personp2 = request.POST.get('text2')
        #dbba = ChatData.objects.filter( (Q(person_head=personp) & Q(person_tail=personp2)) | (Q(person_head=personp2) & Q(person_tail=personp))).order_by('date')
        dbba = ChatData.objects.all().order_by('date')
        l=[]
        for dbb in dbba:
            if dbb.person_head not in l:
                l.append(dbb.person_head)
        context = {
            'dbba':dbba,
            'personp':personp,
            'human':l,
        }
        return render(request, 'chat.html', context)
    else:
        dbba = ChatData.objects.all()
        print(dbba)
        context = {
            'dbba':dbba,
        }
        return render(request, 'chat.html', context)

def create(request, personp, personp2):
    ResponseData = {}
    if request.POST.get('action')=='post':
        body = request.POST.get('body')
        chtdt = ChatData(person_head=personp, person_tail=personp2, body=body)
        chtdt.save()
        ResponseData['body'] = body
        return JsonResponse(ResponseData)

@csrf_exempt
def who(request):
    return render(request, 'who.html', {})

def ajax_update(request, personp, personp2):
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
    '''for dbb in dbba2:
        a={}
        a['person_head']=dbb.person_head
        a['body']=dbb.body
        responsedbba['dbba2'].append(a)'''
    #print(responsedbba)
    return JsonResponse(responsedbba)
