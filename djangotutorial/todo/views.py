from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Case, When, Value, IntegerField
from .models import TodoItem
from .forms import TodoForm


def todo_list(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm()

    # Get filter from query params
    filter_type = request.GET.get('filter', 'all')
    priority_filter = request.GET.get('priority', 'all')

    todos = TodoItem.objects.annotate(
        priority_rank=Case(
            When(priority='high', then=Value(3)),
            When(priority='medium', then=Value(2)),
            When(priority='low', then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by('completed', '-priority_rank', '-created_at')

    # Apply completion filter
    if filter_type == 'active':
        todos = todos.filter(completed=False)
    elif filter_type == 'completed':
        todos = todos.filter(completed=True)

    # Apply priority filter
    if priority_filter != 'all':
        todos = todos.filter(priority=priority_filter)

    all_todos = TodoItem.objects.all()
    total = all_todos.count()
    completed = all_todos.filter(completed=True).count()
    pending = total - completed
    progress = int((completed / total) * 100) if total > 0 else 0

    context = {
        'form': form,
        'todos': todos,
        'total': total,
        'completed': completed,
        'pending': pending,
        'progress': progress,
        'filter_type': filter_type,
        'priority_filter': priority_filter,
    }
    return render(request, 'todo/todo_list.html', context)


def toggle_todo(request, todo_id):
    todo = get_object_or_404(TodoItem, id=todo_id)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')


def delete_todo(request, todo_id):
    todo = get_object_or_404(TodoItem, id=todo_id)
    todo.delete()
    return redirect('todo_list')


def clear_completed(request):
    TodoItem.objects.filter(completed=True).delete()
    return redirect('todo_list')
