from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from apps.srik.models import Information, Posts, Answer, Comment, Img


class IndexView(View):
    def get(self, request):
        # info = Information.objects.filter(receive_name=request.session['username'], read_sure=False)
        contact_list = Posts.objects.all().order_by("-create_time")  # 排序
        paginator = Paginator(contact_list, 5)  # 每页显示25个数据
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

    def get(self, request):
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
        if len(contacts) >= 4 and len(contacts) < 8:
            list1 = [contacts[0], contacts[1], contacts[2], contacts[3]]
        elif len(contacts) >= 8 and len(contacts) < 12:
            list1 = [contacts[0], contacts[1], contacts[2], contacts[3]]
            list2 = [contacts[4], contacts[5], contacts[6], contacts[7]]
        elif len(contacts) >= 12:
            list1 = [contacts[0], contacts[1], contacts[2], contacts[3]]
            list2 = [contacts[4], contacts[5], contacts[6], contacts[7]]
            list3 = [contacts[8], contacts[9], contacts[10], contacts[11]]
        else:
            list1 = [contacts[0], contacts[1], contacts[2], contacts[3]]
        print(len(list1))
        return render(request, 'blackmain/goodclass.html',
                      {'contacts': contacts, 'paginator': paginator, 'list1': list1, 'list2': list2, 'list3': list3})


class EnjoyView(View):
    """分享资源"""

    def get(self, request):
        return render(request, 'blackmain/enjoy.html')

    def post(self, request):
        title = request.POST.get('title')  # 资源主题
        value = request.POST.get('sourcevalue')  # 资源值B币数
        img = request.POST.get('sourceimg')  # 资源图片
        types = request.POST.get('source_type')  # 资源类型
        source_url = request.POST.get('source_bgurl')  # 网盘链接
        psw = request.POST.get('source_psw')  # 网盘密码
        name = request.POST.get('share_name')  # 贡献者
        text = request.POST.get('sourcedsp')  # 资源说明
        try:
            posts = Posts.objects.create(title=title, source_valuemarks=value, source_picurl=img, source_type=types,
                                         source_bgurl=source_url, source_psw=psw, share_name=name, content=text)
            posts.save()
            new_img = Img(
                img=request.FILES.get('sourceimg'),
                wpurl=source_url
            )
            new_img.save()
        except Exception as a:
            print('a:{}'.format(a))  # 打印错误信息
        response = redirect(reverse('user:center'))  # 分享成功后的跳转
        return response


class BwView(View):
    """百度网盘教程资源"""

    def get(self, request):
        contact_list = Posts.objects.filter(source_type="百度网盘资源").order_by("-create_time")
        paginator = Paginator(contact_list, 5)  # Show 25 contacts per page

        page = request.GET.get('page', '1')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页面不是整数，则提交第一个页面
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页面超出范围，提交最后一个页面
            contacts = paginator.page(paginator.num_pages)

        return render(request, 'blackmain/bw.html', {'contacts': contacts, 'paginator': paginator})


class BcView(View):
    """编程源码资源"""

    def get(self, request):
        contact_list = Posts.objects.filter(source_type="编程源码资源").order_by("-create_time")
        paginator = Paginator(contact_list, 7)  # 每页显示的数据量

        page = request.GET.get('page', '1')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'blackmain/bcym.html', {'contacts': contacts, 'paginator': paginator})


class AnswerView(View):
    """有问必答"""

    def get(self, request):
        answer_list = Answer.objects.all().order_by("-question_time")
        print(answer_list)
        return render(request, 'blackmain/answer.html', {'answer': answer_list})


class GetView(View):
    """b币获取"""

    def get(self, request):
        zy_comment = Comment.objects.filter(source_id=111111)
        context = {
            'zy_comment': zy_comment,
        }
        print(zy_comment)
        return render(request, 'blackmain/getcoin.html', context)


# return JsonResponse({'res': "无此页面"})

class VipView(View):
    """vip模板"""

    def get(self, request):
        return render(request, 'blackmain/vip.html')


class CommentView(View):
    """资源评论"""
    def post(self, request):
        comment_sourcename = request.POST.get('comment_sourcename')
        source_id = request.POST.get('source_id')
        source_name = request.POST.get('source_name')
        comment_content = request.POST.get('comment_content')
        comment_name = request.POST.get('comment_name')
        info_tx = comment_name + "评论你的:" + comment_sourcename + " 资源" + comment_content
        try:
            passport = Comment(comment_sourcename=comment_sourcename, source_id=source_id,
                               comment_content=comment_content, comment_name=comment_name)
            passport.save()

            info = Information(info_content=info_tx, receive_name=comment_sourcename, send_name=comment_name)
            info.save()

        except Exception as e:
            print("e: ", e)  # 把异常打印出来
            return JsonResponse({'res': 1, 'errmsg': 'failed'})

        return JsonResponse({'res': 0, 'errmsg': 'success'})
        # return JsonResponse({'res': 1, 'errmsg': 'failed'})


class QuestionView(View):
    """用户提问"""
    def post(self,request):
        tw_name=request.POST.get("twname")
        twcontent=request.POST.get('twcontent')
        try:
            tw = Answer(question_name=tw_name, question_content=twcontent)
            tw.save()
        except Exception as e:
            print("e: ", e) # 把异常打印出来
            return JsonResponse({'res': 1, 'errmsg': '提交失败'})
        return JsonResponse({'res': 0, 'errmsg': '提交成功'})
    # return JsonResponse({'res': 4, 'errmsg': '请求错误'})
# Create your views here.
