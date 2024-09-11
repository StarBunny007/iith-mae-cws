from django.urls import path
from . import views
from django.urls import include, path, re_path
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.order, name='order'),
    path('orders/', views.all_orders, name='all_orders'),
    path('pending_orders/', views.pending_orders, name='pending_orders'),
    path('unapproved_orders/', views.unapproved_orders, name='unapproved_orders/'),
    path('completed_orders/', views.completed_orders, name='completed_orders'),
    path('rejected_orders/', views.rejected_orders, name='rejected_orders'),
    path('status_list/', views.status_list, name='status_list'),
    path('status_completed_list/', views.status_completed_list, name='status_completed_list'),
    path('login/', views.login_menu, name='login_menu'),
    path('do_login/', views.do_login, name='do_login'),
    path('do_register/', views.do_register, name='do_register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('approve_orders/', views.approve_orders, name='approve_orders'),
      re_path(r'^detail/(?P<order_id>[0-9]+)/$', views.detail, name='detail'),
    re_path(r'^order_decision/(?P<order_id>[0-9]+)/$', views.decision_input, name='decision_input'),
    re_path(r'^decision/(?P<order_id>[0-9]+)/$', views.decision, name='decision'),
    re_path(r'^update_status/(?P<order_id>[0-9]+)/$', views.update_status, name='update_status'),
    re_path(r'^order_decision/(?P<order_id>[0-9]+)/(?P<prof_hash>[0-9A-Za-z_\-]+)/$', views.prof_decision_form, name='prof_decision_form'),
    re_path(r'^decision/(?P<order_id>[0-9]+)/(?P<prof_hash>[0-9A-Za-z_\-]+)$', views.prof_decision, name='prof_decision'),
    re_path(r'^details/(?P<order_id>[0-9]+)/(?P<mail_hash>[0-9A-Za-z_\-]+)/$', views.detail_hash, name='detail_hash'),
]
