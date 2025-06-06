"""
Jobs model that allows querying the database
"""
from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL # auth.User


class JobQuerySet(models.QuerySet):
    """
    Adding the option to do a search
    """
    def search(self, name=None, status=None):
        """A search method so we can filter jobs"""
        qs = self.filter(name=name)
        if status in (0, 1, True, False):
            qs = qs.filter(models.Q(status=status))
        return qs


class JobManager(models.Manager):
    """
    Overriding some of the default manager
    """
    def get_queryset(self):
        """
        returns a query set for the model
        """
        return JobQuerySet(self.model, using=self._db)

    def search(self, job_name=None, **kwargs):
        """
        Here we search the queryset based on the job name
        """
        return self.get_queryset().search(name=job_name, **kwargs)


class Jobs(models.Model):
    """
    model for the jobs
    """

    name = models.CharField(max_length=175)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    last_ran_timestamp = models.DateTimeField(blank=True, null=True)

    objects = JobManager()
    
    def set_last_runtime(self, last_runtime):
        """
        Pull the record with the rule id
        Update the object's last runtime
        Then save the record
        """
        self.last_ran_timestamp = last_runtime
        self.save()
    
    def get_job_info(self, job_name:str):
        """Gets the job information from the database

        :param job_name: name of the job to get
        :type job_name: str
        :return: _description_
        :rtype: _type_
        """
        job, created = Jobs.objects.get_or_create(
            name=job_name,
            defaults={'status': 1}
        )
        if created:
            print('Added Job:', job_name)
        return job
