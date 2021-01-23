# Tips and Tricks

### Additional Resources

Our lead coding committee volunteer Rebecca Wei produced a series of [video tutorials](https://www.citybureau.org/city-scrapers-tutorials) that can you and your staff/coding community navigate and troubleshoot common issues.

- [Github for Non-Coders, part 1](https://www.youtube.com/watch?list=PLyCZ96_3y5LXfPVZkHjhHRuIWhcjvCyQA&v=m_MjzgvVZ28)
- [Github for Non-Coders, part 2](https://www.youtube.com/watch?v=T4Pe_SK5knc&list=PLyCZ96_3y5LXfPVZkHjhHRuIWhcjvCyQA&index=5)
- [How to Run a Spider (Scraper)](https://www.youtube.com/watch?v=UgroG8CARWc)
- [Test Code with Scrapy Shell](https://www.youtube.com/watch?list=PLyCZ96_3y5LXfPVZkHjhHRuIWhcjvCyQA&v=7PJ02VtjKhs)
- [Build and Use Scrapy Pipelines](https://www.youtube.com/watch?list=PLyCZ96_3y5LXfPVZkHjhHRuIWhcjvCyQA&v=MtU4xuI8v4c)

### Regular Expressions:
Regular expressions are a powerful tool for searching text. Regular expressions use a sequence of characters to give instructions for what a program should search for in text. These instructions can be as simple as "Return values that contain this string", to more complex instructions like "Return values that begin with numbers 0-7 only if they aren't followed by characters A, B, or C" and so on. Regular expressions can be as complicated or simple as you need them to be, and are especially useful for web scrapers, which often have to retrieve information that only appear in certain patterns.

For an introduction to regular expressions, see [All you need to know about Regular Expressions](https://towardsdatascience.com/regular-expressions-in-python-a212b1c73d7f).

- [Regex syntax](https://www.debuggex.com/cheatsheet/regex/python) - for a regex syntax cheatsheet 
- [Regex checking tools](https://regex101.com/) - to practice and check your regular expressions

### Figuring out how a website changes over time:
A common hazard of web scrapers is that web sites change over time, and web scrapers can easily become outdated, searching for data in locations that are no longer valid, or whose identifying markers have changed. Something as simple as changing a header tag from "h3" to "h4" can break a web scrapers, and in those cases it helps to know what a web page looked like at the time the web scraper was designed. To better identify how a website has changed, we can reference __The Wayback Machine__, a digital archive of websites that can show what websites looked like in the past. 
- [WaybackMachine](https://archive.org/web/web.php)

### Reading Spider Output
- Scrapy `-o` flag
- [jsonprettify](http://jsonprettify.com/)


---
## IDEs
Integrated Development Environments, or __IDEs__, are software applications that provide common tools to programmers for software development. While programmers *could* write all of their code in simple text editors like Notepad and TextEdit, more sophisticated IDEs offer useful features like highlighting language-specific syntax, pointing out errors, and offering useful features for commenting multiple lines at once, or finding and replacing specific text in a document. Below are some of the most common IDEs.
#### [Atom](https://atom.io/)
- [Pretty JSON](https://atom.io/packages/pretty-json)
- [Platformio IDE Terminal](https://atom.io/users/platformio)
#### [Pycharm](https://www.jetbrains.com/pycharm/)
#### [Sublime Text](https://www.sublimetext.com/)
#### [Vim](https://realpython.com/vim-and-python-a-match-made-in-heaven/)
---
#### How to tackle a page efficiently:
1. JSON
2. Legistar
3. Regex

Feel free to comment below with your favorite tools and I will add them!
