# FixityChecker

This checks a fraction of all files. 
usage:

python Checker.py Directory

-------------------------------------------------------
By default, it checks one file in 10. You can specify this with an optional argument:

python Checker.py Directory (interval)

where interval is an integer. It will check the 1st file in every (interval) files.

-------------------------------------------------------
Also, if you want it to check the 2nd file, or the nth file instead of the first (so that you don't always check the same ones), there is an optional third argument for the offset:

python Checker.py Directory (interval) (offset)

Which makes it check the nth file in every interval files. Example:

python Checker.py Directory 20 5

will check the the fifth file in every batch of 20.
