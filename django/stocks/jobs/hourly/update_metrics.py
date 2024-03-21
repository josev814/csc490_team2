"""
Run a job to import metrics hourly
"""

from django_extensions.management.jobs import HourlyJob

class Job(HourlyJob):
    help = "Hourly job to pull metrics"

    def execute(self):
        from django.core import management
        management.call_command('update_metrics')
