#Exercise 2

import re

'''
This comment section will describe the following variables - and corresponding
regex, where necessary - in order of appearance.

As a side note, it should be mentioned that a lot of the variables include
superfluous parentheses that make formatting look better. It should also be
mentioned that when something like "(X)" appears in this comment section it
means that "X" is optional for the expression in question.


#1. Times of day are the highlight of this expression. There's an optional "s"
after each one in case it's found in plural form. Also optionally one can find
"tomorrow" or "___day" preceding the times of day, the latter standing for any
day of the week but also for words like "weekday".
Negative lookahead has been included for a very special case mentioned in the
first part of this PDF.

#2. This appears after #1. because "weekday" is matched by itself. The first
two lines represent clear-cut relative temporal expressions while the third one
introduces a group that allows statements in the form of "(A)B past (C)D",
where A, B, C and D are digits that follow specific rules found in regex #2.
"midday" only appears following "before" or "after" in this file and thus
they're included in order to make the temporal expression more complete.

#3. Description of upcoming events. "week" can optionally turn into "weekend".

#4. This category was named after the main use of its subject. The expression
always ends in "X minutes", where X is any number. Optionally preceding that is
either "(a/1) hundred (and)" or "(an/1) hour (and)".

#5. Again, ordering is important because regex #4. matches combinations of
hours and minutes while this one matches "(less than) X (and (a) half) hours",
where X is any number.

#6. #7. These both refer to dates in a style similar to the file that was
available on Canvas. The first instance is unique and it refers to the pattern
"DAY MONTH Xth", while the second regex symbolises "(DAY) (the) Xth of MONTH
(YEAR)" which appears fairly often. "DAY" is the name of a day, "MONTH" is the
name of a month, "YEAR" is any year between 2000 and 2009 - the only year in
this file is 2007 anyway - "th" symbolises a group of suffixes to show rank,
and finally "X" is any number. "X" should be between 1 and 31 but it's left to
its own devices because of everything else surrounding it; nobody would say
"the 42nd of August".

#8. #9. There are four regexes combined here: prefixes, suffixes and two forms
of expressing time. Prefixes and suffixes were included because there are a lot
of instances where the time is referred to with a plain number, but when that
happens either a) there's a temporal prefix, b) there's a temporal suffix, or
c) time is described in a way covered by "clock" (explained farther down).
Therefore, regexes #8. and #9. cover "(PRE) clock/the_time SUF" and
"PRE clock/the_time (SUF)" respectively. That means that prefixes are optional
for the former and suffixes are optional for the latter, but they're never
optional at the same time to avoid matching numbers unrelated to temporal
expressions. Ordering is once more important because otherwise "clock pm" cases
are missed.

"the_time" is "(half) X\D" where "half" is optional, "X" is a number between 1
and 12, and "\D" is negative lookahead to avoid one specific case mentioned
in the first part of this PDF.

"clock" is "(X)X.YY\D" where "(X)X" is either a non-zero digit or a number from
00 to 23 and "YY" is a number from 00 to 59 and "\D" is the same as above.

Both of the above regexes are necessary for different expressions. That's why
they are separated by an "or" in #8 and #9.

#10. "clock" appears by itself to cover cases such as "05.50" and "2.20" where
no temporal prefix or suffix exists.

#11. "months" appears by itself because some of the questions refer to a month
instead of a specific date. Negative lookahead was included for one special
case mentioned in the first part of this PDF.

#12. "week_days" appears by itself for the same reason as #11.

#13. This category is last simply because it was noticed at the end. It matches
patterns like "(during) (the) SEASON", where "SEASON" is the name of a season.
'''


#1.
time_of_day = "((morning|afternoon|evening|night|midnight)s?)"
tod_prefixes = r"(((\w+day|tomorrow)\s+)?)"

#2.
special_cases = r"(tonight|tomorrow|weekday|" \
"at\s+the\s+moment|at\s+the\s+weekend|((before|after)\s+)?midday|" \
"[1-5]?\d\s+past\s+(1[0-2]|[1-9]))"

#3.
upcoming = r"(this|next)\s+(year|month|week(end)?)"

#4.
movies = r"(((a\s+|1\s+)?hundred\s+(and\s+)?)|" \
"((an\s+|1\s+)?hour\s+(and\s+)?))?" \
"\d+\s+minutes"

#5.
hours = r"(less\s+than\s+)?\d+\s+(and\s+(a\s+)?half\s+)?hours?"

#6. #7. #11. #12.
week_days = "(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"
months = "((January|February|March|April|May|June|July|August|September|" \
"October|November|December)(?!s))"

#6. #7.
rank = "(st|nd|rd|th)"

#8. 9. 10.
clock = r"(((([01]\d)|(2[0-3])|[1-9])\.[0-5]\d)(?!\d))"
the_time = r"(((half\s+)?(1[0-2]|[1-9]))(?!\d))"

prefixes = "(at|by|after|before|from|till|until)"
suffixes = "(o'clock|am|pm)"

#13.
seasons = r"((during\s+)?(the\s+)?(winter|spring|summer|autumn))"

timex = re.compile(
        "(" +
        
        #1.
        tod_prefixes + time_of_day + r"(?!s?\s+at\s+the\s+circus)" + "|" +
        
        #2.
        special_cases + "|" +
        
        #3.
        upcoming + "|" +
        
        #4.
        movies + "|" +
        
        #5.
        hours + "|" +
        
        
        #6.
        week_days + r"\s+" + months + r"\s+\d+" + rank + "|" +
        
        #7
        "(" + week_days + r"\s+)?(the\s+)?" + r"\d+" + rank + r"\s+of\s+" +
        months + r"(\s+200\d)?" + "|" +
        
        
        #8.
        "(" + prefixes + r"\s+)?(" + clock + "|" + the_time + r")\s*" +
        suffixes + "|" +
        
        #9
        prefixes + r"\s+(" + clock + "|" + the_time + r")\s*" +
        suffixes + "?" + "|" +
        
        
        #10.
        clock + "|" +
        
        #11.
        months + "|" +
        
        #12.
        week_days + "s?|" +
        
        #13.
        seasons +
        
        ")(?P<the_rest>.*)", re.I)


'''
"Between" code mentioned on the first page of the PDF.

        "between\s+(" + week_days + r"\s+)?(the\s+)?" + r"\d+" + rank +
        r"\s+of\s+" + months + r"(\s+200\d)?\s+and\s+" + "(" + week_days +
        r"\s+)?(the\s+)?"n+ r"\d+" + rank + r"\s+of\s+" + months +
        r"(\s+200\d)?" + "|" +
'''


'''
The last part of this program is almost untouched from the original version
uploaded by you. One change is that the output goes through .strip() first.
'''

try:
    file_questions = open("list-of-questions.txt")
    for question in file_questions:
        while True:
            match = timex.search(question)
            if match:
                print(question.strip())
                print("==>", match.group(1).strip(), "\n")
                question = match.group("the_rest")
            else:
                break

except IOError:
    print("The file with questions cannot be read")