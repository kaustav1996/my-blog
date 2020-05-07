import os
import requests
import json
from datetime import datetime
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django_blog_it.django_blog_it.models import Post, Category, Tags, Page
from django_blog_it.django_blog_it.forms import ContactForm
from django.db.models import Count
from django_blog_it import settings
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.views.generic import ListView, DetailView
from django.shortcuts import render_to_response
from django.urls import reverse
from microurl import google_mini
from django_blog_it.django_blog_it.models import ContactUsSettings, Post_Slugs
from django.http import Http404
from django.shortcuts import redirect
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import  formatdate
from email import encoders


def send_mail(send_from, send_to, subject, text, files=[]):
  smtp = smtplib.SMTP('smtp.gmail.com', 587)
  smtp.ehlo()
  smtp.starttls()
  smtp.ehlo()
  smtp.login("kaustavsmailbox21@gmail.com", "kaustav@123")
  msg = MIMEMultipart()
  msg['From'] = send_from
  msg['To'] = ','.join(send_to)
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = subject
  msg.attach( MIMEText(text,'html') )
  for f in files:
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(f,"rb").read() )
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
    msg.attach(part)
  smtp.sendmail(send_from, send_to, msg.as_string())
  smtp.close()



def categories_tags_lists():
    categories_list = Category.objects.filter(is_active=True, post__status='Published').distinct()
    tags_list = Tags.objects.annotate(
        Num=Count('rel_posts')).filter(Num__gt=0, rel_posts__status='Published', rel_posts__category__is_active=True)[:20]
    posts = Post.objects.filter(status='Published').order_by('-updated_on')[0:3]
    return {'categories_list': categories_list, 'tags_list': tags_list, 'recent_posts': posts}


# def seperate_tags():
#     posts_tags = Post.objects.filter(category__is_active=True, status='Published')
#     for blog in posts_tags:
#         blog_tags_new = blog.tags.split(',')
#         for tag in blog_tags_new:
#             real_tags = Tags.objects.get(slug=tag)
#             return real_tags


class Home(ListView):
    template_name = "posts/new_index.html"
    queryset = Post.objects.filter(status='Published', category__is_active=True).order_by('-updated_on')
    context_object_name = "blog_posts"

    def get_context_data(self, *args, **kwargs):
        context = super(Home, self).get_context_data(*args, **kwargs)
        context.update({
            "description": settings.BLOG_DESCRIPTION,
            "title": settings.BLOG_TITLE,
            "keywords": settings.BLOG_KEYWORDS,
            "author": settings.BLOG_AUTHOR,
        })
        context.update(categories_tags_lists())
        return context


class BlogPostView(DetailView):
    template_name = 'posts/new_blog_view.html'
    model = Post
    slug_url_kwarg = "blog_slug"
    context_object_name = "blog_name"

    def dispatch(self, request, *args, **kwargs):
        self.object = Post.objects.filter(slug=kwargs.get("blog_slug")).last()
        if not self.object:
            post_slug = get_object_or_404(Post_Slugs, slug=self.kwargs.get("blog_slug"))
            if self.kwargs.get("blog_slug") != post_slug.blog.slug:
                return HttpResponseRedirect(reverse('blog_post_view', kwargs={"blog_slug": post_slug.blog.slug}), status=301)
        return super(BlogPostView, self).dispatch(request, *args, **kwargs)

    def get_mini_url(self, request):
        url = request.build_absolute_uri()
        try:
            api_key = os.getenv('API_KEY')
            url = google_mini(url, api_key)
        except Exception:
            pass
        return url

    def get_context_data(self, *args, **kwargs):
        context = super(BlogPostView, self).get_context_data(*args, **kwargs)
        user = self.object.user
        author = user.first_name if user.first_name else user.username
        related_posts = Post.objects.filter(
            status='Published',
            category=self.object.category,
            tags__in=self.object.tags.all()
        ).exclude(id=self.object.id).distinct()[:3]
        context.update({
            "related_posts": related_posts,
            "disqus_shortname": getattr(settings, 'DISQUS_SHORTNAME'),
            "description": self.object.meta_description if self.object.meta_description else "",
            "title": self.object.title,
            "keywords": self.object.keywords,
            "author": author,
            "short_url": self.get_mini_url(self.request),
            "blog_title": settings.BLOG_TITLE
        })
        context.update(categories_tags_lists())
        return context


class SelectedCategoryView(ListView):
    template_name = "posts/new_index.html"
    context_object_name = "blog_posts"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get("category_slug"))
        return Post.objects.filter(category=self.category, category__is_active=True, status='Published')

    def get_context_data(self, *args, **kwargs):
        context = super(SelectedCategoryView, self).get_context_data(*args, **kwargs)
        user = self.category.user
        author = user.first_name if user.first_name else user.username
        context.update({
            "description": self.category.description,
            "title": self.category.name,
            "keywords": self.category.meta_keywords,
            "author": author,
            "category": self.category,
        })
        context.update(categories_tags_lists())
        return context


