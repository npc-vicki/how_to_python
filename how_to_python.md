# How to Python nicely

All I want is to learn Python. To learn Python, I want to set up an environment where I can work with Python the way I feel I deserve to be able to work with a modern language. This involves stuff like:

- Managing Python versions (with asdf?)
- Managing packages
- Explicitly declaring the dependencies of a project (like with npm or bundler)
- Installing these dependencies with a single command (bonus points if this doesn't affect globally installed packages or installed dependencies of other, unrelated projects)

Is this too much to ask for? We'll see.

## Installing Python nicely

On my Mac, I already have Python installed several times. I have it because it comes with OSX, but I also have `python` and `python3` installed with Homebrew because other Homebrew packages depend on them. This is already confusing. I feel like I want a version manager.

There's a python plugin for `asdf`: https://github.com/tuvistavie/asdf-python

I have a bad feeling about this (a.k.a. I remember trying to do this before and eventually running into problems with asdf), but let's go along with it. Further below, you will witness me remembering what the problems were, and stumbling upon the solution (it turns out that I just did a silly thing). So with that bit of narrative tension unresolved, let's keep going with asdf.

```
asdf plugin-add python https://github.com/tuvistavie/asdf-python.git
asdf install python 3.6.4
asdf global python 3.6.4
```

Seems legit:

```
% python --version
Python 3.6.4
```

## Installing packages nicely

I'd like to be able to install packages on a project-by-project/repo-by-repo basis, such that they're explicitly listed (with versions) in some sort of text file, allows me to separate the installed dependencies for different projects. `pip` seems to be _the_ way to install packages, but I don't want to just globally install packages without documenting them per project.

### A crossroads

After a bunch of googling, I think I've narrowed this down to two options that both seem pretty legit, well-defined and more or less tick my boxes. Number one seems like an uncontroversial, time-honoured Pythony way to do things, number two is newer and maybe less popular(?), but also feels more familiar given the sort of tools I'm already familiar with (like bundler and npm).

To be honest, the more I read about it the more I realised that the first one is probably a dead end and the second one is less controversial/immature than I realised, so you could just skip the first section and just use `pipenv`. The little diversion below might help explain what `pipenv` does and why we want it, though. The main reason I didn't just start using it as soon as I found it was that it seemed to perform so much magic that I didn't understand. After reading about the alternatives I feel like I understand the magic better, and am happier using it.

#### Path The First

* Use a tool to create a "virtual environment" in a given directory (e.g. for a project). You can do this with `virtualenv`, but it seems better to use one of several tools that wrap around `virtualenv`, e.g. `pyenv` or `venv` which comes with Python 3. `pyenv` can also manage Python versions (actually that seems to be its main purpose).
* Happily go on installing `pip` packages inside this virtual environment, knowing that they're only installed in this project-specific little world.
* To document the dependencies, we can use a [`requirements.txt` file](https://pip.pypa.io/en/stable/user_guide/#requirements-files). `pip freeze > requirements.txt` to codify the packages you've installed, and `pip install -r requirements.txt` to install them. I feel like I could live with that for a small project, but [sounds a bit complicated for bigger things](https://www.kennethreitz.org/essays/a-better-pip-workflow).
* Alternatively, we can use a [Pipfile](https://github.com/pypa/pipfile), which is a new fancy thing. But this leads us towards the second path, which (as I'm reading about this) I increasingly think is the way to go.

#### Path The Second

[Pipenv](https://github.com/pypa/pipenv) seems to pretty much do the above for you. It wraps around `virtualenv` to set up a project-specific virtual environment, and implements the `Pipfile` format to manage your dependencies. All this with simple commands that will hopefully feel familiar from the tooling of other nice languages. Apparently this solution is [officially recommended](https://packaging.python.org/tutorials/managing-dependencies/#managing-dependencies) by python.org.

### Okay, let's install pipenv then

I need Python and Pip. Apparently the asdf plugin for Python comes with Pip installed. Nice.

```
% pip --version
pip 9.0.1 from /Users/erik/.asdf/installs/python/3.6.4/lib/python3.6/site-packages (python 3.6)
~/src/erik/python (master)● % python --version
Python 3.6.4

```

So let's install `pipenv`.

This brings us to *a very important gotcha!* Various things on the internet, like [the pipenv tutorial on python.org](https://packaging.python.org/tutorials/managing-dependencies/#managing-dependencies) will tell you that you should `pip install --user` this instead of installing it globally, to avoid breaking system packages. This sounds like a great idea, but not if you use `asdf`. With `--user`, the packages will get installed in `~/.local/` - i.e. outside of `asdf`'s nice, version-managed world. If you install other Python versions, the packages in `~/.local/` will still get picked up, and if you uninstall Python entirely (in `asdf`), they'll still be there. Whereas if we install them "globally" (without `--user`), they'll be installed inside somewhere in `~/.asdf/` and will play well with the way we want to be able to use asdf. Yay!

*This is actually where my vague memory of having a bad feeling about `asdf` came from.* I previously tried to do all this with `asdf`, naively and unknowingly `pip install --user pipenv` and started feeling suspicious and frightened as files started appearing in `~/.local`, as I needed to add `~/.local/bin` to my `PATH`, and so on... Turns out it's fine if you do it right! So with that tension nicely resolved, let's go on.

```sh
pip install pipenv
```

The first time I tried this, I got the error:

```
Could not import setuptools which is required to install from a source distribution.
Please install setuptools.
```

I don't really know why this happened, but it seems that `setuptools` is a pip package and that we just need to install it. (It seems strange to me that pip, a tool for installing packages and their dependencies, didn't figure this out and do it by itself, but whatever.)

```sh
pip install setuptools
pip install pipenv
```

Now that it's installed I want to run it.

```
% pipenv --version
zsh: command not found: pipenv
```

Sad. I think this is because the `pipenv` executable is now sitting somewhere in the depths of `~/.asdf/`, and asdf hasn't yet figured out that it's a thing you want to be able to run and that needs to be in your `PATH` (i.e. it needs to have a "shim" for it). Luckily there's a magic command that sorts this out:

```sh
% asdf reshim python
```

Now we can run pipenv:

```
% pipenv --version
pipenv, version 9.0.1
```

### Actually doing a thing with pipenv

Let's pretend we want to do some data science.

```sh
mkdir data_science
cd data_science
```

I know a lot of people use pandas to data science, so I want to install pandas.

```sh
pipenv install pandas
```

This does a bunch of things. One of them is to create a "virtualenv", which apparently lives in `~/.local/share/virtualenvs/data_science-OooVusIR`

I was hoping I could let everything live inside asdf, but I guess this will have to be an exception. If I want to cleanse my system of all this stuff, I guess I'll have to remove this `~/.local/share/virtualenvs` directory.

It's also created a `Pipfile` and a `Pipfile.lock`. Nice and familiar!

We can run stuff inside the virtual environment with `pipenv run`. This seems pretty much the same as `bundle exec`:

```
% pipenv run python
Python 3.6.4 (default, Jan  3 2018, 13:28:44)
[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.39.2)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pandas as pd
>>>
```

This works, so I guess I have pandas now.

Just type `pipenv` to get some colourful advice on what commands you can run.

* `pipenv install --dev` is for dev-only dependencies, just like with npm
* `pipenv --rm` removes the virtual environment again.
* `pipenv install`, given that we have a Pipfile, installs the dependencies in the Pipfile just like `bundle install`

Having done that, I feel pretty content that this lets me do what I wanted it to do. Time for a cup of tea!

## Tests?

I want to be able to write tests, and run them all easily.

As with most things Python in my experience so far, the hard thing isn't figuring out how to use something, but figuring out which of the three or four things I should be using. The short answer seems to be that I should use `pytest`. It wraps around the built-in `unittest` library, and lets you avoid a lot of boilerplate. It also seems widely used. Cool.

`doctest` might also be useful for some scenarios (especially the sort of little toy projects I'm likely to do while learning). Elixir has this feature built in (also called `doctest`) and it's nice. It lets you write little usage examples in comments right next to your functions, and turns them into assertions that you can run. Cool for speedy TDD.

`unittest.mock` seems to be the way to do mocking if you need to do mocking.

`hypothesis` does property based testing.

## What about Conda?

The stuff above gets me to a setup that I feel very comfortable with as a Rubyist/Elixirist/Javascriptist. But I want to (pretend to be) a data scientist. They do things differently.

They use Conda. I think. My first impression of this was that it's some sort of friendly and bloated Python distribution - it's a big thing that you install and it comes with all the packages you'll ever need preinstalled, so you never have to be explicit about any dependencies or understand where anything came from. Great if you're coming from a relatively non-technical background, grubby as hell if you're a developer. Then I [watched a talk](https://www.youtube.com/watch?v=9by46AAqz70) and [read an article](https://jakevdp.github.io/blog/2016/08/25/conda-myths-and-misconceptions/), and I don't think it seems that bad any more.

Conda lets us do what `pipenv` lets us do, i.e. create multiple isolated environments and install packages inside them. The difference is that `pip` only manages Python packages. Some packages that are used for data sciencing (so I hear) depend on non-Python binaries/libraries/whatever. With `pip` we'd have to `brew install` these or something, and besides the `Pipfile` we'd need to come up with some other way of dealing with non-Python dependencies. Or we can use Conda to manage all these dependencies instead. Sounds great.

There's Anaconda, which is kind of the friendly but grubby thing I mentioned above, a huge prepackaged bunch of packages (which I hasten to add I'm sure is very convenient and useful in a lot of situations). There's also Miniconda, which is just the package manager with nothing preinstalled. I think I want Miniconda.

We could download the official installer (or `brew cask install miniconda`), but this would take over our system Python, and completely destroy my dream of using asdf to version-manage everything. Good news: looks like you can install Miniconda with asdf.

```sh
asdf install python miniconda3-4.3.30 # the latest version right now

# I'll leave my system python as it is for now and just play around with this
mkdir more_data_science
cd more_data_science
asdf local python miniconda3-4.3.30
```

I now have conda, but I no longer have python. I guess miniconda doesn't even come with Python preinstalled:

```
% conda --version
conda 4.4.6
% python --version
No such command in miniconda3-4.3.30 of python
```

Conda seems to behave a lot like any other nice, familiar package manager - just `conda` gives a list of useful commands. So I'll `conda search python`, and `conda install python=3.6.4`, which is the latest version.

It looks like this created a new environment for me - I'll need to figure out what this means, and how to manage more environments, later. For now, I can see that the "environment location" is `~/.asdf/installs/python/miniconda3-4.3.30` - this directory seems to have a whole Unix-style filesystem hierarchy inside it, and this is where Conda has now installed Python, as well as its non-Python dependencies like OpenSSL. It's all nicely contained within a conda environment which is contained within asdf. Success!

![Yo dawg, I heard you like version managers so I put a version manager in your version manager so you can version manage while you version manage - Xzibit](https://memegenerator.net/img/instances/500x/81027239/yo-dawg-i-heard-you-like-version-managers-so-i-put-a-version-manager-in-your-version-manager-so-you-.jpg)

### Multiple Conda environments

One thing conda lets you do is create multiple named environments (with different stuff installed) and switch between them. I ran into some problems with asdf when I tried this. Let's create a new named environment with Python 3.6 installed:

```sh
conda create --name huzzah python=3.6
```

Now you're supposed to be able to switch to this environment like this:

```sh
source activate huzzah
```

but this exits my shell. Before exiting, it says `Error: activate must be sourced. Run 'source activate envname' instead of 'activate envname'.`.

Turns out this is a known problem with version managers that rely on shims, like asdf. It's not very well-attested (or googlable) with asdf, but there are [multiple reports](https://encrypted.google.com/search?hl=en&q=pyenv%20conda%20activate%20crashes%20shell) of the same problem with `pyenv`, which works in a similar way. [Here's a comment that sort of explains the reason.](https://github.com/pyenv/pyenv/issues/662#issuecomment-269145248) The issue is that the script is meant to be sourced, but shims are meant to be executed, not sourced - trying to source a shim (which is what we're doing when we `source activate` - see `which activate`) actually executes the file that it ultimately refers to (hence why it thinks it's been executed, not sourced). Tl;dr: this explanation led me to a fix - instead of trying to source the shim, we can source the `activate` script directly:

```sh
source ~/.asdf/installs/python/miniconda3-4.3.30/bin/activate data
```

This is pretty horrible. I guess I could alias it or something. I could also add `~/.asdf/installs/python/miniconda3-4.3.30/bin/` to my PATH (before the asdf shims directory) so I can `source activate` again, but this would seriously mess with asdf. I think an alias might be the way forward (although it'll need to change when I update the miniconda version in asdf).

## Other notes and links

* [The Definitive Guide to Python import Statements](https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html)
