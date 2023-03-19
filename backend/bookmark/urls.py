from django.urls import path

from bookmark import views

urlpatterns = [
    path('newest-bookmarks/', views.NewestBookmarksList.as_view()),
    path('used-bookmarks/', views.UsedBookmarksList.as_view()),
    path('bookmarks/', views.BookmarksList.as_view()),
    path('bookmarks/<int:bookmark_id>/',
         views.BookmarksList.as_view()),
    path('categorys/<slug:category_slug>/', views.CategoryList.as_view()),
    path('categorys/', views.CategoryList.as_view()),
    path('add-copy-bookmark/<int:bookmark_id>/', views.addCopy),
    path('new-default-category/', views.newCategoryDefault),
]
