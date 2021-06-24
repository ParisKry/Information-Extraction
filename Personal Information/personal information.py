import re

try:
    file_handle = open("text_about_people.txt", encoding = "utf8")
except IOError:
    print("An error occured while opening the file for reading")

'''
Since most of the big picture analysis for this program can be found in the
beginning of this PDF, here comments will be used to describe the expressions
themselves. The numbering system is consistent with the one mentioned earlier.
'''

'''
The very first regex used is simply a comprehensive list of titles found at the
very beginning of the lines of the txt file. "PhDr." was a special case because
of the period at the end (which had to be escaped) and because it was missed
during the first pass. No matter which title is matched, the whitespace right
after it should not be neglected, otherwise future matching would be
problematic.

A tactic was then reused from exercise 2, week 10 where after a search() is
completed everything that comes after it is grouped together so that *it* may
be searched anew. This is used again when matching dates.
'''

#1.
title = re.compile("^(Archduke|Archbishop|Marshal|Baron|Prince|Count|PhDr\.)\s"
                   + "(?P<the_rest>.*)")

'''
Short regex that was used to make the compile() that follows it look a little
nicer. It simply covers cases where "de" or "von" (followed by a space)
appears, but of course it's matched optionally.
'''

#1.
de_von = "((de|von)\s)?"

'''
Three separate regexes are used to match names - all of them looking
exclusively at the beginning of the line, as mentioned before - but most of the
work is done by the first one.

i. Alphanumeric characters are matched until a space is found and then that is
matched as well. If "de" or "von" follows it is matched. Then there's a loop of
at least one instance of an uppercase letter followed optionally by
alphanumberic characters and dashes, with optional "de"s or "von"s in between.

ii. Positive lookahead was used for single names that are followed by a comma.
This includes "Sophie,", "Karl," and "Archduke Friedrich,", since "Archduke"
gets filtered out before this stage.

iii. Positive lookahead is used again, this time for single names followed by
"of" or "(". These are "Johann (Yona)" and "Archduke John of Austria".
'''

#1.
person = re.compile("(" +
        
        "^\w+\s" + de_von + "([A-Z](\w-?)*\s?" + de_von + ")+" + "|" +
        
        "^\w{4,}(?=,)" + "|" + "^\w{4,}(?=(\sof|\s\())" +
        
        ")")

'''
Code was again partially reused, namely the regex that covers month. From there
it was only necessary to add an expression for numbers 1-31 and finally one for
years - in the file there are no years before 1000 or after 1999. There are
three patterns used for dates: "MONTH NUMBER, YEAR", "NUMBER MONTH(,) YEAR" and
finally "YEAR". In the first one the comma *always* appears while in the second
it only appears a few times, so it had to be made optional.
'''

#2.
months = "(January|February|March|April|May|June|July|August|September|" \
"October|November|December)"
month_number = "(3[01]|[12]\d|[1-9])"
year = "1\d{3}"

dates = re.compile("(" +
        
        months + "\s" + month_number + ",\s" + year + "|" +
        
        month_number + "\s" + months + ",?\s" + year + "|" +
        
        year +
        
        ")(?P<the_rest>.*)")

'''
This segment had to be of this length because of the three variations for the
lookbehind: professions are matched after "was a", "was an" or "was the" is
found and those three had to be separate. The main regex itself is simple
enough: it keeps matching until the first comma or period is found.
To make some outputs shorter, a lookahead was added to exclude text that
appears after a "who" is matched, since that text usually doesn't have any
new professions to add. Since most of the cases did not have a "who", however,
it had to be an option that appears in the beginning of the regex so that the
regular version can be split with an "|" to cover all bases.
'''

#3.
profession = re.compile("(" +
        
        "(?<=was\sa\s)([^,\.]+)(?=who)" + "|" +
        
        "(?<=was\san\s)([^,\.]+)(?=who)" + "|" +
        
        "(?<=was\sthe\s)([^,\.]+)(?=who)" + "|" +
        
        "(?<=was\sa\s)([^,\.]+)" + "|" +
        
        "(?<=was\san\s)([^,\.]+)" + "|" +
        
        "(?<=was\sthe\s)([^,\.]+)" +
        
        ")")

'''
Last comment section for portfolio part 2!

The first thing this for loop does - after printing the input for reference is
it tries to filter out titles found at the very beginning; if one isn't found,
nothing happens.
Then it tries to match a person's name(s). If it fails the program goes on to
the file's next line. Otherwise it prints the name(s) found and goes on to
search for a date.
However it is not printed right away; a second date is searched for in the text
following that of the first date matched. Then if *that* is found both dates
are printed, the first one assumed as the date of birth and the second as the
date of death. There was no instance matched where one appeared without the
other so no information is lost here.
Finally, assuming a name was matched earlier, a search is conducted for
professions. If any are found, they are printed.
The last print() exists purely for formatting reasons. The two strip() methods
used are also used to avoid printing whitespace.
'''

for line in file_handle:
    print(line)
    
    match_title = title.search(line)
    if match_title:
        line = match_title.group("the_rest")
    
    match_name = person.search(line)
    if match_name:
        print("==> Name:", match_name.group(1).strip())
        
        match_dob = dates.search(line)
        if match_dob:
            print("==> Date of birth:", match_dob.group(1))
            line = match_dob.group("the_rest")
            
            match_dod = dates.search(line)
            if match_dod:
                print("==> Date of death:", match_dod.group(1))
        
        match_prof = profession.search(line)
        if match_prof:
            print("==> Profession(s):", match_prof.group(1).strip())
    
    print()

file_handle.close()