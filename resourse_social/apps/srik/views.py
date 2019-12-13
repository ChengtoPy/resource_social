from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views import View

from apps.srik.models import Information, Posts


class IndexView(View):
    def get(self,request):
        # info = Information.objects.filter(receive_name=request.session['username'], read_sure=False)
        contact_list = Posts.objects.all().order_by("-create_time")
        paginator = Paginator(contact_list, 7)  # 每页显示25个数据

        page = request.GET.get('page', '1')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页面不是整数，则提交第一个页面
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页面超出范围，提交最后一个页面
            contacts = paginator.page(paginator.num_pages)

        return render(request, 'blackmain/index.html', {'contacts': contacts, 'paginator': paginator})

# Create your views here.
