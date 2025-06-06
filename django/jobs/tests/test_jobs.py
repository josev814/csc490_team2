from io import StringIO
from unittest.mock import patch
from django.test import TestCase

from jobs.models import Jobs
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your tests here.
class JobTestCases(TestCase):
    job_names = [
        'ImportData', 'ExportData', 'Reindex', 'SyncUsers', 'Daily', 'Weekly'
    ]

    def tearDown(self):
        Jobs.objects.filter(name__in=self.job_names).delete()
        return super().tearDown()

    def test_create_job(self):
        job = Jobs.objects.create(name="ImportData")
        self.assertEqual(job.name, "ImportData")
        self.assertTrue(job.status)
        self.assertIsNotNone(job.create_date)
        self.assertIsNotNone(job.updated_date)
        self.assertIsNone(job.last_ran_timestamp)

        with self.assertRaises(ValidationError):
            job = Jobs(name='TestFail', status='string')
            job.full_clean()  # Trigger field  validation
            job.save()

    def test_set_last_runtime(self):
        job = Jobs.objects.create(name="ExportData")
        now = timezone.now()
        job.set_last_runtime(now)
        job.refresh_from_db()
        self.assertEqual(job.last_ran_timestamp, now)

    def test_get_job_info_creates_job(self):
        job_name = "SyncUsers"
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            job = Jobs().get_job_info(job_name)
            output = fake_stdout.getvalue()
        self.assertEqual(job.name, job_name)
        self.assertTrue(job.status)

        # Ensure "Added Job:" was printed
        self.assertIn(f"Added Job: {job_name}", output)

    def test_get_job_info_existing_job(self):
        job_name = 'Reindex'
        job = Jobs.objects.create(name=job_name)
        with patch('sys.stdout', new=StringIO()) as fake_stdout:  # capturing output
            fetched_job = Jobs().get_job_info(job_name)
            output = fake_stdout.getvalue()
        self.assertEqual(fetched_job.id, job.id)
        self.assertEqual(fetched_job.name, job_name)
        self.assertTrue(fetched_job.status)

        self.assertNotIn(f"Added Job: {job_name}", output)

    def test_search_by_name_and_status(self):
        Jobs.objects.create(name="Daily", status=True)

        # search only by name
        daily = Jobs.objects.search(job_name="Daily")
        self.assertEqual(daily.count(), 1)
        self.assertEqual(daily.first().name, "Daily")

        # search with name and numeric status
        daily = Jobs.objects.search(job_name="Daily", status=1)
        self.assertEqual(daily.count(), 1)
        self.assertTrue(daily.first().status)

        Jobs.objects.create(name="Weekly", status=False)
        # search with name and boolean status
        weekly = Jobs.objects.search(job_name="Weekly", status=False)
        self.assertEqual(weekly.count(), 1)
        self.assertFalse(weekly.first().status)

        # edge case: wrong status
        with self.assertRaises(ValidationError):
            Jobs.objects.filter(name='Weekly', status='inactive').get()
