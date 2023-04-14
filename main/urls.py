from django.urls import path
from django.conf import settings

from forum_orphee.settings import MEDIA_ROOT, STATIC_ROOT
from django.conf.urls.static import static
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    #path('404', views.page_doesnt_exist, name='404'),
    path('cgu', views.cgu, name='cgu'),
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('delete', views.delete_request, name='delete'),
    path('account', views.account, name='account'),
    path('topics', views.topics, name='topics'),
    path('new_topic', views.new_topic, name='new_topic'),
    path('post_topic', views.post_topic_request, name='post_topic'),
    path('post_answer', views.post_answer_request, name='post_answer'),
    path('personal_topics', views.personal_topics, name='personal_topics'),
    path('private_message/<str:pseudo>', views.private_message, name='private_message'),
    path('private_message/<str:pseudo>/post/', views.post_private_message, name='post_private_message'),
    path('topic/<int:id_topic>', views.get_topic, name='topic'),
    path('delete_topic/<int:id_topic>/<str:confirm>', views.delete_topic, name='delete_topic'),
    path('delete_message/<int:id_message>/<int:id_topic>', views.delete_message, name='delete_message'),
    path('edit_topic/<int:id_topic>/', views.edit_topic, name='edit_topic'),
    path('edit_topic/<int:id_topic>/post/', views.post_edit_topic, name='edit_topic'),
    path('edit_message/<int:id_message>/', views.edit_message, name='edit_message'),
    path('edit_message/<int:id_message>/post/', views.post_edit_message, name='edit_message'),
    path('messages', views.messages, name='messages'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('reset_password/step2', views.reset_password_step2, name='reset_password'),
] + static(settings.MEDIA_URL, document_root=MEDIA_ROOT) + static(settings.STATIC_URL, document_root=STATIC_ROOT)