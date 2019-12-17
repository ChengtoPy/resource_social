from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.srik.models import Posts, Comment, Buys, Img


class SourceView(View):
    """资源信息"""
    def get(self, request):
        sid = request.GET.get('n')
        source = Posts.objects.filter(id=sid)
        zy_comment = Comment.objects.filter(source_id=sid)
        buysource = Buys.objects.filter(source_id=sid)
        # source_img = Img.objects.filter(wpurl=source[0].source_bgurl)
        context = {
            'title': source[0].title,
            'content': source[0].content,
            'source_bgurl': source[0].source_bgurl,
            'source_psw': source[0].source_p3sw,
            'source_valuemarks': source[0].source_valuemarks,
            'click_nums': source[0].click_nums,
            'load_nums': source[0].load_nums,
            'source_price': source[0].source_price,
            'share_name': source[0].share_name,
            'source_id': source[0].id,
            'share_time': source[0].create_time,
            'zy_comment': zy_comment,
            'buysource': buysource,
        }
        print(zy_comment)
        return render(request, 'other/contentzy.html', context)

# Create your views here.
