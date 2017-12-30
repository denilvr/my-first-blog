from django.shortcuts import render
from .forms import PostForm, CommentsForm
from .models import Post, Comments
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.dispatch import receiver
from django.contrib.auth import login, authenticate
from .forms import SignUpForm


def post_list(request):
	posts = Post.objects.filter(published_date__isnull=False).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request,pk):
	if Post.objects.filter(pk=pk):
		post = Post.objects.filter(pk=pk)
		comm = Comments.objects.filter(post=post)
		form = CommentsForm()
		return render(request, 'blog/post_detail.html', {'post': post[0],'comm':comm,'form':form})
	else:
		return render(request, 'blog/error.html')

@login_required
def post_new(request):

	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.created_date = timezone.now()
			post.save()
			messages.success(request, 'Draft created successfully!')
			return redirect('post_list')
	else:
		form = PostForm()
	return render(request, 'blog/post_new.html', {'form': form})

@login_required
def post_edit(request, pk):
	post = Post.objects.filter(pk=pk)[0]
	if post.author == request.user:
		if request.method == "POST":
			form = PostForm(request.POST, instance=post)
			if form.is_valid():
				post = form.save(commit=False)
				post.author = request.user
				post.created_date = timezone.now()
				post.save()
				messages.success(request, 'Blog edited successfully!')
				return redirect('post_detail', pk=post.pk)
		else:
			form = PostForm(instance=post)
		return render(request, 'blog/post_new.html', {'form': form})
	else:
		return render(request, 'blog/error.html')

@login_required
def post_remove(request, pk):
	post = Post.objects.filter(pk=pk)[0]
	comm = Comments.objects.filter(post=post)
	if post.author == request.user:
		comm.delete()
		post.delete()
		messages.success(request, 'Blog Removed!')
		return redirect('post_list')
		
	else:
		return render(request, 'blog/error.html')

@login_required
def post_drafts(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('published_date')
	return render(request, 'blog/post_drafts.html', {'posts': posts})

@login_required
def post_publish(request, pk):
	post = Post.objects.filter(pk=pk)[0]
	post.publish();
	messages.success(request, 'Draft published successfully!')
	return redirect('post_drafts')



@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
	messages.success(request, 'Logged out successfully!')

@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
	messages.success(request, 'Logged in successfully!')


def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/')
	else:
		form = SignUpForm()
	return render(request, 'blog/signup.html', {'form': form})

def add_comment(request,pk):
	post = Post.objects.filter(pk=pk)[0]
	# print(request.POST['text'])
	# comm = Comments(request.user.id,post,request.POST['text'])
	# comm.save()
	form = CommentsForm(request.POST)
	print(form)
	print(form.is_valid())
	if form.is_valid():
		comm = form.save(commit=False)
		comm.author = request.user
		comm.post = post		
		comm.save() 		       
	return redirect('post_detail',pk=pk)
	
def edit_comment(request,pk,ck):
	comm = Comments.objects.filter(pk=ck)[0]
	post = Post.objects.filter(pk=pk)[0]
	form = CommentsForm(request.POST, instance=comm)
	if form.is_valid():		
		comm.save()
	return redirect('post_detail', pk=post.pk)
	
def remove_comment(request,pk,ck):
	Comments.objects.filter(pk=ck)[0].delete()
	next = request.POST.get('next', '/')
	return redirect(next)