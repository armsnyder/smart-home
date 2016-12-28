
__MAIN = 'assistant.intent.action.MAIN'
__START_FIREPLACE = 'START_FIREPLACE'


def handle(request_object):
    intent = request_object['inputs'][0]['intent']
    return {
        "conversation_token": "42",
        "expect_user_response": True,

        "expected_inputs": [
            {
                "input_prompt": {
                    "initial_prompts": [
                        {
                            "text_to_speech": "What is your next guess?"
                        }
                    ],
                    "no_input_prompts": [
                        {
                            "text_to_speech": "I didn't hear a number."
                        },
                        {
                            "text_to_speech": "If you're still there, what's your guess?"
                        },
                        {
                            "text_to_speech": "We can stop here. Let's play again soon."
                        }
                    ]
                },
                "possible_intents": [
                    {
                        "intent": "assistant.intent.action.TEXT"
                    }
                ]
            }
        ]
    }
