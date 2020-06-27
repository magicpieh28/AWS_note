import json
import random

idempotent = None


def lambda_handler(event, context):
    global idempotent
    first_invoke_seed = random.seed
    local_idempotent = None
    if idempotent is None:
        idempotent = first_invoke_seed
        local_idempotent = first_invoke_seed

    if idempotent == local_idempotent:
        pass
