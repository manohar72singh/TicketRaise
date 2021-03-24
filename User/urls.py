from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('index/',views.index),
    path('signup/',views.signup),
    path('login/',views.login),
    path('logout/',views.logout),
    path('viewallrequest/',views.viewallrequest),
    path('viewallrequestB/',views.viewallrequestforbus),
    path('viewallrequestD/',views.viewallrequestfordev),
    path('approveduser/<int:id>/<int:uid>',views.approvel_request),
    path('rejectuser/<int:id>/',views.rejectuser),
    path('profile/',views.profile),
    path('businessprofile/',views.businessprofile),
    path('devloperprofile/',views.devloperprofile),
    path('activeuser/',views.allactiveuser),
    path('logindetail/',views.logindetail),
    path('emailverify/',views.e_verify),
    path('emailotp/',views.emailotpverify),
    path('check_email/',views.check_email),
    path('devloper/',views.devloper_home),
    path('business/',views.business_home),
    path('ticketraise/',views.ticketraise),
    path('ticketraiseB/',views.ticketraiseB),
    path('showraiseticket/',views.showraiseticket),
    path('showraiseticketd/',views.showraiseticketD),
]