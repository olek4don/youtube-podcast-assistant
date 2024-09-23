# %%
dic = {
    "test": "test1",
    "test2": "test3",
    "test3": "test5",
}

portfolio = [
    ("ACME", 12, 15.0),
    ("WIG", 8, 20.0),
    ("DELL", 2, 50.0),
    ("WIG", 16, 20.0),
]

total_shares = {s[0]: 0 for s in portfolio}
print(total_shares)

for name, shares, _ in portfolio:
    total_shares[name] += shares
print(total_shares)

# %%
import re

strings = ["ariaNa's", "brutal", "the condon"]
pattern = "|".join(re.escape(c) for c in strings)
print(pattern)

# %%
# Lists of guests and times
guests = ["Elon Musk", "DJ Seo", "Matthew McDougall", "Bliss Chapman", "Noland Arbaugh"]
starts = ["00:00:00", "01:27:34", "03:38:39", "05:06:01", "06:48:53"]

# zip both lists

guest_time = list(zip(guests, starts))
print(guest_time)

# %%
# fill up with real excercises
list_of_excercies = [
    {"exercise_name": "shoulder press", "type_of_activity": "bench press"},
    {"exercise_name": "squats", "type_of_activity": "deadlift"},
    {"exercise_name": "bench press", "type_of_activity": "abdominals"},
]

entry_template = """
exercise_name: {exercise_name}
type_of_activity: {type_of_activity}
""".strip()

context = ""

for i in list_of_excercies:
    context = context + entry_template.format(**i) + "\n\n"
print(context)
