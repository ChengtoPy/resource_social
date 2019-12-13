from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views import View

from apps.srik.models import Information, Posts


class IndexView(View):
    def get(self,request):
        # info = Information.objects.filter(receive_name=request.session['username'], read_sure=False)
        contact_list = Posts.objects.all().order_by("-create_time")
        paginator = Paginator(contact_list, 7)  # Show 25 contacts per page

        page = request.GET.get('page', '1')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)

        return render(request, 'blackmain/index.html', {'contacts': contacts, 'paginator': paginator})

# Create your views here.
