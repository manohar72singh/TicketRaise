from django.shortcuts import render, redirect
from .models import *
import datetime
import random
from django.core.mail import send_mail
from django.http import JsonResponse
# Create your views here.
def index(request):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')

    un = request.session.get('un')
    ut = request.session.get('ut')
    uid = request.session.get('uid')
    newrequest = User.objects.filter(approvedby= None)
    tnr = len(newrequest)
    newtr = Ticket.objects.filter(status=None)
    ntr = len(newtr)
    return render(request,'index.html',{'un':un,'tr':tnr,'ut':ut,'uid':uid,'ntr':ntr})

def signup(request):
    msg = ''
    msgtype =''
    utype = UserType.objects.all()
    email = request.session.get('email', 'none')
    if email == 'none':
        # user is not login redirect to login page
        return redirect('/emailverify/')
    email=request.session.get('email')
    if request.method == 'POST':
        # CHECK EMAIL ID ALREDY EXIT OR NOT
        d = User.objects.filter(email__exact=request.POST['email'])
        if len(d) != 0:
            msg = "EMAIL ID ALREADY EXIST"
            msgtype='danger'
            return render(request,'signup.html',{'msg':msg,'msgtype':msgtype})
        iutype=UserType.objects.get(id=request.POST['utype'])
        u = User(fname=request.POST['ufname'],lname=request.POST['ulname'],utype=iutype,gen=request.POST['gen'],email=request.POST['email'],pwd=request.POST['pwd'])
        u.save()
        msg='Your request for adding as a new user is recorded. pls wait for on veryfication or rejection you will get Mail on Your given Email id.'
        msgtype='success'
        del request.session['email']
    return render(request,'signup.html',{'utype':utype,'msg':msg,'msgtype':msgtype,'email':email})

def login(request):
    msg = ""
    msgtype = ''
    if request.method == 'POST':
        # CHECK USERNAME AND PASSWORD
        u = User.objects.filter(email__exact=request.POST['email']).filter(pwd__exact=request.POST['pwd'])
        if len(u) != 0:
            if u[0].approvedby != None:
                request.session['uid'] = u[0].id
                request.session['un'] = u[0].fname
                request.session['ut']= u[0].utype.type
                request.session['em']=u[0].email
                cdttm = datetime.datetime.now()
                login_details =Logindetail(users =User.objects.get(id=u[0].id),logindt=cdttm)
                login_details.save()
                if u[0].utype.type =='Admin':
                    return redirect('/index/')
                elif u[0].utype.type == 'Devloper':
                    return redirect('/devloper/')
                else:
                    return redirect('/business/')
            else:
                msg='Currently you are not able to login as your request is panding:.'
                msgtype='danger'
        else:
            msg = "invallid Email id and password"
            msgtype = 'danger'
    return render(request,'login.html',{'msg':msg,'msgtype':msgtype,})

def logout(request):
    try:
        del request.session['uid']
        # redirect to login page
        return redirect('/login/')
    except:
        # redirect to login page
        return redirect('/login/')


def viewallrequest(request):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')
    un = request.session.get('un')
    uid = request.session.get('uid')
    ut = request.session.get('ut')
    new_request = User.objects.filter(approvedby= None)
    tnr = len(new_request)
    newtr = Ticket.objects.filter(status=None)
    ntr = len(newtr)
    return render(request,'viewallrequest.html',{'uid':uid,'tr':tnr,'nr':new_request,'un':un,'ut':ut,'ntr':ntr})


def viewallrequestforbus(request):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')
    un = request.session.get('un')
    uid = request.session.get('uid')
    ut = request.session.get('ut')
    new_request = User.objects.filter(approvedby= None)
    tnr = len(new_request)
    return render(request,'viewallrequestforbus.html',{'uid':uid,'tr':tnr,'nr':new_request,'un':un,'ut':ut})

def viewallrequestfordev(request):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')
    un = request.session.get('un')
    uid = request.session.get('uid')
    ut = request.session.get('ut')
    new_request = User.objects.filter(approvedby= None)
    tnr = len(new_request)
    newtr = Ticket.objects.filter(status=None)
    ntr = len(newtr)
    return render(request,'viewallrequestfordev.html',{'uid':uid,'tr':tnr,'nr':new_request,'un':un,'ut':ut,'ntr':ntr})


