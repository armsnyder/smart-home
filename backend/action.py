"""
Contains all code pertaining to handling verbal requests through the Google Assistant, interacting with the required
backend objects, and returning a verbal response.
"""


def respond_to_request(request_json):
    """
    The main entrypoint to the Google Assistant backend.
    :param request_json: A request object containing information about the voice command issued
    :return: A compliant dictionary to return to the google frontend containing text for the assistant to speak
    """
    # Example response that echos the user request text
    return {
        "conversation_token": "42",
        "expect_user_response": False,
        "final_response": {
            "speech_response": {
                "text_to_speech": request_json['inputs']['raw_inputs'][0]['query']
            }
        }
    }
