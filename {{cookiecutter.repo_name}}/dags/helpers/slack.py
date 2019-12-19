from slackclient import SlackClient
from airflow.hooks.base_hook import BaseHook


def send_slack_notification(txt, channel, *args, **kwargs):
    """
    sends a notification to a slack channel
    :param txt: message string to send
    :param channel: slack channel to send the notification to
    :return:
    """
    try:
        slack_token = BaseHook.get_connection("slack").password
        sc = SlackClient(slack_token)
        sc.api_call("chat.postMessage", channel="#{}".format(channel), text=txt)
    except Exception as e:
        raise
