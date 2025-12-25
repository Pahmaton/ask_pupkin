from datetime import timedelta

from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.db.models import Count, Q
from django.utils import timezone

from app.models import Profile, Tag


# предполагается запуск по cron
# */15 * * * * /Users/pahmaton/development/ask_pupkin/venv/bin/python /Users/pahmaton/development/ask_pupkin/ask_pupkin/manage.py update_sidebar
class Command(BaseCommand):

    def handle(self, *args, **options):
        three_months_ago = timezone.now() - timedelta(days=90)
        popular_tags = Tag.objects.filter(
            questions__created_at__gte=three_months_ago
        ).annotate(
            q_count=Count('questions')
        ).order_by('-q_count')[:10]

        cache.set('popular_tags', list(popular_tags), 3600)

        last_week = timezone.now() - timedelta(days=7)
        best_members = Profile.objects.filter(
            Q(questions__created_at__gte=last_week) |
            Q(answers__created_at__gte=last_week)
        ).annotate(
            total_activity=Count('questions', distinct=True) + Count('answers', distinct=True)
        ).order_by('-total_activity')[:10]

        cache.set('best_members', list(best_members), 3600)
        self.stdout.write(self.style.SUCCESS('Successfully updated cache'))