class SelectedTagView(ListView):
    template_name = "posts/new_index.html"
    context_object_name = "blog_posts"

    def get_queryset(self):
        self.tag = get_object_or_404(Tags, slug=self.kwargs.get("tag_slug"))
        return get_list_or_404(Post, tags=self.tag, status='Published', category__is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(SelectedTagView, self).get_context_data(*args, **kwargs)
        context.update({
            "description": self.tag.name,
            "title": self.tag.name,
            "keywords": self.tag.name,
            "author": settings.BLOG_AUTHOR,
            "tag": self.tag,
        })
        context.update(categories_tags_lists())
        return context


class ArchiveView(ListView):
    template_name = "posts/new_index.html"
    context_object_name = "blog_posts"

    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        self.date = datetime(int(year), int(month), 1)
        return Post.objects.filter(
            category__is_active=True, status="Published", updated_on__year=year, updated_on__month=month).order_by('-updated_on')

    def get_context_data(self, *args, **kwargs):
        context = super(ArchiveView, self).get_context_data(*args, **kwargs)
        context.update({
            "description": "Blog Archive - " + self.date.strftime("%B %Y"),
            "title": "Blog Archive - " + self.date.strftime("%B %Y"),
            "keywords": "Blog Archive - " + self.date.strftime("%B %Y"),
            "author": settings.BLOG_AUTHOR,
            "date": self.date,
        })
        context.update(categories_tags_lists())
        return context

def PageView(request,page_slug):
    p=Page.objects.get(slug=page_slug)
    print(p.title)
    print(p.content)
    template="posts/page.html"
    return render(request, template, {'page': p})

# class PageView(DetailView):
#     template_name = "posts/page.html"
#     model = Page
#     slug_field = 'slug'
#     slug_url_kwarg = "page_slug"
#     context_object_name = "page"

    # def get_object(self, **kwargs):
    #     print(kwargs)
    #     p=Page.objects.get(slug=self.kwargs['page_slug'])
    #     print(p.title)
    #     print(p.content)
    #     return p
    # def get(self, request, *args, **kwargs):
    #     try:
    #         self.object = self.get_object()
    #     except Http404:
    #         # redirect here
    #         return redirect('')
    #     context = self.get_context_data(object=self.object)
    #     return self.render_to_response(context)


def contact_us(request):
    form = ContactForm()
    if request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            if os.getenv("GOOGLE_CAPTCHA_SECRET_KEY"):
                payload = {'secret': os.getenv("GOOGLE_CAPTCHA_SECRET_KEY"),
                           'response': request.POST.get('g-recaptcha-response'),
                           'remoteip': request.META.get('REMOTE_ADDR')}
                r = requests.get('https://www.google.com/recaptcha/api/siteverify', params=payload)
                if not json.loads(r.text)['success']:
                    return JsonResponse({'error': True, 'response': {"captcha": "Invalid captcha"}})
            # email sending
            contact_us = ContactUsSettings.objects.last()
            # email to admin
            subject = 'Blog Suggestions - ' + form.cleaned_data.get("contact_name")
            from_email = form.cleaned_data.get("contact_email")
            context = {
                "NAME_OF_USER": form.cleaned_data.get("contact_name"),
                "EMAIL_OF_USER":from_email,
                "WEBSITE_OF_USER": form.cleaned_data.get("contact_website"),
                "USER_DESCRIPTION": form.cleaned_data.get("content"),
                "BLOG_TITLE": settings.BLOG_TITLE
            }
            html_content = render_to_response('emails/email_to_admin.html', context).content.decode("utf-8")
            send_mail(from_email, [contact_us.email_admin] , subject, html_content,[])
            # msg = EmailMultiAlternatives(subject, subject, from_email, [contact_us.email_admin])
            # # msg.attach(html_content, 'text/html')
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            # email to user
            subject = 'Thank you for contacting us - ' + settings.BLOG_TITLE
            from_email = contact_us.from_email
            context = {
                "BODY_USER": contact_us.body_user,
                "BLOG_TITLE": settings.BLOG_TITLE
            }
            html_content = render_to_response('emails/email_to_user.html', context).content.decode("utf-8")
            send_mail(from_email, [form.cleaned_data.get("contact_email")] , subject, html_content,[])
            # headers = {'Reply-To': contact_us.reply_to_email}
            # msg = EmailMultiAlternatives(subject, subject, from_email, [form.cleaned_data.get("contact_email")], headers=headers)
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            # end
            messages.success(
                request, 'Successfully Submitted !! I will get back to you soon.')
            data = {'error': False,
                    'response': 'Successfully Submitted !! I will get back to you soon.'}
        else:
            data = {'error': True, 'response': form.errors}
        return JsonResponse(data)

    context = {"description": settings.BLOG_DESCRIPTION,
               "title": settings.BLOG_TITLE,
               "keywords": settings.BLOG_KEYWORDS,
               "author": settings.BLOG_AUTHOR,
               "contact_form": form}

    if os.getenv("GOOGLE_CAPTCHA_SITE_KEY"):
        context.update({"GOOGLE_CAPTCHA_SITE_KEY": os.getenv("GOOGLE_CAPTCHA_SITE_KEY")})
    context.update(categories_tags_lists())
    return render(request, 'posts/contact.html', context)
