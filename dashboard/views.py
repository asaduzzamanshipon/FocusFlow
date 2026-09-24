from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from datetime import timedelta

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Task, Routine, PomodoroSession, Notification


@login_required
def home(request):

    user = request.user
    today = timezone.localdate()

    todays_tasks = Task.objects.filter(
        user=user,
        due_date=today
    )

    completed_tasks = todays_tasks.filter(
        completed=True
    ).count()

    total_tasks = todays_tasks.count()

    remaining_tasks = todays_tasks.filter(
        completed=False
    ).count()

    if total_tasks > 0:
        task_progress = round(
            (completed_tasks / total_tasks) * 100
        )
    else:
        task_progress = 0

    todays_routine = Routine.objects.filter(
        user=user,
        day__in=[
            "Everyday",
            today.strftime("%A")
        ]
    )

    context = {
        "todays_tasks": todays_tasks,
        "todays_routine": todays_routine,
        "completed_tasks": completed_tasks,
        "total_tasks": total_tasks,
        "remaining_tasks": remaining_tasks,
        "task_progress": task_progress,
    }

    return render(
        request,
        "dashboard/home.html",
        context
    )


@login_required
def tasks(request):

    today = timezone.localdate()

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        due_time = request.POST.get("due_time") or None

        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                description=description,
                due_date=today,
                due_time=due_time,
            )

        return redirect("tasks")

    todays_tasks = Task.objects.filter(
        user=request.user,
        due_date=today
    )

    return render(
        request,
        "dashboard/tasks.html",
        {
            "todays_tasks": todays_tasks,
            "today": today,
        }
    )


@login_required
def complete_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    task.completed = not task.completed
    task.save()

    return redirect("tasks")


@login_required
def delete_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    task.delete()

    return redirect("tasks")


@login_required
def routine(request):

    today = timezone.localdate()
    today_name = today.strftime("%A")

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        subject = request.POST.get("subject", "").strip()
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time") or None
        day = request.POST.get("day", "Everyday")

        if title and start_time:
            Routine.objects.create(
                user=request.user,
                title=title,
                subject=subject,
                start_time=start_time,
                end_time=end_time,
                day=day,
            )

        return redirect("routine")

    todays_routine = Routine.objects.filter(
        user=request.user,
        day__in=["Everyday", today_name]
    )

    all_routines = Routine.objects.filter(
        user=request.user
    )

    context = {
        "todays_routine": todays_routine,
        "all_routines": all_routines,
        "today": today,
        "today_name": today_name,
    }

    return render(
        request,
        "dashboard/routine.html",
        context
    )

@login_required
def delete_routine(request, routine_id):

    routine = get_object_or_404(
        Routine,
        id=routine_id,
        user=request.user
    )

    routine.delete()

    return redirect("routine")

@login_required
def pomodoro(request):
    return render(
        request,
        "dashboard/pomodoro.html"
    )


@login_required
@require_POST
def complete_pomodoro(request):

    session_type = request.POST.get("session_type", "focus")
    duration = request.POST.get("duration", "25")

    if session_type not in ["focus", "break"]:
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid session type."
            },
            status=400
        )

    try:
        duration = int(duration)
    except (TypeError, ValueError):
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid duration."
            },
            status=400
        )

    PomodoroSession.objects.create(
        user=request.user,
        session_type=session_type,
        duration_minutes=duration
    )

    Notification.objects.create(
        user=request.user,
        notification_type="pomodoro",
        title="Pomodoro Completed",
        message=f"{session_type.capitalize()} session completed for {duration} minutes."
    )

    return JsonResponse({
        "success": True,
        "message": "Pomodoro session saved."
    })


@login_required
def progress(request):

    user = request.user
    today = timezone.localdate()

    # -----------------------------
    # Today's tasks
    # -----------------------------

    todays_tasks = Task.objects.filter(
        user=user,
        due_date=today
    )

    total_tasks = todays_tasks.count()

    completed_tasks = todays_tasks.filter(
        completed=True
    ).count()

    remaining_tasks = total_tasks - completed_tasks

    if total_tasks > 0:
        today_progress = round(
            (completed_tasks / total_tasks) * 100
        )
    else:
        today_progress = 0


    # -----------------------------
    # Weekly progress
    # -----------------------------

    week_start = today - timedelta(
        days=today.weekday()
    )

    weekly_data = []

    for i in range(7):

        current_day = week_start + timedelta(days=i)

        day_tasks = Task.objects.filter(
            user=user,
            due_date=current_day
        )

        total = day_tasks.count()

        completed = day_tasks.filter(
            completed=True
        ).count()

        if total > 0:
            percentage = round(
                (completed / total) * 100
            )
        else:
            percentage = 0

        weekly_data.append({
            "date": current_day,
            "day": current_day.strftime("%a"),
            "total": total,
            "completed": completed,
            "percentage": percentage,
        })


    # -----------------------------
    # Routine statistics
    # -----------------------------

    total_routines = Routine.objects.filter(
        user=user
    ).count()


    context = {
        "today": today,

        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "remaining_tasks": remaining_tasks,
        "today_progress": today_progress,

        "weekly_data": weekly_data,

        "total_routines": total_routines,
    }

    return render(
        request,
        "dashboard/progress.html",
        context
    )


@login_required
def notifications(request):

    user = request.user
    today = timezone.localdate()
    now = timezone.localtime().time()

    # -----------------------------
    # Today's tasks
    # -----------------------------

    todays_tasks = Task.objects.filter(
        user=user,
        due_date=today
    ).order_by("due_time", "created_at")


    # -----------------------------
    # Overdue tasks
    # -----------------------------

    overdue_tasks = Task.objects.filter(
        user=user,
        due_date__lt=today,
        completed=False
    ).order_by("-due_date", "due_time")


    # -----------------------------
    # Today's routines
    # -----------------------------

    today_name = today.strftime("%A")

    todays_routines = Routine.objects.filter(
        user=user,
        day__in=["Everyday", today_name]
    ).order_by("start_time")


    # -----------------------------
    # Upcoming tasks
    # -----------------------------

    upcoming_tasks = Task.objects.filter(
        user=user,
        due_date__gt=today,
        completed=False
    ).order_by("due_date", "due_time")[:10]


    # -----------------------------
    # Counts
    # -----------------------------

    completed_today = todays_tasks.filter(
        completed=True
    ).count()

    pending_today = todays_tasks.filter(
        completed=False
    ).count()


    context = {
        "todays_tasks": todays_tasks,
        "overdue_tasks": overdue_tasks,
        "todays_routines": todays_routines,
        "upcoming_tasks": upcoming_tasks,

        "completed_today": completed_today,
        "pending_today": pending_today,

        "today": today,
        "now": now,
    }

    return render(
        request,
        "dashboard/notifications.html",
        context
    )