This document covers some of the issues associated with first-time development environment setup and with collaboration using Git.

## Git and GitHub

### Installing Git

Please refer to the [installation guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) according to your operating system to install Git.

### Creating a GitHub account

If you do not have an account already, go to [GitHub](https://github.com) and sign up for an account.

### Git 101 Resources
For a primer on Git for first-time users, see the [try.github.io](https://try.github.io/levels/1/challenges/1) or watch the [following video](https://www.youtube.com/watch?list=PLyCZ96_3y5LXfPVZkHjhHRuIWhcjvCyQA&v=m_MjzgvVZ28) on how to (1) find an issue, (2) fork the code, (3) edit code, (4) open a pull request.

### Git status
By typing the `git status` command, we know if we have succesfully cloned the project, and which branch we are, as well as if there are any new files we've changed that git does not know about. Type this often.
```shell
$ git status
```
### Adding and committing your changes
Please commit your changes regularly! 
To do so, we first stage our changes:

```shell
$ git add .
```
The `.` or period symbol is a wildcard character that grabs all of your files within your currenty directory and below and "stages" them for Git.
```shell
$ git commit -m "YOUR COMMIT MESSAGE HERE"
```
We then commit our changes with the `-m` flag and our commit message in quotes. Make your commit as descriptive as possible in case you need to go back and find those changes!

### Syncing your Fork
Once you have forked the code and have begun contribution, [syncing your fork](https://help.github.com/articles/syncing-a-fork/) periodically with the main Pittsburgh Public meetings repository will be useful in staying up-to-date with the project.

1. You must first [add a remote link](https://help.github.com/articles/configuring-a-remote-for-a-fork/) from which Git can track the main City Bureau project. The remote URL is `<https://github.com/pgh-public-meetings/city-scrapers-pitt.git>`. Conventionally we name this remote source `upstream`. The remote source for your original cloned repository is usually named `origin`.

```shell
$ git remote add upstream https://github.com/pgh-public-meetings/city-scrapers-pitt.git
```

You can see your existing remotes as well by running `git remote -v`.

2. Once you've added the City Bureau remote, fetch the changes from upstream

```shell
$ git fetch upstream
```

3. Make sure you are in the branch you hope to merge changes into (typically your `master` branch), then merge the changes in from the `upstream/master` branch.

```shell
$ git checkout master
$ git merge upstream/master
```

4. The final step is to update your fork on Github with the changes from the original repository by running `git push`.

## Python and Pipenv

### [Installing Python and Pipenv on Windows](installing_python.md)
If you want to install python on windows [click here](installing_python.md). If
that tutorial didn't do it for you, here's another one.

 [Get started using Python on Windows for beginners](https://docs.microsoft.com/en-us/windows/python/beginners)

### Installing and using Pipenv

[Pipenv](https://pipenv.readthedocs.io/en/latest/) is package management tool for Python which combines managing dependencies and virtual environments. It's also designed to be compatible with Windows. Other tools like `virtualenv` and `virtualenv-wrapper` can be used, but our documentation will only refer to Pipenv since it's quickly being adopted as the standard for Python dependency management.

You can see installation instructions for Pipenv in the [Installing Pipenv](https://pipenv.kennethreitz.org/en/latest/install/#installing-pipenv) section of the documentation.
