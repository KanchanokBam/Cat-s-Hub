from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

Cathub = ''
urlpatterns = [
    path('', views.HomeView.as_view(), name='Home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfilePageView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='user_profile'),
    path('cat/<int:cat_id>/', views.CatDetailView.as_view(), name='cat_detail'),
    path('cat/delete/<int:cat_id>/', views.DeleteCatView.as_view(), name='delete_cat'),
    path('edit_cat/<int:cat_id>/', views.EditCatView.as_view(), name='edit_cat'),
    path('post/', views.PostCatView.as_view(), name='post'),
    path('adopt/', views.AdoptView.as_view(), name='adopt'),
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
    path('find-cat/', views.FindCatView.as_view(), name='find_cat'),
    path('match/', views.MatchView.as_view(), name='match'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),

    # Notifications & Contact
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
    path('notifications/read/<int:notification_id>/', views.MarkNotificationAsReadView.as_view(), name='mark_notification_as_read'),
    path('clear_notifications/', views.ClearNotificationsView.as_view(), name='clear_notifications'),
    path('api/notifications/count/', views.GetNotificationCountView.as_view(), name='get_notifications_count'),
    path('api/request_contact/<int:cat_id>/', views.RequestContactView.as_view(), name='request_contact'),
    path('approve_contact/<int:contact_request_id>/', views.ApproveContactView.as_view(), name='approve_contact'),
    path('decline_contact/<int:contact_request_id>/', views.DeclineContactView.as_view(), name='decline_contact'),
    path('view_contact/<int:request_id>/', views.ViewContactInfoView.as_view(), name='view_contact'),

    # Admin Views
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin-dashboard/addcat/', views.AddCatAdminView.as_view(), name='add_cat'),
    path('admin-dashboard/adduser/', views.AddUserAdminView.as_view(), name='add_user'),
    path('admin-dashboard/edit-user/<int:user_id>/', views.EditUserAdminView.as_view(), name='edit_user'),
    path('admin-dashboard/delete-user/<int:user_id>/', views.DeleteUserAdminView.as_view(), name='delete_user'),
    path('admin-dashboard/edit/<int:cat_id>/', views.EditCatAdminView.as_view(), name='edit_cat_admin'),
    path('admin-dashboard/delete/<int:cat_id>/', views.DeleteCatAdminView.as_view(), name='admin_delete_cat'),
    path('admin-dashboard/projects/add/', views.AddProjectAdminView.as_view(), name='admin_add_project'),
    path('admin-dashboard/projects/edit/<int:project_id>/', views.EditProjectAdminView.as_view(), name='admin_edit_project'),
    path('admin-dashboard/projects/delete/<int:project_id>/', views.DeleteProjectAdminView.as_view(), name='admin_delete_project'),
    


] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)