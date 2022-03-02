import traceback
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions as sel_exceptions

DEFAULT_MAX_TIMEOUT = 30 
DEFAULT_PAGE_WAIT_DELAY = 0.5  # also serves as minimum wait for randomized delays
DEFAULT_MAX_PAGE_WAIT_DELAY = 1.0  # used for random page wait delay

def strtobool (val):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    if isinstance(val, bool):
        return val 
     
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1', 'True'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0', 'False'):
        return 0
    elif val in ('None', None, 'none'):
        return None 
    else:
        raise ValueError("invalid truth value %r" % (val,))
    
def none_or_floatval(val):
    str_val = str(val)
    if str_val == "-" or "nan" in str_val.lower():
        return None 

    if str_val.lower() != "none" and val != None and "Infinity" not in str_val:
        if "%" in str_val:
            str_val = str_val.replace("%","")
        if "." in str_val and "," in str_val:
            str_val = str_val.replace(".", "").replace(",", ".")
        if "," in str_val and "." not in str_val:
            str_val = str_val.replace(",", ".")

        return float(str_val)
    else:
        return None 
    
def nice_error(error : Exception):    
    traceback_k = error.__traceback__
    stack_summary = traceback.StackSummary.extract(traceback.walk_tb(traceback_k))
    
    errlist = []
    lasterr = {}
    for frame_summary in stack_summary:
        lasterr = {
            "filename" : frame_summary.filename,
            "function" : frame_summary.name,
            "line"     : frame_summary.lineno,
            "easy"     : f'"{frame_summary.filename}", line {frame_summary.lineno}',
            "full"     : traceback.format_exc(),
        }
        errlist.append(lasterr)

    return lasterr, errlist

def str_to_bool(s):
    """If unsure if the value is a string or whatever always use this utillity method.

    Args:
        s (unkown): Pass anything, it'll convert to bool.

    Raises:
        ValueError: If for whatever reason none of the checks work, it'll return error.

    Returns:
        [bool]: Returns the boolean equivalent fo whatever you passed
    """
    s = str(s)
    if s.lower() == 'true':
         return True
    elif s.lower() == 'false':
         return False
    elif s == "0":
        return False 
    elif s == '':
        return False
    elif s == "1":
        return True
    elif s.lower() == "none":
        return False
    elif s == None:
        return False
    else:
         raise ValueError 
     
     
def webdriver_wait_until(driver):
    # TODO: Really cool way to wait for something in browser to happen 
    # TODO add screenshot of element, send to telegram, have user solve, and send back to this 
    
    # Maybe/Probably/Likely a One Time Password prompt?  Let's wait until the user takes action
    #self.notification_handler.play_alarm_sound()
    print("One Time Password input required... pausing for user input")
    try:
        WebDriverWait(driver, timeout=300).until(
            lambda d: "/ap/" not in d.driver.current_url
        )
    except sel_exceptions.TimeoutException:
        print("User did not solve One Time Password prompt in time.")    


def get_timeout(self, timeout=DEFAULT_MAX_TIMEOUT):
    return time.time() + timeout


