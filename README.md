# eulerscraper

Scrapes all of the problems from projecteuler.net and sets up a 
directory with a file for each problem, with the text of the problem in
comments, along with the title and url.

## Usage

    python eulerscraper.py path/to/directory language
    
The path to directory does not have to exist yet. If the script would
overwrite any files, it skips that problem. Supported languages so far 
can be seen in `languages.json` - feel free to add more.

## Notes

Because there are a lot of problems, this script uses multiple
threads to download pages concurrently. Don't set the number of threads
too high or you risk angering the ProjectEuler gods (/sysadmins)!