from django.shortcuts import render, redirect, get_object_or_404
from .models import discussion, category
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def home(request):
    categories = category.objects.all()

    # POST ma'lumotlar
    discuss = request.POST.get('discuss')
    content = request.POST.get('content')
    category_id = request.POST.get('category')
    name = request.POST.get('name')
    image = request.FILES.get('image')

    # GET filter parametrlari (default: 'recent')
    filter_type = request.GET.get('filter', 'recent')
    extra_filter = request.GET.get('extra_filter', '').lower()
    search_query = request.GET.get('search', '').strip()

    # Asosiy queryset
    discussions = discussion.objects.select_related('category', 'author')

    # Agar qidiruv bo‘lsa
    if search_query:
        discussions = discussions.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query) |
            Q(author2__icontains=search_query)
        )

    # Filterlash
    if filter_type == 'most_discussed':
        discussions = discussions.annotate(num_comments=Count('comments')).order_by('-num_comments', '-created_at')
    elif filter_type == 'most_votes':
        discussions = discussions.order_by('-vote_count', '-created_at')
    else:  # default: recent
        discussions = discussions.order_by('-created_at')

    # Faqat user o‘z postlari
    if extra_filter == 'my_ideas' and request.user.is_authenticated:
        discussions = discussions.filter(author=request.user)
    elif extra_filter == 'my_ideas':
        discussions = discussions.none()

    # POST orqali yangi discussion yaratish
    if request.method == 'POST' and discuss:
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
        return redirect(f"{request.path}?filter={filter_type}")

    discussions = discussions.prefetch_related('comments')

    paginator = Paginator(discussions, 7)
    page_number = request.GET.get('page')
    discussions_page = paginator.get_page(page_number)

    # Kim ovoz berganini tekshirish
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
        'search_query': search_query,
    }
    return render(request, 'index.html', context)

def category_filter(request, slug):
    categories = category.objects.all()
    current_category = get_object_or_404(category, slug=slug)
    search_query = request.GET.get('search', '').strip()
    filter_type = request.GET.get('filter', 'recent')
    extra_filter = request.GET.get('extra_filter', '').lower()

    discussions = discussion.objects.filter(category=current_category).select_related('category', 'author')

    if search_query:
        discussions = discussions.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query) |
            Q(author2__icontains=search_query)
        )

    if filter_type == 'most_discussed':
        discussions = discussions.annotate(num_comments=Count('comments')).order_by('-num_comments', '-created_at')
    elif filter_type == 'most_votes':
        discussions = discussions.order_by('-vote_count', '-created_at')
    else:
        discussions = discussions.order_by('-created_at')

    if extra_filter == 'my_ideas' and request.user.is_authenticated:
        discussions = discussions.filter(author=request.user)
    elif extra_filter == 'my_ideas':
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
        'current_filter_display': current_filter_display,
        'search_query': search_query,
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
    # return redirect("main:home")


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


@login_required
def roadmap(request):
    filter_type = request.GET.get('filter', 'recent').lower()
    extra_filter = request.GET.get('extra_filter', '').lower()

    # Avval userga tegishli barcha discussionlarni olamiz
    user_discussions = discussion.objects.filter(author=request.user).select_related('category')

    # Filterlash
    if filter_type == 'most_discussed':
        user_discussions = user_discussions.annotate(num_comments=Count('comments')).order_by('-num_comments', '-created_at')
    elif filter_type == 'most_votes':
        user_discussions = user_discussions.order_by('-vote_count', '-created_at')
    else:  # default: recent
        user_discussions = user_discussions.order_by('-created_at')

    # Kategoriyalarni olish
    categories = category.objects.all()

    # Har bir kategoriya bo'yicha discussionlarni filterlab dictga joylash
    category_discussions = {}
    for cat in categories:
        category_discussions[cat] = user_discussions.filter(category=cat)

    # Voted set tayyorlash
    voted_set = set()
    for d in user_discussions:
        if request.user.is_authenticated:
            key = f'voted_{request.user.id}_{d.id}'
        else:
            if not request.session.session_key:
                request.session.create()
            key = f'voted_{request.session.session_key}_{d.id}'
        if request.session.get(key):
            voted_set.add(d.id)

    context = {
        'category_discussions': category_discussions,
        'voted_set': voted_set,
        'filter_type': filter_type,  # agar frontenda kerak bo'lsa
    }
    return render(request, 'roadmap.html', context)