# decorator to wait until
def wait_until(driver, seconds=0, jquery="", js="", url="", title="", text="", button="",page_loaded=False ,max_wait=30):
    """Decorator to wait on something to happen. Example: 
    wait until a certain jquery can be executed correctly or wait until a button is visibile. 

    Args:
        driver (WebDriver) : Selenium WebDriver
        func (function): the function 
        seconds (int, optional): [description]. Defaults to 0.
        jquery (str, optional): [description]. Defaults to "".
        js (str, optional): [description]. Defaults to "".
        url (str, optional): [description]. Defaults to "".
        title (str, optional): [description]. Defaults to "".
        text (str, optional): [description]. Defaults to "".
        button (str, optional): [description]. Defaults to "".
        link (str, optional): [description]. Defaults to "".
    """
    def sleeper(timer):
        time.sleep(timer)
        return timer

    if page_loaded:
        timer = 0 
        is_page_loaded = False
        while not is_page_loaded and timer < max_wait:
            is_page_loaded = driver.execute_script('return document.readyState;')
            if is_page_loaded == "complete":
                return True 
            timer += sleeper(1)
        raise TimeoutError(f'Max wait of {max_wait} seconds, exceeded.')
        

    if seconds:
        # wait for 'seconds' till continue 
        time.sleep(seconds)
        return True 
        
    if jquery:
        # wait till 'jquery' was executed succesfully 
        is_on_page = False
        timer = 0 
        while not is_on_page and timer < max_wait:
            is_on_page = driver.execute_script("return " + jquery)
            if is_on_page:
                return True 
            timer += sleeper(1)
        
        raise TimeoutError(f'Max wait of {max_wait} seconds, exceeded.')

            
    if js:
        # wait till 'js' was executed succesfully 
        is_on_page = False
        timer = 0 
        while not is_on_page and timer < max_wait:
            is_on_page = driver.execute_script('return ' + js)
            if is_on_page:
                return True 
            timer += sleeper(1)
        
        raise TimeoutError(f'Max wait of {max_wait} seconds, exceeded.')


    if url:
        # wait till certain 'url' is the current url or if part of the url is 'url'
        # - for example you can pass "login", if "login" is in url then continue 
        is_new_page = False
        is_current_page = False
        timer = 0 
        if url.startswith("not_"):
            url = url.split("not_")[1]
            while not is_new_page and timer < max_wait:
                if url not in driver.current_url:
                    is_new_page = True
                timer += sleeper(1)
        else:
            while not is_current_page and timer < max_wait:
                    if url in driver.current_url:
                        is_current_page = True
                    timer += sleeper(1)

        if is_new_page or is_current_page:
            return True 
        else:
            raise TimeoutError(f'Max wait of {max_wait} seconds, exceeded.')

    if title:
        # if the title of the website is "title" or includes "title"
        is_new_title = False
        is_current_title = False
        timer = 0 
        if title.startswith("not_"):
            title = title.split("not_")[1]
            while not is_new_title and timer < max_wait:
                if title not in driver.title:
                    is_new_title = True
                timer += sleeper(1)
        else:
            while not is_current_title and timer < max_wait:
                    if title in driver.title:
                        is_current_title = True
                    timer += sleeper(1)
                    
        if is_new_title or is_current_title:
            return True 
        else:
            raise TimeoutError(f'Max wait of {max_wait} seconds, exceeded.')


    if text:
        # is visible on page, this has to be an exact match 
        is_text_on_page = False
        timer = 0 
        while not is_text_on_page and timer < max_wait:
            try:
                try:
                    is_text_on_page = driver.execute_script(f"return (document.documentElement.textContent || document.documentElement.innerText).indexOf('{text}') > -1")
                except Exception as e:
                    is_text_on_page = driver.execute_script(f"return document.body.innerHTML.search('{text}') > -1")
            except Exception as e:
                if text in driver.page_source:
                    is_text_on_page = True    
            timer += sleeper(1)
            
        if is_text_on_page:
            return True 
        else:
            raise TimeoutError(f'Max wait of {max_wait} seconds, exceeded.')    
        
    if button:
        # check if button is visible on page 
        is_on_page = False
        timer = 0 
        while not is_on_page and timer < max_wait:
            if button.startswith("css_"):
                button_css_selector = button.split("css_")[1]
                try:
                    is_on_page = driver.find_element(By.CSS_SELECTOR, button_css_selector)
                except Exception as e:
                    is_on_page = driver.find_element_by_css_selector(button_css_selector)
                    
            elif button.startswith("xpath_"):
                button_xpath_selector = button.split("xpath_")[1]
                try:
                    #driver.find_element(By.XPATH, "//*[contains(text(), 'My Button')]")
                    is_on_page = driver.find_element(By.XPATH, button_xpath_selector)
                except Exception as e:  
                    is_on_page = driver.find_element_by_xpath(button_xpath_selector)
            else:
                is_on_page = driver.execute_script(button)
            
            timer += sleeper(1)
            
        if is_on_page:
            return True 
        else:
            raise TimeoutError(f'Max wait of {max_wait} seconds, exceeded.')    



    
        
        
def anti_anti_bot(driver):
    # attempts to detect itself as a bot 
    # https://github.com/backdrop-contrib/antibot
    # https://github.com/OXDBXKXO/akamai-toolkit
    # https://github.com/ultrafunkamsterdam/undetected-chromedriver
    # detects if using webdriver like chromium
    is_webdriver = driver.execute_script("return navigator.webdriver")
    
    # navigator.userAgent
    ua = driver.execute_script("return navigator.userAgent")
    


def page_wait_delay():
    return DEFAULT_PAGE_WAIT_DELAY
    
def wait_for_element(driver):
    from selenium.common import exceptions as sel_exceptions
    timeout = get_timeout()
    while True:
        try:
            email_field = driver.find_element_by_xpath('//*[@id="ap_email"]')
            break
        except sel_exceptions.NoSuchElementException:
            try:
                password_field = driver.find_element_by_xpath(
                    '//*[@id="ap_password"]'
                )
                break
            except sel_exceptions.NoSuchElementException:
                pass
        if time.time() > timeout:
            break