def approvel_request(request,id,uid):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')
    #email=request.session.get('em')
    apr=User.objects.get(id=id)
    cdttm = datetime.datetime.now()
    apr.approveldt=cdttm
    apr.approvedby=uid
    apr.save()

    email=apr.email
    pwd=apr.pwd
    send_Mail(email, pwd)
    return redirect('/viewallrequest/')


def rejectuser(request,id):
    try:
        rec=User.objects.get(id=id)
        rec.delete()
        return redirect("/viewallrequest/")
    except:
        return redirect("/viewallrequest/")

def allactiveuser(request):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')
    un = request.session.get('un')
    uid = request.session.get('uid')
    ut = request.session.get('ut')
    newrequest = User.objects.filter(approvedby =None)
    tnr = len(newrequest)
    newtr = Ticket.objects.filter(status=None)
    ntr = len(newtr)
    #users = User.objects.filter(approvedby__isnull=False)
    users=User.objects.raw("select * from User_User where approvedby is not NULL")
    return render(request,'activeusers.html',{'un':un,'tr':tnr,'users':users,'uid':uid,'ut':ut,'ntr':ntr})

def profile(request):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')
    un = request.session.get('un')
    uid = request.session.get('uid')
    ut = request.session.get('ut')
    recs = User.objects.get(id=uid)
    return render(request,'profile.html',{'pro':recs,'un':un,'uid':uid})

def businessprofile(request):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')
    un = request.session.get('un')
    uid = request.session.get('uid')
    ut = request.session.get('ut')
    recs = User.objects.get(id=uid)
    newrequest = User.objects.filter(approvedby=None)
    tnr = len(newrequest)
    return render(request,'businessprofile.html',{'pro':recs,'un':un,'uid':uid,'tr':tnr})



def devloperprofile(request):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')
    un = request.session.get('un')
    uid = request.session.get('uid')
    ut = request.session.get('ut')
    recs = User.objects.get(id=uid)
    newrequest = User.objects.filter(approvedby=None)
    tnr = len(newrequest)
    return render(request,'devprofile.html',{'pro':recs,'un':un,'uid':uid,'tr':tnr})

def logindetail(request):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')
    new_request = User.objects.filter(approvedby=None)
    tnr = len(new_request)
    un = request.session.get('un')
    ut=request.session.get('ut')
    uall=Logindetail.objects.all()
    newtr = Ticket.objects.filter(status=None)
    ntr = len(newtr)
    return render(request,'logindetail.html',{'u':uall,'un':un,'tr':tnr,'ut':ut,'ntr':ntr})

def send_Mail(email, pwd):
    subject='Account verification'
    msg = f'your Account is verified, id:{email},password:{pwd} '
    to= [email]
    send_mail(subject,msg,'manalvi2610singh@gmail.com',to,fail_silently=False)

def e_verify(request):
    msg=''
    msgtype=''
    if request.method=='POST':
        email = request.POST['email']
        d = User.objects.filter(email__exact=request.POST['email'])
        if len(d) != 0:
            msg = "EMAIL ID ALREADY EXIST"
            msgtype = 'danger'
            return render(request,'emailverify.html',{'msg':msg,'msgtype':msgtype})

        #generate otp
        otp = random.randint(1111,9999)
        sub='Account verification'
        msg =f'Your OTP is {otp}'
        to=[email]
        send_mail(sub,msg,'manalvi2610singh@gmail.com',to,fail_silently=False)
        request.session['email']=email
        request.session['otp']=otp
        return redirect('/emailotp/')
    return render(request,'emailverify.html')

def emailotpverify(request):
    msg = ''
    msgtype=''
    email = request.session.get('email', 'none')
    if email == 'none':
        # user is not login redirect to login page
        return redirect('/emailverify/')
    em = request.session.get('email')
    otp = request.session.get('otp')
    if request.method=='POST':
        if  str(otp)==str(request.POST['otp']):

            del request.session['otp']
            return redirect('/signup/')
        else:
            msg=' invallid otp '
            msgtype='danger'
    return render(request,'emailotp.html',{'em':em,'msg':msg,'msgtype':msgtype})

