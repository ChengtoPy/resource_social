from pprint import pprint

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.srik.models import Posts, Comment, Buys, Img, Information
from apps.user.models import Users
from utils.message import Comment_Msg, Social_Msg


class SourceView(View):
    """资源信息"""

    def get(self, request):
        sid = request.GET.get('n')
        source = Posts.objects.filter(id=sid).first()
        zy_comment = Comment.objects.filter(source_id=sid)
        buysource = Buys.objects.filter(source_id=sid)
        comment_new = Comment_Msg()  # 显示最新评论
        socials = Social_Msg()  # 显示最新资源信息
        # source_img = Img.objects.filter(wpurl=source[0].source_bgurl)
        source.click_nums += 1  # 浏览量+1
        source.save()
        # print(source[0].click_nums)
        context = {
            'title': source.title,
            'content': source.content,
            'source_bgurl': source.source_bgurl,
            'source_psw': source.source_psw,
            'source_valuemarks': source.source_valuemarks,
            'click_nums': source.click_nums,
            'load_nums': source.load_nums,
            'source_price': source.source_price,
            'share_name': source.share_name,
            'source_id': source.id,
            'share_time': source.create_time,
            'zy_comment': zy_comment,
            'buysource': buysource,
            'comment_new': comment_new,
            'socials': socials
        }
        return render(request, 'other/contentzy.html', context)


def send(send_name, content, receive_name, source_id):
    # 发送消息
    try:
        buy = Information(send_name=send_name, receive_name=receive_name, info_content=content, source_id=source_id)
        buy.save()
    except Exception as e:
        print("e: ", e)


class BuyView(View):
    """购买资源"""

    def post(self, request):
        user_name = request.POST.get('user_name')
        source_id = request.POST.get('source_id')
        source_value = request.POST.get('source_value')
        source = Buys.objects.filter(source_id=source_id)
        for record in source:
            if record.user == user_name:
                return JsonResponse({'res': 1, 'errmsg': '您已购买此资源'})
            else:
                continue
        user = Users.objects.get(username=user_name)
        if int(user.user_allmarks) >= int(source_value):
            user_allmarks = int(user.user_allmarks) - int(source_value)
            user.user_allmarks = user_allmarks
            user.save()
        else:
            return JsonResponse({'res': 2, 'errmsg': '积分不足'})
        try:
            buy = Buys(source_id=source_id, user=user_name, source_value=source_value)
            buy.save()
        except Exception as e:
            print("e: ", e)
            return JsonResponse({'res': 3, 'errmsg': '购买失败'})

        posts = Posts.objects.get(id=source_id)
        posts.load_nums+= 1
        posts.save()
        source = Posts.objects.filter(id=source_id)
        send_name = "系统消息"
        content = "你已兑换资源" + str(source[0].title) + "网盘/开源网址" + str(source[0].source_bgurl) + " 网盘密码：" + str(
            source[0].source_psw)
        send(send_name, content, request.session['username'], source_id)
        return JsonResponse({'res': 0, 'bgurl': source[0].source_bgurl, 'psw': source[0].source_psw})
        # return JsonResponse({'res': "无此页面"})


class SeacherView(View):
    """搜索"""

    def get(self, request):
        skey = request.GET.get('seacherkey')
        if not skey:
            error_msg = '请输入关键词'
            return render(request, 'other/seacher.html', {'error_msg': error_msg})
        else:
            contact_list = Posts.objects.filter(title__icontains=skey).order_by("-create_time")
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

            return render(request, 'other/seacher.html',
                          {'contacts': contacts, 'paginator': paginator, 'num': len(contact_list), 'key': skey})
            # return JsonResponse({'res': "无此页面"})


class ImgView(View):
    """图片配置cdn"""

    def get(self):
        pass
# Create your views here.
