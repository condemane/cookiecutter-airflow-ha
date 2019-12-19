import logging
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers.slack import send_slack_notification


class SlackOperator(BaseOperator):
    @apply_defaults
    def __init__(self, *args, **kwargs):
        super(SlackOperator, self).__init__(*args, **kwargs)
        self.txt = kwargs["txt"]
        self.channel = kwargs["channel"]

    def execute(self, context):
        """This method always runs when using this operator. This is where your logic should go"""
        try:
            send_slack_notification(self.txt, self.channel)
        except Exception:
            raise
