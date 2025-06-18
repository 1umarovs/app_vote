from django.shortcuts import render, redirect, get_object_or_404
from .models import discussion, category
from django.core.paginator import Paginator
from django.db.models import Count

def home(request):
    categories = category.objects.all()
    discuss = request.POST.get('discuss')
    content = request.POST.get('content')
    category_id = request.POST.get('category')
    name = request.POST.get('name')
    image = request.FILES.get('image')


        # POST orqali yangi discussion yaratish


    filter_type = request.GET.get('filter', 'most_discussed')  # default filter
    extra_filter = request.GET.get('extra_filter', '')  # my_ideas uchun

    discussions = discussion.objects.select_related('category', 'author')

    # Filter bo'yicha tartiblash:
    if filter_type == 'most_discussed':
        discussions = discussions.annotate(num_comments=Count('comments')).order_by('-num_comments', '-created_at')
    elif filter_type == 'most_votes':
        discussions = discussions.order_by('-vote_count', '-created_at')
    elif filter_type == 'recent':
        discussions = discussions.order_by('-created_at')
    else:
        discussions = discussions.order_by('-created_at')

    # Agar user auth bo'lsa va my_ideas filter tanlangan bo'lsa
    if extra_filter == 'my_ideas' and request.user.is_authenticated:
        discussions = discussions.filter(author=request.user)
    elif extra_filter == 'my_ideas' and not request.user.is_authenticated:
        # Agar user auth bo'lmasa, bo'sh queryset qaytaramiz
        discussions = discussions.none()

    discussions = discussions.prefetch_related('comments')
    if request.method == 'POST' and 'discuss' in request.POST:
        if not request.user.is_authenticated:
            discussion.objects.create(
                title=discuss,
                content=content,
                category_id=category_id,
                author2=name,
                img=image
            )
        else:
            discussion.objects.create(
                title=discuss,
                content=content,
                category_id=category_id,
                author=request.user,
                img=image
            )
        # POST so‘ng sahifani filter bilan qayta yuklash uchun redirect qilsak yaxshi
        return redirect(f"{request.path}?filter={filter_type}")

    paginator = Paginator(discussions, 7)
    page_number = request.GET.get('page')
    discussions_page = paginator.get_page(page_number)

    voted_set = set()
    for d in discussions_page:
        if request.user.is_authenticated:
            key = f'voted_{request.user.id}_{d.id}'
        else:
            if not request.session.session_key:
                request.session.create()
            key = f'voted_{request.session.session_key}_{d.id}'
        if request.session.get(key):
            voted_set.add(d.id)

    context = {
        'categories': categories,
        'discussions': discussions_page,
        'voted_set': voted_set,
        'current_filter': filter_type,
        'extra_filter': extra_filter,
    }
    return render(request, 'index.html', context)


def category_filter(request, slug):
    categories = category.objects.all()
    current_category = get_object_or_404(category, slug=slug)

    filter_type = request.GET.get('filter', 'recent')
    extra_filter = request.GET.get('extra_filter', '').lower()  # my_ideas uchun

    discussions = discussion.objects.filter(category=current_category).select_related('category', 'author')

    if filter_type == 'most_discussed':
        discussions = discussions.annotate(num_comments=Count('comments')).order_by('-num_comments', '-created_at')
    elif filter_type == 'most_votes':
        discussions = discussions.order_by('-vote_count', '-created_at')
    elif filter_type == 'recent':
        discussions = discussions.order_by('-created_at')
    else:
        discussions = discussions.order_by('-created_at')

    if extra_filter == 'my_ideas' and request.user.is_authenticated:
        discussions = discussions.filter(author=request.user)
    elif extra_filter == 'my_ideas' and not request.user.is_authenticated:
        discussions = discussions.none()

    discussions = discussions.prefetch_related('comments')

    paginator = Paginator(discussions, 7)
    page_number = request.GET.get('page')
    discussions_page = paginator.get_page(page_number)

    voted_set = set()
    for d in discussions_page:
        if request.user.is_authenticated:
            key = f'voted_{request.user.id}_{d.id}'
        else:
            if not request.session.session_key:
                request.session.create()
            key = f'voted_{request.session.session_key}_{d.id}'
        if request.session.get(key):
            voted_set.add(d.id)

        filter_names = {
            'most_discussed': 'Most Discussed',
            'most_votes': 'Most Votes',
            'recent': 'Recent',
        }

    current_filter_display = filter_names.get(filter_type, 'Recent')

    context = {
        'categories': categories,
        'current_category': current_category,
        'discussions': discussions_page,
        'voted_set': voted_set,
        'current_filter': filter_type,
        'extra_filter': extra_filter,
        'current_filter_display': current_filter_display
    }
    return render(request, 'index.html', context)


def toggle_vote(request, discussion_id):
    discussion_obj = get_object_or_404(discussion, id=discussion_id)

    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    if request.user.is_authenticated:
        vote_key = f'voted_{request.user.id}_{discussion_id}'
    else:
        vote_key = f'voted_{session_key}_{discussion_id}'

    voted = request.session.get(vote_key, False)

    if voted:
        discussion_obj.vote_count -= 1
        request.session[vote_key] = False
    else:
        discussion_obj.vote_count += 1
        request.session[vote_key] = True

    discussion_obj.save()
    return redirect(request.META.get('HTTP_REFERER'))


def discussion_detail(request, discussion_id):
    # ✅ Optimallashtirilgan discussion obyekt chaqiruvi
    discussion_obj = discussion.objects.select_related('category', 'author') \
                                       .prefetch_related('comments').get(id=discussion_id)

    content = request.POST.get('content')
    name = request.POST.get('name')

    # Fikr (comment) qo‘shish
    if request.method == 'POST' and content:
        if not request.user.is_authenticated:
            discussion_obj.comments.create(content=content, author2=name)
        else:
            discussion_obj.comments.create(content=content, author=request.user)

    categories = category.objects.all()

    # ✅ Vote holatini tekshirish
    voted_set = set()
    if request.user.is_authenticated:
        key = f'voted_{request.user.id}_{discussion_obj.id}'
    else:
        key = f'voted_{request.session.session_key}_{discussion_obj.id}'

    if request.session.get(key):
        voted_set.add(discussion_obj.id)

    context = {
        'discussion': discussion_obj,
        'categories': categories,
        'voted_set': voted_set,
        'comments': discussion_obj.comments.all(),
        'comment_count': discussion_obj.discussions_comments_count(),
    }
    return render(request, 'discussion_detail.html', context)

