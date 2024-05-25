## Assignment 01: Set up and prerequisites

1. Git
- Install git.
https://git-scm.com/downloads

- You may see references to the stand alone app for git on your desktop. That's not what we're using for this course.

- Watch the videos in this series that you need to watch (seriously, even if you've been working with git for a while, it's sometimes handy to revisit, e.g., the difference between git and Github). They are on youtube. If you don't have a subscription, it will pop up with short ads. Sorry, but these are really decent videos. There's about 30 min total.

https://www.youtube.com/playlist?list=PL5-da3qGB5IBLMp7LtN8Nc3Efd4hJq0kD

- Follow the instructions to do what the videos walk you through.



2. Data Engineering Jobs

- Google "data engineering jobs"
- Read ads (between 5&10)
- What are companies looking for in skills, experience, competencies?
  * Answer: Many companies are looking for a Data Engineer: 
  
  1. Disney, ABC, NBC on the entretainment business. They want people with experience in Hadoop, Spatk, SQL, etc.
  2. Morgan Stanley, JP Morgan, Hedge Funds in the finance sector. They want people to build trading pipelines with connections with kdb, Python, SQL.
  3. AETNA, Avery, Medical hospital in the healtcare sector. They want people to build the entire pipeline.


3. Submit a PR for this assignment.
- You changed this `README.md` in part 2;

- Commit your changes.

- Submit a PR with this `README.md` changed.
(following the instructions from the synchronous session)


4. You should know a few things about Markdown, the markup language that  determines how things look when you view them on the Github web interface. That is what we see when we review your work, so you should always check to see how your `README.me` file looks before you submit. You might check out [this cheat sheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) for some pointers.

Markdown is designed to look pretty much in plain text the way that you might guess it would look when made into pretty HTML.

### Here are some basics.

Use `#`, `##`, `###`, and so on to indicate headers. The header above is `###`.

```
Emphasis, aka italics, with *asterisks* or _underscores_.

Strong emphasis, aka bold, with **asterisks** or __underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses two tildes. ~~Scratch this.~~

[This is a link](https://www.google.com)

```

Look like this:

Emphasis, aka italics, with *asterisks* or _underscores_.

Strong emphasis, aka bold, with **asterisks** or __underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses two tildes. ~~Scratch this.~~

[This is a link](https://www.google.com)

#### Formatting Code

Since much of what we'll be doing is showing code and output, it's important to know how to display that such that it is readable.

    Inline `code` has `back-ticks around` it.

Inline `code` has `back-ticks around` it.


Blocks of code can be indicated by indenting with 4 spaces or with three back-ticks (<code>```</code).


    ```sql
    SELECT this, that, the_other
    FROM my_table
    ```

```sql
SELECT this, that, the_other
FROM my_table;
```

    ```
    col1               col2               col3
    fun                dog                cat
    mouse              rat                banana
    ```

```
col1               col2               col3
fun                dog                cat
mouse              rat                banana
```
without the backticks, that sql would look like:

SELECT this, that, the_other
FROM my_table;


and that pretty table would look like this (please don't do this!!):

col1               col2               col3
fun                dog                cat
mouse              rat                banana
