from apps.srik.models import Comment, Posts


def Comment_Msg():
    """查询最新评论信息"""
    comment = Comment.objects.all().order_by('-comment_time')[0:7]
    return comment


def Social_Msg():
    """查询最新资源信息"""
    socials = Posts.objects.all().order_by('-create_time')[0:5]
    return socials