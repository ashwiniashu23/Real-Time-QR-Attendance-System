from django.contrib import admin
from django.urls import path, include
from . import views

handler403 = 'myapp.views.403'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('signin',views.Signin,name='signin'),
    path('signup',views.Signup),
    path('logout',views.SignOut, name="Signout"),
    path('qrcode',views.show_qr_token, name="qrcode"),
    path('dashboard',views.dashboard,name='dashboard'),
    path('info', views.info, name="client"),
    path('otp', views.my_function, name="otp"),
    path('attendance/<str:token>/', views.attendance_redirect, name='attendance_redirect'),
    path('attendance/view',views.attendance_view, name="view_attendance"),
    path('attendance/edit',views.attendance_edit, name="edit_attendance"), # to be changed
    path('attendance/absent',views.mark_all_absent_for_new_day, name="absent"),
    path('location',views.location, name="location"),
]


