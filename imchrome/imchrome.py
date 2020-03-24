from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import os
import sys

class ImChrome():

    def __init__(self, **kwargs):
        # download chromedriver for your platform
        # https://chromedriver.chromium.org/downloads
        if sys.platform.lower() == "linux" or sys.platform.lower() == "linux2":
            self.chromedriver = "chromedriver/linux64/chromedriver"
        elif sys.platform.lower() == "win32":
            self.chromedriver = "chromedriver/win32/chromedriver.exe"
        elif sys.platform.lower() == "darwin":
            self.chromedriver = "chromedriver/mac64/chromedriver"

        self.chrome_options = Options()
        self.caps = DesiredCapabilities().CHROME
        self.tab_dict = {}
        self._driver = None
        self.status = 'Chrome Not Initialized'

        #if any argument is passed to constructor then: call launch_chrome function with those arguments
        #else don't call launch_chrome function
        if len(kwargs) != 0:
            #chromedriver=None, headless=False, chrome_options=None, mode='normal', load_image=True
            chromedriver = kwargs['chromedriver'] if 'chromedriver' in kwargs else None
            headless = kwargs['headless'] if 'headless' in kwargs else False
            chrome_options = kwargs['chrome_options'] if 'chrome_options' in kwargs else None
            mode = kwargs['mode'] if 'mode' in kwargs else 'normal'
            load_image = kwargs['load_image'] if 'load_image' in kwargs else True

            #automatically launch chrome at class initilization
            self.launch_chrome(chromedriver=chromedriver, headless=headless, chrome_options=chrome_options, mode=mode, load_image=load_image)


    def launch_chrome(self, chromedriver=None, headless=False, chrome_options=None, mode='normal', load_image=True):
        try:
            status = {}
            status["headless"] = headless
            status["load_image"] = load_image

            self.caps["pageLoadStrategy"] = mode #"normal", "eager", "none"
            status["capability"] = self.caps

            if chromedriver == None:
                chromedriver = self.chromedriver

            if chrome_options == None:
                chrome_options = self.chrome_options

            if headless == True:
                self.chrome_options.add_argument("--headless")
                self.chrome_options.add_argument("--window-size=1920x1080")
                status["headless"] = True

            if load_image == False:
                chrome_prefs = {}
                self.chrome_options.experimental_options["prefs"] = chrome_prefs
                chrome_prefs["profile.default_content_settings"] = {"images": 2}
                chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
                status["load_image"] = False

            status["chromedriver"] = chromedriver
            status["chrome_running"] = True
            self.status = status

            _driver = webdriver.Chrome(desired_capabilities=self.caps, options=chrome_options, executable_path=chromedriver)
            self._driver = _driver
            self.tab_dict[-1] = _driver.window_handles[0]

            html_content = """
            <html>
                 <head>
                     <title>Don't close this tab</title>
                 </head>
                 <body>
                     <div id="warn">
                         Do not close this tab.
                     </div>
                 </body>
            </html>
            """
            self.driver.get("data:text/html;charset=utf-8," + html_content)

            self.new_tab(0)
            return self
        except Exception as e:
            print(e)
            return e


    @property
    def driver(self):
        if not self.status["chrome_running"]: return "chrome not running"
        try:
            return self._driver
        except Exception as e:
            print(e)
            return e


    def quit_chrome(self):
        try:
            if self.status["chrome_running"]:
                self.driver.quit()
                self.status["chrome_running"] = False
                return 'success'
            else:
                return 'already closed'
        except Exception as e:
            print(e)
            return e


    def new_tab(self, idx=None):
        if not self.status["chrome_running"]: return "chrome not running"
        try:
            tab_dict = self.tab_dict
            driver = self.driver

            #if idx is not provided increment new index
            if idx == None: idx = max(tab_dict.keys())+1

            #if any tab with given index is already created
            #we need to delete that tab
            if idx in tab_dict.keys():
                #print("deleting tab:", idx, tab_dict[idx])
                driver.switch_to.window(tab_dict[idx])
                driver.close()
                driver.switch_to.window(tab_dict[-1])

            #create new tab
            driver.execute_script("window.open('');")
            tab_dict[idx] = driver.window_handles[-1]
            #print("created tab:", idx, tab_dict[idx])

            #switch to newly created tab
            #print("switching tab:", idx, tab_dict[idx])
            driver.switch_to.window(tab_dict[idx])

            #sorting tab_dict for convenience
            tab_dict = dict(sorted(tab_dict.items()))

            return self.current_tab()
        except Exception as e:
            print(e)
            return e


    def current_tab(self):
        if not self.status["chrome_running"]: return "chrome not running"
        try:
            val = self.driver.current_window_handle
            for key, value in self.tab_dict.items():
                if val == value:
                    return key
            raise ValueError(val)
        except Exception as e:
            print(e)
            return e


    def switch_tab(self, idx=None):
        if not self.status["chrome_running"]: return "chrome not running"
        try:
            current_tab = self.current_tab
            driver = self.driver
            tab_dict = self.tab_dict

            if idx in ['next', 'n', '+']:
                idx = list(filter(lambda i: i>current_tab(), sorted(tab_dict)))
                idx = idx[0] if len(idx)>=1 else -1

            elif idx in ['previous', 'prev', 'p', '-']:
                idx = list(filter(lambda i: i<current_tab(), sorted(tab_dict)))
                idx = idx[-1] if len(idx)>=1 else -1

            if idx < 0: raise KeyError(idx)

            #check if given index exists
            if idx in tab_dict:
                driver.switch_to.window(tab_dict[idx])
                return idx
            else:
                raise KeyError(idx)
        except Exception as e:
            print(e)
            return current_tab()


    def delete_tab(self, idx=None):
        if not self.status["chrome_running"]: return "chrome not running"
        try:
            current_tab = self.current_tab
            tab_dict = self.tab_dict
            switch_tab = self.switch_tab
            driver = self.driver

            #if idx is not provided get current tab's index
            if idx == None: idx = current_tab()

            #check if given index exists
            if idx in tab_dict and idx>0:
                #print("deleting:", idx, tab_dict[idx])

                #just to make sure we are on the current tab
                switch_tab(idx)

                #first try to switch to previous tab to make sure
                #falling back to previous tab is possible
                #before deleting current tab
                prev_tab = switch_tab('p')

                #again switch to the given input tab to delete it
                switch_tab(idx)
                driver.close()
                del tab_dict[idx]

                #fall back to previous tab after deleting given tab
                switch_tab(prev_tab)

                #sorting tab_dict for convenience
                tab_dict = dict(sorted(tab_dict.items()))
                return idx

            else:
                raise KeyError(idx)
        except Exception as e:
            print(e)
            if idx == 0: self.new_tab(0)
            return current_tab()


    def get(self, url, tab_num=None):
        if not self.status["chrome_running"]: return "chrome not running"
        if tab_num == None: tab_num = self.current_tab()
        assert self.tab_exist(int(tab_num)), "tab {} doesn't exists".format(tab_num)
        try:
            if tab_num < 0: raise KeyError(tab_num)
            self.driver.switch_to.window(self.tab_dict[tab_num])
            if not url.startswith("http"): url = "http://"+url
            self.driver.get(url)
            return self.driver.title, self.driver
        except Exception as e:
            print(e)
            return e, self.driver


    def tab_exist(self, key):
        if not self.status["chrome_running"]: return "chrome not running"
        if key in self.tab_dict:
            return True
        return False


    def tab_list(self):
        if not self.status["chrome_running"]: return "chrome not running"
        return sorted(self.tab_dict)[1:]


    def sleep(self, sec):
        time.sleep(sec)


    def imwrite(self, path, element):
        if not self.status["chrome_running"]: return "chrome not running"
        try:
            with open(path, "wb") as f:
                f.write(element.screenshot_as_png)
        except Exception as e:
            print(e)
