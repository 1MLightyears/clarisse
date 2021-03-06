[toc]

# Clarisse

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/clarisse?style=plastic)![PyPI](https://img.shields.io/pypi/v/clarisse?style=plastic)

:cn::[说明文档](./README_zh-cn.md)

Clarisse is a light-weighted Python function GUI framework.

With at least one single line of code, you can easily create a user-friendly GUI for your code(or a part of your code), yet not make other changes!

### TL;DR

If you have a function like

```python
def func(arg1,arg2:int,arg3:str="have a try")->bool:
    ...
```

To give a GUI to a function like above, simply:

```python
from clarisse import Clarisse

@Clarisse()
def func(arg1,arg2:int,arg3:str="have a try")->bool:
    ...
```

It's done.

Any time when `func()` is called, a GUI will be showed, allowing user to manually input/modify/check the arguments about to be given to the original`func()` and get executed.

```python
@Clarisse()
def func(arg1,arg2:int,arg3:str="have a try") -> bool:
    """This is only a ***test*** function\\
    but enough to show what clarisse can do!"""
    print("arg1 is {0}".format(arg1))
    print(arg3.upper())
    return arg2>10

print(func("this is output",0))
```

<img src="./img/img1.png"  style="zoom : 80%">

##### Clarisse understands your need! 

In the example above, `func()` still returns the original `bool` type value as if not modified(decorated); the arguments given when calling `func()` will be default values of them and be shown on the GUI.

##### Clarisse provides you plenty of choices!

You can run `func()` multiple times ( by clicking the `Run` button ) and check the output in the output dialog provided, and close the window to "confirm" the last result as your final run.

### Installation

```bash
#pip install clarisse
```

Clarisse uses PySide2 as its backend GUI framework.

Clarisse works well on Python 3.9.1 .

### Customization

1. After using `@Clarisse()`, there are two ways to set the default value/ placeholder text for arguments : the `def` header of the function, the arguments' value when calling the function. The later way is prior than the former way.
2. The window could also be modified by giving arguments to `@Clarisse`.
   1. `margin` is the distance from the widgets to the edge of window;
   2. `vert_spacing` is the distance between widgets;
   3. `description` is the introduction of the function as a default(`func.__doc__`), but could also be customized to any other words you like;
   4. `args_desc` is a list of string, each is used to replace the description label of an argument.
   5. `args_kwdesc` is similar with `args_desc`, but description label are given as a `dict` like  `{[argument name]:[argument description]}`.
3. Clarisse has a good compatibility with PyInstaller. You can set Clarisse as an interface of your command-line program, pack it through PyInstaller and distribute the binary file.

##### Typing

Clarisse choose widgets for arguments based on their types. 

Note that if a type is not supported by Clarisse, it'll use an `ClrsUnknown` type to mark the argument. In that case the value would be shown/edited/passed in `str`.

| argument types | Clarisse widgets   | example                    |
| -------------- | ------------------ | -------------------------- |
| `int`          | spin box           | <img src="./img/arg1.png"> |
| `float`        | spin box for float | <img src="./img/arg2.png"> |
| `str`          | line edit box      | <img src="./img/arg3.png"> |
| `bool`         | check box          | <img src="./img/arg4.png"> |
| `list`         | text edit box      | <img src="./img/arg5.png"> |
| `dict`         | table              | <img src="./img/arg6.png"> |

##### Attention

- if you used `typing.List[a_type,...]` , Clarisse will call a `a_type.__init__(arg_text:str)` to give an `a_type`object to the function, make sure you have appropriate constructor;
- if you used `typing.Dict[key_type,value_type,...]` , Clarisse will call `key_type.__init__(key_text:str)`and `value_type.__init__(value_text:str)` to give an `{key_type:value_type}`dict to the function, make sure you have appropriate constructor.

##### Icons

Clarisse automaticly load icon under the current dir.

For example, if a function named `func()` and is decorated by `@Clarisse()`, Clarisse will try to load `func.ico` from the current dir. 

The icon file could also be chosen by argument:

```python
@Clarisse(icon="<path-to-icon>.ico")
```

this will load the `<path-to-icon>.ico` as the window icon.

##### Single-pass run

Clarisse can be set to run once only.

Set the `single_pass` argument to `True` to tell the GUI to return once the function is finished, like `@Clarisse(single_pass=True)`.

##### Docstring parser

In most cases, Clarisse read the docstring of the function (i.e. `func.__doc__`) and show it as a description of the function. But if you have already written a well-designed docstring, Clarisse can also make full use of it.

Now, if the function has a numpy-style docstring,  Clarisse will take six hyphens(`------`), which is also the splitor in Markdown syntax, as separators between paragraphs. The first paragraph will be treated as the description of the function.

##### Examples

```python
@Clarisse(
    margin=10,
    vert_spacing=10,
    description="""another description. \\
         Note that this description is <font color=#ff0000>prior</font> than \\
         func.\_\_doc\_\_ .""")
def func(arg1,arg2:int,arg3:str="have a try") -> bool:
    """This is only a ***test*** function\\
    but enough to show what clarisse do!"""
    print("arg1 is {0}".format(arg1))
    print(arg3.upper())
    return arg2>10

print(func("this is clarisse output",0))
```

<img src="./img/img2.png" style="zoom : 80%">

```python
@Clarisse(args_desc=("This is arg1","This is arg2, label warps if it is too long"),args_kwdesc={"arg3":"an example to show args_kwdesc"})
def func(arg1,arg2:int,arg3:str="have a try") -> bool:
    """This is only a ***test*** function\\
    but enough to show what clarisse do!"""
    print("arg1 is {0}".format(arg1))
    print(arg3.upper())
    return arg2>10

print(func())
# actually doesn't need parameters when calling,
# but need to be given before Run is clicked.
```

<img src="./img/img3.png" style="zoom : 65%">

```python
@Clarisse(single_pass=True)
def f(this_is_arg1:int,this_is_arg2:str,this_is_arg3:list):
    """
    ...				#<- numpy.ndarray.__doc__
    """
```

<img src="./img/img4.png" style="zoom : 65%">

### Well done, but...

*Why not gooey?*

<a href="https://github.com/chriskiehl/Gooey">Gooey</a> is an outstanding and all-around framework for almost all kinds of python programs, but it

- needs code modifications;
- you have to implement an `ArgumentParser` : sad story for `fire` and `click` users :cry:
- works only for command line entrance;
- ~~I failed to learn it - the doc of gooey is too too much for a non-native speaker like me :sob:~~

Of course I advise you to choose gooey if you're familiar to it and need deep customization, but if you only need a light-weight, pain-less, quick-deployment GUI framework, maybe Clarisse is an alternative!

### I wanna make it better!

You are 24/7 welcome! As an *end-stage hypo-comment-phobia patient*, ~10% of the lines are comments. With those comments one can start easily. I also have plans to write docs to describe the function of each part.

If you bumped into some *insane* codes, please feel free to ask me directly.

If you're not interested in contribute codes to Clarisse, you could also find the entrance for discussion about new feature requests at the *future* paragraph of [patch](./patch.md).

### ...and, Future!

- [ ] There will be more layouts and be available to get changed;
- [ ] QSS(CSS-like) style will be applied for sheets & widgets to make them look better;
- [ ] Clarisse will support classes;
- [ ] And also support more types;

......

### FAQ

- Q: error:`qt.qpa.plugin: Could not load the Qt platform plugin "***" in ...`

  - A: you don't have all the Qt library, or you have but PySide2 failed to find them.

    On Windows, try copy

    ```
    \Anaconda3\Lib\site-packages\PySide2\plugins\platforms\qminimal.dll
    \Anaconda3\Lib\site-packages\PySide2\plugins\platforms\qoffscreen.dll
    \Anaconda3\Lib\site-packages\PySide2\plugins\platforms\qwindows.dll
    ```

    to

    `\Anaconda3\Library\plugins\platforms\`.

    On Linux (tested on Ubuntu 18.04), try `apt install python3-pyqt5`.

- Q: error:`qt.qpa.plugin: Could not find the Qt platform plugin “***“ in ... `

  - A: PyQt5/PySide2 is only the binding between Qt and Python. This error means that Python failed to find the real "worker" (which is Qt plugin for your platform).

    Add below to your code after `import` part:

    ```python
    import PySide2
    import os
    
    dirname = os.path.dirname(PySide2.__file__) 
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    ```

    or write it in a new .py file and import it, anyway make sure it runs before Clarisse is called.

### Acknowledgements

Thanks to the <a href="https://github.com/google/python-fire/">fire</a> library that inspired me the idea;

Thanks to the <a href="https://github.com/google/latexify_py/">latexify_py</a> module that gives me the idea of interface and the lessons of  python syntax analyzing and the usage of  `inspect`;~~hey dude I also contributed to latexify_py that's a really handy module go star it~~

Thanks to <a href="https://www.fanfiction.net/u/1596712/Hieronym">@Hieronym</a>, for the splendid fanfiction *<a href="https://www.fanfiction.net/s/7406866/1/To-the-Stars">To The Stars</a>* ~~the best fanfiction space opera I've ever read~~, which gives the name of this module.



1MLightyears

20201215