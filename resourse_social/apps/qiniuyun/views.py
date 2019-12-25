from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from qiniu import Auth


@require_http_methods(['GET'])
def get_token(request):
    # 1. 先要设置AccessKey和SecretKey
    access_key = "iAwVmChsyqh6RTqTgqNZTRu6rU8169wx81s_YVXC"
    secret_key = "iAwVmChsyqh6RTqTgqNZTRu6rU8169wx81s_YVXC"
    # 2. 授权
    q = Auth(access_key, secret_key)
    # 3. 设置七牛空间(自己刚刚创建的)
    bucket_name = 'srik_cheng'
    # 4. 生成token
    token = q.upload_token(bucket_name)
    # 5. 返回token,key必须为uptoken
    return JsonResponse({'uptoken': token})
# Create your views here.
