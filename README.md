## imchrome [![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

```python
pip install imchrome
```

Easy to use functionalities for using selenium based chrome browser from python.

#### Working

Using selenium is not so difficult, but we always need to deal with number of parameters such as launching the chrome with various options such as:

- headless mode
- fast page loading
- disable image loading
- controlling multiple tabs

Out of all the features mentioned above, the coolest part is to be able to manage multiple tabs, it is difficult to keep track of tabs especially with selenium but don't worry it is going to be fun and easy now.

------

#### Example 1

```python
import imchrome

ic = imchrome.init(headless=False, load_image=True)
page_title, result = ic.get("www.google.com")
print(page_title)
```

#### output

```python
'Google'
```

You will able to see chrome running automatically, if any error occurs consider passing chromedriver path with ``imchrome.init(headless=False, load_image=True, chromdriver='path/to/chromedriver')``

#### Example 2

````python
import imchrome

ic = imchrome.init()
ic.launch_chrome()

print("current active tab:",ic.current_tab())
print("creating new tabs...")
ic.new_tab()
ic.new_tab()
ic.new_tab()
ic.new_tab()

print("all opened tabs:", ic.tab_list())
print("deleting tabs")
ic.delete_tab(1)
ic.delete_tab(2)

print("all opened tabs:", ic.tab_list())
print("switching to another tab")
ic.switch_tab(3)

print("current active tab:",ic.current_tab())
print("quitting chrome")
ic.quit_chrome()
````

#### output

````bash
current active tab: 0
creating new tabs...
all opened tabs: [0,1,2,3,4]
deleting tabs
all opened tabs: [0,3,4]
switching to another tab
current active tab: 3
quitting chrome
````

As you will run the code, new tabs will be created, deleted and changed automatically, do not try to close tabs manually using mouse and the GUI, as it will break the internal data dictionary used to manage tabs. Use python code to create, delete, switch tabs.