from django.urls import path
from .views import generateEmphasisView, homePageView, emphasisHistoryView, EditTitle, settings_page, DeleteHighlightView


urlpatterns = [
    path("emphasize/", generateEmphasisView, name='emphasis'),
    path("", homePageView, name='home'), 
    path("emphasize/<str:slug>/", emphasisHistoryView, name='detail'),
    path("edit/<str:slug>/", EditTitle.as_view(), name='edit'),
    path("settings/", settings_page, name='settings'),
    path("delete/<str:slug>/", DeleteHighlightView.as_view(), name='delete'),
]