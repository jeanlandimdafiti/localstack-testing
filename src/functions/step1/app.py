from random import randint

def lambda_handler(event, context):
    """Sample Lambda function which returns a random number between 0 and 10 that is the
    value to be uset to the time in seconds to wait.

    Parameters
    ----------
    event: dict, required
        Input event to the Lambda function

    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    ------
        dict: Random number between 0 and 10
    """

    delay_time = randint(0, 10)

    return {"delay_time": delay_time}