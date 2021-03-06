"""API_SoftDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from rest_framework_nested import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserViewSet, CreateUserAPIView
from softdesk.views import ProjectsViewSet, ContributorsViewSet, IssuesViewSet, CommentsViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename="user")
router.register(r'projects', ProjectsViewSet, basename="projects")

projects_router = routers.NestedSimpleRouter(
    router, r'projects', lookup='projects')
projects_router.register(r'users', ContributorsViewSet,
                         basename='contributors')
projects_router.register(r'issues', IssuesViewSet, basename='issues')

issues_router = routers.NestedSimpleRouter(
    projects_router, r'issues', lookup='issues')
issues_router.register(r'comments', CommentsViewSet, basename='comments')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', CreateUserAPIView.as_view()),
    path('api/obtain-token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/', include(projects_router.urls)),
    path('api/', include(issues_router.urls)),
    path('api/', include('rest_framework.urls')),
]
