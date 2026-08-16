import json


def parse(text):
    plan = json.loads(text)
    if "fclass" in plan:
        if isinstance(plan["fclass"], str):
            plan["fclass"] = plan["fclass"].strip()
        elif isinstance(plan["fclass"], list):
            plan["fclass"] = [
                x.strip()
                for x in plan["fclass"]
            ]
    return plan