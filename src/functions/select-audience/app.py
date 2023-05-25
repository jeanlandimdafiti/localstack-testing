import os
from datetime import datetime, timedelta
from urllib.parse import urlparse, unquote

import pymysql.cursors
import hvac


def lambda_handler(event, context):
    """Lambda function which get audience from database.

    Parameters
    ----------
        event: dict, required
            Input event to the Lambda function

        context: object, required
            Lambda Context runtime methods and attributes

    Returns
    ------
        dict: information with campaign data and list of audience
    """
    vault_secrets = get_vault_secrets()

    id_list = get_audience_id_list(
        vault_secrets['campaign_database_url'],
        event['visit_time_range'])

    response = {
        'campaign': event['campaign'],
        'country': event['country'],
        'store': event['store'],
        'braze': {
            'canvas_id': event['braze']['canvas_id'],
            'objects_limit': event['braze']['objects_limit']
        },
        'audience': id_list
    }
    return response

def get_vault_secrets() -> dict:
    """Get database secrets keys from Vault.

    Parameters
    ----------
        None

    Returns
    ------
        dict: information about database url
    """
    try:
        client = hvac.Client(
            url=os.environ['VAULT_URL'],
            token=os.environ['VAULT_TOKEN'],
        )

        read_response = client.secrets.kv.v1.read_secret(
                mount_point=os.environ['VAULT_MOUNT_POINT'],
                path="campaign-segmentation-workflow"
        )
    except Exception as e:
        print(e)

    vault_secrets = {
        'campaign_database_url': read_response['data']['data']['campaign_database_url'],
    }

    return vault_secrets

def get_audience_id_list(campaign_database_url: str, visit_time_range: dict) -> list:
    """Get a list of ids from database in a period of time.

    Parameters
    ----------
        campaign_database_url: str, required
            Database connection url

    Returns
    ------
        dict: information with campaign data and list of audience
    """
    user_id_list = []

    database_url_parsed = urlparse(campaign_database_url)

    try:
        connection = pymysql.connect(
            host=database_url_parsed.hostname, 
            user=database_url_parsed.username,
            password=unquote(database_url_parsed.password),
            database=database_url_parsed.path.split('/')[1],
            port=int(database_url_parsed.port),
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            sql_query = """
                SELECT `id_hash` FROM `DAFITI_BR_MIAC_GENERAL` 
                WHERE `visit_time` BETWEEN %s AND %s """

            now = datetime.today() - timedelta(hours=3) # TO DO: Fix with UTC
            initial_date = now - timedelta(minutes=visit_time_range['start']) 
            final_date = now - timedelta(minutes=visit_time_range['end'])

            cursor.execute(sql_query, (initial_date, final_date))
            result = cursor.fetchall()

            for id in result:
                user_id_list.append(*id.values())
    except Exception as e:
        print(e)

    return user_id_list
