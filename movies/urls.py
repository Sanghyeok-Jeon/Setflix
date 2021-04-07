from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('community/', views.community, name='community'),
    path('<int:movie_pk>/review_form/', views.review_form, name="review_form"),
    path('<int:review_pk>/', views.review_detail, name='review_detail'),
    path('<int:review_pk>/delete/', views.delete, name='delete'),
    path('<int:review_pk>/update/', views.update, name='update'),
    path('<int:review_pk>/like/', views.like, name='like'),
    path('<int:review_pk>/comment_create/', views.comment_create, name='comment_create'),
    path('<int:review_pk>/comment_create/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:movie_pk>/movie_detail/', views.movie_detail, name='movie_detail'),
    path('recommend1/', views.recommend1, name='recommend1'),
    path('recommend1/<int:genre_pk>/', views.recommend2, name='recommend2'),
    path('recommend1/<int:genre_pk>/<str:nation>/', views.recommend3, name='recommend3'),
    path('recommend1/<int:genre_pk>/<str:nation>/<str:popular>/', views.recommend4, name='recommend4'),
    path('recommend1/<int:genre_pk>/<str:nation>/<str:popular>/<str:vote>/', views.recommend_result, name='recommend_result'),
    path('recommend1/anything/', views.recommend_anything, name='recommend_anything'),
    path('recommend/<int:pk>/', views.recommend_genre, name='recommend_genre'),
]