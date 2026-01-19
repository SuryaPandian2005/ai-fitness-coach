def progress_prompt(previous_plan, weight_change):
    return f"""
The user followed this plan:
{previous_plan}

Progress update:
Weight change in last week: {weight_change} kg

Adjust the workout and diet plan for the next week.
Focus on healthy progress.
"""
