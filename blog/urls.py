from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('post/<slug:slug>/', views.post_detail, name='post-detail'),
    path('create/',views.post_create,name = 'post-create'),
    path('post/<slug:slug>/update/',views.post_update,name='post-update'),
    path('post/<slug:slug>/delete/',views.post_delete,name='post-delete'),
    path('post/<slug:slug>/like/',views.toggle_like,name='toggle_like'),
    path('comment/<int:pk>/delete',views.comment_delete,name='comment-delete')
]