"""
Command to update the Growth and Profit for a user
"""
from django.core.management.base import BaseCommand
from django.db.models import Sum

from rules.models import Rules
from users.models import Users


class Command(BaseCommand):
    """
    Update the Growth and Profit for a user
    """
    help = "Update the Growth and Profit for a user"

    def add_arguments(self, parser):
        parser.add_argument(
            '--user_id',
            type=int,
            help='The user id to update profit growth for'
        )

    def handle(self, *args, **options):
        """
        The main control of the command
        """
        if 'user_id' in options and options['user_id'] is not None:
            self.output_info(f"Updating Profit for {options['user_id']}")
            user = self.get_user_record(options['user_id'])
            pg = self.get_total_rules_profit_growth(user)
            self.update_profit_growth(user, pg)
        else:
            self.output_info('Updating Profit for ALL Users')
    
    def get_user_record(self, user_id:int) -> Users:
        """
        Get a user record from the db based on the user id

        :param user_id: The id of the user
        :type user_id: int
        :return: Returns the user object
        :rtype: Users
        """
        return Users.objects.filter(pk__exact=int(user_id)).get()
    
    def get_total_rules_profit_growth(self, user:Users) -> dict:
        """
        Gets the total profit and growth of all rules for a user
        """
        profit_growth = Rules.objects.filter(
            user_id=user.pk
        ).aggregate(
            total_profit=Sum('profit') or 0,
            total_growth=Sum('growth') or 0
        )
        return {
            'profit': profit_growth['total_profit'],
            'growth': profit_growth['total_growth']
        }

    def update_profit_growth(self, user:Users, profit_growth:dict):
        """
        Updates the user record's profit and growth
        """
        for key,val in profit_growth.items():
            setattr(user, key, val)
        user.save()
    
    def output_error(self, error_msg) -> None:
        """Outputs an error message

        :param error_msg: the error message to output
        :type error_msg: str
        """
        self.stdout.write(
            self.style.ERROR(
                error_msg
            )
        )
    
    def output_success(self, success_msg) -> None:
        """Outputs a success message

        :param success_msg: the message to output
        :type success_msg: str
        """
        self.stdout.write(
            self.style.SUCCESS(
                success_msg
            )
        )
    
    def output_info(self, info_msg) -> None:
        """Outputs an informational message

        :param info_msg: the message to output
        :type info_msg: str|list
        """
        if isinstance(info_msg, list):
            formatted_msg = [self.style.NOTICE(line) for line in info_msg]
            self.stdout.writelines(
                formatted_msg
            )
        else:
            self.stdout.write(
                self.style.NOTICE(
                    info_msg
                )
            )
