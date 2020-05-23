from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import VideoContent, VideoTagList, VideoTagName

def index(request, page=0):
    max_page = VideoContent.objects.count() // 10
    return construct_page(request, VideoTagList.objects.values('content_id'), VideoContent.objects.order_by('-upload_date')[page*10:(page+1)*10].values(), page, max_page, 'video:index')

from django.db.models import Count

def construct_page(request, all_content_ids, page_contents, current_page, max_page, url_type, url_word=''):
    # page_contents(動画)に関連するタグを抜き出し、テンプレートで使えるよう整形
    contents = []
    for item in page_contents:
        tmp_dict = item
        tmp_dict.update({'tags': VideoTagList.objects.filter(content_id=item['id']).select_related('tag')})
        contents.append(tmp_dict)

    # all_content_idsからタグを多い順で集計し、整形する
    tag_cnt = VideoTagList.objects.filter(content__in = all_content_ids).values('tag').annotate(tag_count=Count('tag')).order_by('-tag_count')[:10]
    tag_names = [VideoTagName.objects.filter(id = item.get('tag'))[0] for item in tag_cnt]
    tags = [{'name': tag_names[i].name, 'count': tag_cnt[i]["tag_count"]} for i in range(len(tag_names))]

    # ページが有効な範囲をvalidでマークを付ける
    page_list = [{'num':x, 'valid':0 <= x and x <= max_page} for x in range(current_page-5, current_page+4)]

    return render(request, 'video/index.html', {'tags': tags, 'contents': contents, 'page':{'type':url_type, 'word': url_word, 'current': current_page, 'max': max_page, 'list': page_list}})
