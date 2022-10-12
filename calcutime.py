import re
import subprocess
import sys


def _invalid():
    print(
        "Invalid. It should be only digits with\
 operator(*/+-) with or without spaces, parenthesis."
    )
    sys.exit()


PATTERN = r"[*/+-]?\s*?\(.*?\)"
EXECUTE = False
DONE = False
PASS = False

USER_INPUT = input("$ ")
if re.search(r"^(?<!\D)\d+(\.\d+)?(?!\D)$", USER_INPUT):
    PASS = True
elif re.search(r"[^\s\d*/+-.()]", USER_INPUT):
    _invalid()


while True:
    if PASS:
        break
    MATCH = re.search(rf"{PATTERN}", USER_INPUT)
    if MATCH:
        EXECUTE = True
        MATCH = USER_INPUT[MATCH.start():MATCH.end()]
        RE_OPERATORS = re.findall(r"[*/+-]", MATCH)
        RE_OPERATORS_LIST = RE_OPERATORS
        if len(RE_OPERATORS_LIST) == 2:
            FIRST_OPERATOR, SECOND_OPERATOR = RE_OPERATORS
        else:
            SECOND_OPERATOR = RE_OPERATORS
            SECOND_OPERATOR = str(SECOND_OPERATOR)
            SECOND_OPERATOR = re.sub(r"\['|'\]", "", SECOND_OPERATOR)
            FIRST_OPERATOR = ""
        FIRST_NUMBER, SECOND_NUMBER = re.findall(r"\d+\.\d+|\d+", MATCH)
        FIRST_NUMBER = float(FIRST_NUMBER)
        SECOND_NUMBER = float(SECOND_NUMBER)
        match SECOND_OPERATOR:
            case "+":
                RESULT = FIRST_NUMBER + SECOND_NUMBER
            case "-":
                RESULT = FIRST_NUMBER - SECOND_NUMBER
            case "*":
                RESULT = FIRST_NUMBER * SECOND_NUMBER
            case "/":
                RESULT = FIRST_NUMBER / SECOND_NUMBER
        if FIRST_OPERATOR == "":
            USER_INPUT = USER_INPUT.replace(f"{MATCH}", f"{RESULT}")
        else:
            USER_INPUT = USER_INPUT.replace(
                f"{MATCH}",
                f"{FIRST_OPERATOR} {RESULT}")
    else:
        match PATTERN:
            case r"[*/+-]?\s*?\(.*?\)":
                PATTERN = r"\d+(\.\d+)?\s*?[*/]\s*?\d+(\.\d+)?"
            case r"\d+(\.\d+)?\s*?[*/]\s*?\d+(\.\d+)?":
                PATTERN = r"\d+(\.\d+)?\s*?[+-]\s*?\d+(\.\d+)?"
            case r"\d+(\.\d+)?\s*?[+-]\s*?\d+(\.\d+)?":
                DONE = True
        if DONE:
            if EXECUTE:
                break
            _invalid()
            break


# ------------------------------------------------------------ #


def output(hour, minute, am_or_pm="", one_twenty_four="\n24"):
    if one_twenty_four == "12":
        if (hour >= 12) and (hour != 24):
            am_or_pm = "PM"
        else:
            am_or_pm = "AM"
        if hour > 12:
            hour = hour - 12
    if hour < 10 and minute < 10:
        print(
            f"{one_twenty_four} hour one_twenty_four:\
 0{hour}:0{minute} {am_or_pm}"
        )
    elif hour < 10:
        print(
            f"{one_twenty_four} hour one_twenty_four:\
 0{hour}:{minute} {am_or_pm}"
        )
    elif minute < 10:
        print(
            f"{one_twenty_four} hour one_twenty_four:\
 {hour}:0{minute} {am_or_pm}"
        )
    else:
        print(
            f"{one_twenty_four} hour one_twenty_four:\
 {hour}:{minute} {am_or_pm}"
        )


def splitter(string):
    string = string.replace('"', "")
    string = int(string)
    return string


LINE = "# -------------------------------------------------------- #"

# ------------------------------------------------------------ #

print(LINE)
print("ADDED TIME:")
USER_INPUT = round(float(str(USER_INPUT)))
if USER_INPUT < 60:
    ADD_MINUTE = USER_INPUT

ADD_HOUR = round(USER_INPUT / 60)

if USER_INPUT < 0 or ADD_HOUR >= 24:
    print("Less than 0 and more than a day is not supported, sorry.")
    sys.exit()

while USER_INPUT > 1:
    USER_INPUT = USER_INPUT - 60
    if not USER_INPUT < 0:
        ADD_MINUTE = USER_INPUT

output(ADD_HOUR, ADD_MINUTE, one_twenty_four="24")
output(ADD_HOUR, ADD_MINUTE, one_twenty_four="12")
print(LINE)

# ------------------------------------------------------------ #


print("CURRENT TIME:")

TIME = subprocess.run(
    ["/bin/date", '+"%H:%M"'], capture_output=True, text=True, check=True
).stdout
SPLIT = TIME.split(":")

CURRENT_HOUR = splitter(SPLIT[0])
CURRENT_MINUTE = splitter(SPLIT[1])

output(CURRENT_HOUR, CURRENT_MINUTE, one_twenty_four="24")
output(CURRENT_HOUR, CURRENT_MINUTE, one_twenty_four="12")
print(LINE)


# ------------------------------------------------------------ #


print("TOTAL TIME:")

TOTAL_HOUR = CURRENT_HOUR + ADD_HOUR
TOTAL_MINUTE = CURRENT_MINUTE + ADD_MINUTE

if TOTAL_MINUTE >= 60:
    TOTAL_HOUR = TOTAL_HOUR + 1
    TOTAL_MINUTE = TOTAL_MINUTE - 60

if TOTAL_HOUR > 24:
    print("It's more than a day, sorry.")
    sys.exit()

output(TOTAL_HOUR, TOTAL_MINUTE, one_twenty_four="24")
output(TOTAL_HOUR, TOTAL_MINUTE, one_twenty_four="12")
print(LINE)
