from apps.srik.models import Comment


def Comment_Msg():
    comment = Comment.objects.all().order_by('-comment_time')[0:7]
    return comment
