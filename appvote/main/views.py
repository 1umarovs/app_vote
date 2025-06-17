from django.shortcuts import render
from .models import category, discussion
from django.core.paginator import Paginator



# Create your views here.
def home(request):
    discuss = request.POST.get('discuss')
    content = request.POST.get('content')
    category_id = request.POST.get('category')
    name = request.POST.get('name')
    image = request.FILES.get('image')
    categories = category.objects.all()
    discussions = discussion.objects.all()
    paginator = Paginator(discussions, 10)  # 10 discussions per page
    page_number = request.GET.get('page')
    discussions = paginator.get_page(page_number)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            discussion.objects.create(
                title=discuss,
                content=content,
                category_id=category_id,
                author2=name,
                image=image
            )
        else:
             discussion.objects.create(
                title=discuss,
                content=content,
                category_id=category_id,
                author=request.user,
                img=image
            )
    context = {
        'categories': categories,
        'discussions': discussions
    }
    return render(request, 'index.html', context)