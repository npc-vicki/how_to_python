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

### Okay, let's actually do something with pipenv

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

```
pip install pipenv
```
