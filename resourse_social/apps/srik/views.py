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


class GoodClass(View):
    """精品教程"""
    def get(self,request):
        contact_list = Posts.objects.all().order_by("-create_time")
        paginator = Paginator(contact_list, 12)  # Show 25 contacts per page

        page = request.GET.get('page', '1')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页面不是整数，则提交第一个页面
            contacts = paginator.page(1)
        except EmptyPage:
            #  如果页面超出范围，提交最后一个页面
            contacts = paginator.page(paginator.num_pages)
        list2 = []
        list3 = []
        if len(contacts)>=4 and len(contacts)<8:
            list1=[contacts[0],contacts[1],contacts[2],contacts[3]]
        elif len(contacts)>=8 and len(contacts)<12:
            list1 = [contacts[0], contacts[1], contacts[2], contacts[3]]
            list2 = [contacts[4], contacts[5], contacts[6], contacts[7]]
        elif len(contacts)>=12:
            list1 = [contacts[0], contacts[1], contacts[2], contacts[3]]
            list2 = [contacts[4], contacts[5], contacts[6], contacts[7]]
            list3 = [contacts[8], contacts[9], contacts[10], contacts[11]]
        else:
            list1 = [contacts[0], contacts[1], contacts[2], contacts[3]]
        print(len(list1))
        return render(request, 'blackmain/goodclass.html', {'contacts': contacts, 'paginator': paginator,'list1':list1,'list2':list2,'list3':list3})

# Create your views here.
