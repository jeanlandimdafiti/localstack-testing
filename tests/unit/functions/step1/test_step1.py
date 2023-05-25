from src.functions.step1 import app

def test_step1():
    """
    Run 20 times the lambda and check if it always return an integer between 0 and 10.
    """

    for _ in range(30):
        delay_time_provider_result = app.lambda_handler("", "")
        random_int = delay_time_provider_result["delay_time"]

        assert 0 <= random_int <= 10
