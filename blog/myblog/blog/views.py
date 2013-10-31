# _*_ coding: utf-8 _*_
import md5
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User, UserManager
from blog.models import Entries, Categories, TagModel, Comments
from django.template import Context, loader
from django.core.context_processors import csrf
from django.shortcuts import render_to_response


def main_page(request):
	page_title = '메인 화면'

	user = request.user

	ctx = Context({
		'page_title':page_title,
		'user':user
		})
	ctx.update(csrf(request))

	return render_to_response('main.html', ctx)


def profile(request):
	page_title = '프로필 화면'

	user = request.user

	ctx = Context({
		'page_title':page_title,
		'user':user
		})
	ctx.update(csrf(request))

	return render_to_response('profile.html', ctx)


def index(request, page=1):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/?next=%s' % request.path)

	per_page = 5
	start_pos = (int(page)-1) * per_page
	end_pos = start_pos + per_page
	
	page_title = '블로그 글 목록 화면'
	
	entries = Entries.objects.all().order_by('-created')[start_pos:end_pos]
	
	tpl = loader.get_template('list.html')

	ctx = Context({
		'page_title':page_title,
		'entries':entries,
		'current_entry':page
		})

	return HttpResponse(tpl.render(ctx))


def read(request, entry_id=None):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/?next=%s' % request.path)

	page_title = '블로그 글 읽기 화면'

	user = request.user

	try:
		current_entry = Entries.objects.get(id=int(entry_id))
	except:
		return HttpResponse('없는 글입니다.')

	try:
		prev_entry = current_entry.get_previous_by_created()
	except:
		prev_entry = None

	try:
		next_entry = current_entry.get_next_by_created()
	except:
		next_entry = None

	try:
		comments = Comments.objects.filter(Entry=current_entry).order_by('created')
	except:
		comments = None

	ctx = Context({
		'page_title':page_title,
		'user':user,
		'current_entry':current_entry,
		'comments':comments,
		'prev_entry':prev_entry,
		'next_entry':next_entry
		})
	ctx.update(csrf(request))

	return render_to_response('read.html', ctx)


def write_form(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/?next=%s' % request.path)

	page_title = '블로그 글 쓰기 화면'

	user = request.user

	categories = Categories.objects.all()

	ctx = Context({
		'page_title':page_title,
		'user':user,
		'categories':categories
		})
	ctx.update(csrf(request))

	return render_to_response('write.html', ctx)


def add_post(request):
	entry_id = Entries

	if request.POST.has_key('name') == False:
		return HttpResponse('작성자가 없습니다.')
	else:
		if len(request.POST['name']) == 0:
			return HttpResponse('빈 작성자입니다.')
		else:
			entry_writer = request.POST['name']

	if request.POST.has_key('title') == False:
		return HttpResponse('글 제목이 없습니다.')
	else:
		if len(request.POST['title']) == 0:
			return HttpResponse('빈 제목입니다.')
		else:
			entry_title = request.POST['title']

	if request.POST.has_key('content') == False:
		return HttpResponse('글 내용이 없습니다.')
	else:
		if len(request.POST['content']) == 0:
			return HttpResponse('글 내용이 비어있습니다.')
		else:
			entry_content = request.POST['content']

	try:
		entry_category = Categories.objects.get(id=request.POST['category'])
	except:
		return HttpResponse('올바르지 않은 카테고리입니다.')

	if request.POST.has_key('tags') == True:
		tags = map(lambda str: str.strip(), unicode(request.POST['tags']).split(','))
		tag_list = map(lambda tag: TagModel.objects.get_or_create(Title=tag)[0], tags)
	else:
		tag_list = []

	new_entry = Entries(Name=entry_writer, Title=entry_title, Content=entry_content, Category=entry_category)

	try:
		new_entry.save()
	except:
		return HttpResponse('오류')

	for tag in tag_list:
		new_entry.Tags.add(tag)

	if len(tag_list) > 0:
		try:
			new_entry.save()
		except:
			return HttpResponse('오류')

	return HttpResponse('%s번 글을 성공적으로 작성했습니다.' % new_entry.id)


def add_comment(request):
	cmt_name = request.POST.get('name', '')
	if not cmt_name.strip():
		return HttpResponse('작성자 이름이 올바르지 않습니다.')

	cmt_content = request.POST.get('content', '')
	if not cmt_content.strip():
		return HttpResponse('댓글 내용을 입력하세요.')

	if request.POST.has_key('entry_id') == False:
		return HttpResponse('댓글 달 글이 지정되어있지 않습니다.')
	else:
		try:
			entry = Entries.objects.get(id=request.POST['entry_id'])
		except:
			return HttpResponse('없는 글입니다.')
	
	new_cmt = Comments(Name=cmt_name, Content=cmt_content, Entry=entry)
		
	try:
		new_cmt.save()
	except:
		return HttpResponse('제대로 저장하지 못했습니다.')

	entry.Comments += 1
	entry.save()

	return HttpResponse('%s번 글에 댓글을 달았습니다.' % entry.id)


def join_form(request):
	page_title = '회원가입 화면'

	ctx = Context({
		'page_title':page_title,
		})
	ctx.update(csrf(request))

	return render_to_response('join.html', ctx)


def add_user(request):
	usr_username = request.POST['username']
	if not usr_username.strip():
		return HttpResponse('아이디를 입력하세요!')

	usr_password = request.POST['password']
	if not usr_password.strip():
		return HttpResponse('비밀번호를 입력하세요!')

	user = User.objects.create_user(usr_username, None, usr_password)
	user.is_staff = False
	user.save()

	return HttpResponse('회원가입이 완료되었습니다.')


def logout_page(request):
	logout(request)

	return HttpResponseRedirect('/')
