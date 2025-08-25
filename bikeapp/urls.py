
from django.urls import path
from . import views 

urlpatterns = [
    path('',views.index),
    path('reg',views.reg),
    path('log',views.log,name='log'),
    path('sign-out',views.sign_out),
    path('low',views.low,name='low'),# 1:key , 2:views function
    path('loc',views.loc,name='loc'),
    path('custom',views.cust),
    # path('edit/<int:idno>',views.edit,name="edit"),
    # path('edit1/<int:idno>',views.edit,name="edit1"),
    path('approve/<int:idno>/', views.approve_request, name='approve_request'),
    path('reject/<int:idno>/', views.reject_request, name='reject_user'),
    path('approve_w/<int:idno>/', views.approve_reqwork, name='approve_w'),
    path('reject_w/<int:idno>/', views.reject_reqwork, name='reject_w'),
    path('profile/', views.profile, name='profile'),
    path('custprofile/', views.cprofile, name='cprofile'),
    path('go-back/', views.go_back, name='go_back'),
    path('work/locate',views.location),
    path('custlocate',views.custlocation,name='custlocate'),
    path('matches', views.match_pickup, name='match_pickup'),
    # path('booking/<str:worker>/custom', views.book_ride, name='booking_page'),
    path('book_ride/<str:worker_username>/custom', views.book_ride, name='booking_page'),
    path("bookings/", views.booking_list, name="booking_list"),
    path('work/bikes',views.bikes),
    path("feedback/add/", views.add_feedback, name="add_feedback"),
    path("feedbacks/", views.feedback_list, name="feedbacks"),
    path('custfeedback',views.custfeed),
    path("work/list/", views.worker_work_list, name="worker_work_list"),
    path("work_assigned/<str:customer_username>/", views.worker_assigned_work, name="work_assigned"),
    path("work/", views.worker_dashboard, name="worker_dashboard"),

]