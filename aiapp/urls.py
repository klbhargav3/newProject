from . import views
from django.urls import path

app_name="aiapp"

urlpatterns = [
    path("",views.login_view,name="login"),
    path("signup/",views.signup_view,name="signup"),
    path("chat/",views.chat_view,name="chat"),
    path("logout/",views.logout_view,name="logout"),
    path("history/",views.chat_history,name="history"),
    path("history/<int:id>/",views.specific_history,name="specific")
    ]
