from django.shortcuts import render, redirect
from learning_logs.forms import TopicForm
from learning_logs.models import Topic


# Create your views here.
def index(request):
    return render(request, 'learning_logs/index.html')


def contents(request):
    return render(request, 'learning_logs/contents.html')


def about(request):
    return render(request, 'learning_logs/about.html')


def contact(request):
    return render(request, 'learning_logs/contact.html')


def topics(request):
    """显示所有主题"""
    topics = Topic.objects.order_by()
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    # topic_id从url的topics/<int:topic_id>中获取
    """显示单个主题及其所有条目"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    if request.method != 'POST':
        # 显示一个空的表单给用户
        form = TopicForm()
    else:
        # 处理提交的表单数据
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