def check_email(request):
    email =request.GET.get('email',None)
    data = {
        'is_taken': User.objects.filter(email__exact=email).exists()
    }
    print(data)
    return JsonResponse(data)

def devloper_home(request):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')
    un = request.session.get('un')
    ut = request.session.get('ut')
    uid = request.session.get('uid')
    newrequest = User.objects.filter(approvedby=None)
    tnr = len(newrequest)
    newtr = Ticket.objects.filter(status=None)
    ntr = len(newtr)
    return render(request,'devloper.html',{'un':un,'ut':ut,'uid':uid,'tr':tnr,'ntr':ntr})

def business_home(request):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')
    un = request.session.get('un')
    ut = request.session.get('ut')
    uid = request.session.get('uid')
    newrequest = User.objects.filter(approvedby=None)
    tnr = len(newrequest)
    return render(request,'business.html',{'un':un,'ut':ut,'uid':uid,'tr':tnr})

def ticketraise(request):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')
    msg =''
    msgtype =''
    ticket_type= Ticket_type.objects.all()
    category = Category.objects.all()

    cdttm = datetime.datetime.now()
    uid =request.session.get('uid')
    un=request.session.get('un')
    ut=request.session.get('ut')
    if request.method == 'POST':
        ttype = Ticket_type.objects.get(id=request.POST['tctype'])
        cat = Category.objects.get(id=request.POST['cat'])
        u= User.objects.get(id=uid)
        t =Ticket(user=u,category =cat,ticket_type=ttype,question=request.POST['que'],trd=cdttm,desc=request.POST['desc'])
        t.save()
        msg='ticket raise sucessfull'
        msgtype='success'
    newrequest = User.objects.filter(approvedby=None)
    tnr = len(newrequest)
    newtr = Ticket.objects.filter(status=None)
    ntr = len(newtr)
    return render(request,'ticketraise.html',{'tc':ticket_type,'cat':category,'ut':ut,'msg':msg,'msgtype':msgtype,'ntr':ntr,'un':un,'tr':tnr})



def ticketraiseB(request):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')
    msg =''
    msgtype =''
    ticket_type= Ticket_type.objects.all()
    category = Category.objects.all()

    cdttm = datetime.datetime.now()
    uid =request.session.get('uid')
    un=request.session.get('un')
    ut=request.session.get('ut')
    if request.method == 'POST':
        ttype = Ticket_type.objects.get(id=request.POST['tctype'])
        cat = Category.objects.get(id=request.POST['cat'])
        u= User.objects.get(id=uid)
        t =Ticket(user=u,category =cat,ticket_type=ttype,question=request.POST['que'],trd=cdttm,desc=request.POST['desc'])
        t.save()
        msg='ticket raise sucessfull'
        msgtype='success'
    newrequest = User.objects.filter(approvedby=None)
    tnr = len(newrequest)
    return render(request,'ticketraiseB.html',{'tc':ticket_type,'cat':category,'ut':ut,'msg':msg,'msgtype':msgtype,'un':un,'tr':tnr})

def showraiseticket(request):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')
    un = request.session.get('un')
    ticket=Ticket.objects.all()
    newrequest = User.objects.filter(approvedby=None)
    tnr = len(newrequest)
    newtr=Ticket.objects.filter(status=None)
    ntr=len(newtr)
    return render(request,'show Raise Ticket.html',{'ticket':ticket,'tr':tnr,'ntr':ntr,'un':un})

def showraiseticketD(request):
    uid = request.session.get('uid', 'none')
    if uid == 'none':
        # user is not login redirect to login page
        return redirect('/login/')
    un = request.session.get('un')
    ticket=Ticket.objects.all()
    newrequest = User.objects.filter(approvedby=None)
    tnr = len(newrequest)
    newtr=Ticket.objects.filter(status=None)
    ntr=len(newtr)
    return render(request,'showraiseticketd.html',{'ticket':ticket,'tr':tnr,'ntr':ntr,'un':un})