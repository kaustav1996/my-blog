from django.conf.urls import url
from django.conf.urls.static import static
from .django_blog_it.views import *
from .posts.views import *
from .settings import MEDIA_URL, MEDIA_ROOT
from django.views.generic.base import RedirectView
from .payments import urls as payment_urls

from django.conf.urls import include 

favicon_view = RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^$', Home.as_view(), name='index'),
    url(r'^blog/contact/$', contact_us, name='contact_us'),
    url(r'^blog/category/(?P<category_slug>[-\w]+)/$', SelectedCategoryView.as_view(), name='selected_category'),
    url(r'^blog/tags/(?P<tag_slug>[-\w]+)/$', SelectedTagView.as_view(), name='selected_tag'),
    url(r'^blog/(?P<year>\w{0,})/(?P<month>\w{0,})/$', ArchiveView.as_view(), name='archive_posts'),
    url(r'^blog/(?P<blog_slug>[-\w]+)/$', BlogPostView.as_view(), name='blog_post_view'),
    url(r'^payments/', include(payment_urls), name='payments'),
    url(r'^dashboard/$', AdminLoginView.as_view(), name='admin_login'),
    url(r'^dashboard/gplus/$', google_login, name='google_login'),
    url(r'^fb/$', facebook_login, name='facebook_login'),
    url(r'^dashboard/logout/$',
        admin_logout,
        name='admin_logout'),
    url(r'^dashboard/blog/$',
        PostList.as_view(),
        name='blog'),
    url(r'^dashboard/add/$',
        PostCreateView.as_view(),
        name='blog_add'),
    url(r'^dashboard/view/(?P<blog_slug>[-\w]+)/$',
        PostDetailView.as_view(),
        name='view_blog'),
    url(r'^dashboard/delete/(?P<blog_slug>[-\w]+)/$',
        PostDeleteView.as_view(),
        name='delete_blog'),
    url(r'^dashboard/edit/(?P<blog_slug>[-\w]+)/$',
        PostEditView.as_view(),
        name='edit_blog'),
    url(r'^dashboard/bulk_actions_blog/$',
        BlogPostBulkActionsView.as_view(),
        name='bulk_actions_blog'),

    url(r'^dashboard/category/$', CategoryList.as_view(), name='categories'),
    url(r'^dashboard/category/add/$', CategoryCreateView.as_view(), name='add_category'),
    url(r'^dashboard/category/edit/(?P<category_slug>[-\w]+)/$', CategoryUpdateView.as_view(), name='edit_category'),
    url(r'^dashboard/category/delete/(?P<category_slug>[-\w]+)/$', CategoryDeleteView.as_view(), name='delete_category'),
    url(r'^dashboard/category/status/(?P<category_slug>[-\w]+)/$', CategoryStatusUpdateView.as_view(), name='category_status_update'),
    # pages
    url(r'^dashboard/bulk_actions_category/$',
        CategoryBulkActionsView.as_view(), name='bulk_actions_category'),

    url(r'^dashboard/pages/$', PagesListView.as_view(), name='pages'),
    url(r'^dashboard/pages/add/$', PageCreateView.as_view(), name='add_page'),
    url(r'^dashboard/pages/edit/(?P<page_slug>[-\w]+)/$',
        PageUpdateView.as_view(), name='edit_page'),
    url(r'^dashboard/pages/update/(?P<page_slug>[-\w]+)/$',
        page_status_update, name='page_status_update'),
    url(r'^dashboard/pages/delete/(?P<page_slug>[-\w]+)/$',
        PageDeleteView.as_view(), name='delete_page'),
    url(r'^dashboard/bulk_actions_pages/$',
        BulkActionsPageView.as_view(), name='bulk_actions_pages'),
    url(r'^(?P<page_slug>[-\w]+)/$', PageView, name='page_view'),

    url(r'^dashboard/upload_photos/$', upload_photos, name='upload_photos'),
    url(r'^dashboard/recent_photos/$', recent_photos, name='recent_photos'),
    url(r'^dashboard/users/$', UserListView.as_view(), name='users'),
    url(r'^dashboard/users/add/$', UserCreateView.as_view(), name='add_user'),
    url(r'^dashboard/user/edit/(?P<pk>[-\w]+)/$', UserUpdateView.as_view(), name='edit_user'),
    url(r'^dashboard/user/update/(?P<pk>[-\w]+)/$', user_status_update, name='user_status_update'),
    url(r'^dashboard/user/edit/(?P<pk>[-\w]+)/user_role/$',
        edit_user_role, name='edit_user_role'),
    url(r'^dashboard/user/delete/(?P<pk>[-\w]+)/$',
        UserDeleteView.as_view(), name='delete_user'),
    url(r'^dashboard/bulk_actions_users/$',
        UserBulkActionsView.as_view(), name='bulk_actions_users'),

    # menu management
    url(r'^dashboard/menu/$', MenuListView.as_view(), name='menus'),
    url(r'^dashboard/menu/add/$', MenuCreateView.as_view(), name='add_menu'),
    url(r'^dashboard/menu/edit/(?P<pk>[-\w]+)/$', MenuUpdateView.as_view(), name='edit_menu'),
    url(r'^dashboard/menu/update/(?P<pk>[-\w]+)/$', menu_status_update, name='menu_status_update'),
    url(r'^dashboard/bulk_actions_menu/$',
        MenuBulkActionsView.as_view(), name='bulk_actions_menu'),

    # themes management
    url(r'^dashboard/themes/$', ThemesList.as_view(), name='themes'),
    # url(r'^dashboard/themes/add/$', add_theme, name='add_theme'),
    url(r'^dashboard/themes/add/$',
        ThemeCreateView.as_view(),
        name='add_theme'),
    url(r'^dashboard/themes/(?P<theme_slug>[-\w]+)/$',
        ThemeDetailView.as_view(),
        name='view_theme'),
    url(r'^dashboard/themes/edit/(?P<pk>[0-9]+)/$',
        ThemeUpdateView.as_view(),
        name='edit_theme'),
    # url(r'^dashboard/themes/edit/(?P<theme_slug>[-\w]+)/$',
    #     edit_theme, name='edit_theme'),
    url(r'^dashboard/themes/delete/(?P<pk>[-\w]+)/$',
        DeleteThemeView.as_view(),
        name='delete_theme'),
    # url(r'^dashboard/themes/delete/(?P<theme_slug>[-\w]+)/$',
    #     delete_theme, name='delete_theme'),
    url(r'^dashboard/bulk_actions_themes/$',
        ThemesBulkActionsView.as_view(), name='bulk_actions_themes'),

    url(r'^dashboard/themes/update/(?P<theme_slug>[-\w]+)/$',
        theme_status_update,
        name='theme_status_update'),

    url(r'^dashboard/contactUs/$',
        configure_contact_us, name='configure_contact_us'),
    url(r'^dashboard/change-password/$', ChangePasswordView.as_view(), name='change_password'),
    url(r'^favicon\.ico$', favicon_view),

] + static(MEDIA_URL, document_root=MEDIA_ROOT)
