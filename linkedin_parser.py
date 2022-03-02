import time
import logging
import sys
import argparse
from decouple import config
import urllib.parse
import re
from utils.qa import grab_qa_for
from utils.browser_opts import browser_options
from utils.utillities import wait_until, strtobool

my_parser = argparse.ArgumentParser()
my_parser.add_argument('-s', '--show',
                    action='store_true',
                    help='Show browser. Default is headless.')
my_parser.add_argument('-l', '--live',
                    action='store_true',
                    help='Run real test, not just practice.')

options = my_parser.parse_args()
options = vars(options)


LINKED_IN_USER    = config('LINKED_IN_USER')
LINKED_IN_PASS    = config('LINKED_IN_PASS')
LINKED_IN_PROFILE = config('LINKED_IN_PROFILE')
QUESTION_COUNT    = 15
EXAM_NAME         = "" 



def main():
    driver = browser_options(options)
    if EXAM_NAME:
        clean_qa, dirty_qa = grab_qa_for(quiz=EXAM_NAME)
        if clean_qa[0]:
            login(driver)
            wait_until(driver, page_loaded=True)
            #run_single(EXAM_NAME)
    else:
        login(driver)
        wait_until(driver, page_loaded=True)
        run_all(driver)





def run_all(driver):
    on_page = to_quiz_page(driver)
    
    if not on_page:
        return False 
    
    exam_list = get_all_test(driver)

    for exam in exam_list:
        exam_s = urllib.parse.quote(exam)
        exam_link = f"https://www.linkedin.com/skill-assessments/{exam_s}/quiz-intro/"
       
        selected_qa = 0
        exam = exam.replace("assessment","").replace("microsoft","").strip()

            
        l = exam.split(" ")
        clean_qa, dirty_qa = grab_qa_for(quiz=exam)
        if not clean_qa[0]:
            for x in l:
                clean_qa,dirty_qa = grab_qa_for(quiz=x.replace("(","").replace(")",""))
                if clean_qa[0]:
                    selected_qa = clean_qa
        else:
            selected_qa = clean_qa
            
        if selected_qa:        
            driver.get(exam_link)
            wait_until(driver, page_loaded=True)
            wait_until(driver, page_loaded=True)
            
            time.sleep(3)
            if "quiz-intro" in driver.current_url:
                if options.get("live"):
                    driver.execute_script("""document.querySelector("button[title='Start']").click()""")
                else:
                    driver.execute_script("""document.querySelector("button[title='Practice']").click()""")
                    time.sleep(2)
                    driver.execute_script("""Array.from(document.querySelectorAll('button')).find(el => el.innerText === 'Next').click()""")

                wait_until(driver, page_loaded=True)
                wait_until(driver, page_loaded=True)
                time.sleep(2)
                # handles our exam taking 
                during_the_exam(exam, driver,selected_qa)

                # after exam go back to profile
                # maybe we add more here we wanna do after 
                #result, score = after_exam()


"""
def run_single(exam_name,driver):
    # basic usage

    to_quiz_page(driver)

    # has to run so we get all the tests visible
    options_list = get_all_test(driver)

    # pick exam to take - leave blank for all
    pick_and_go(exam_name,options_list)

    # handles our exam taking 
    during_the_exam(exam_name)

    # after exam go back to profile
    # maybe we add more here we wanna do after 
    result, score = after_exam()
"""


def login(driver):
    try:
        driver.get("https://www.linkedin.com/login")
        wait_until(driver, page_loaded=True)
    except Exception as e:
        logging.critical("login page could not be loaded " + str(e)) 
        sys.exit()

    wait_until(driver, page_loaded=True)
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")

    username.send_keys(LINKED_IN_USER)
    password.send_keys(LINKED_IN_PASS)
    
    wait_until(driver, page_loaded=True)
    #wait_until(
    #    driver=driver,
    #    jquery=f'$("#username").val() == "{LINKED_IN_USER}" && $("#password").val() == "{LINKED_IN_PASS}"'
    #)
    time.sleep(3)
    driver.find_element_by_css_selector(".btn__primary--large").click()
    wait_until(driver, page_loaded=True)
    wait_until(driver, js='document.querySelector("#global-nav-typeahead").id.length > 0')

    change_lang(driver)


def change_lang(driver):
    driver.get(LINKED_IN_PROFILE)
    wait_until(driver, page_loaded=True)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script('''
        var languages = document.querySelector("#globalfooter-select_language")
        for(var i = 0; i < languages.length; i++){
            if (languages[i].value === "en_US"){
                languages.value = "en_US"; 
                languages.lang  = "en_US";
                languages.dispatchEvent(new Event('change'));
            };
        };
    ''')
    wait_until(driver, page_loaded=True)
    wait_until(driver, page_loaded=True)
    
    
def to_quiz_page(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.get("https://www.linkedin.com/skill-assessments/hub/quizzes/")
    wait_until(driver, page_loaded=True)
    wait_until(driver, page_loaded=True)
    time.sleep(2)

    try:
        is_skill_page = strtobool(driver.execute_script('return document.querySelector("header > div > h2").innerText === "Skill Assessments"'))
        if is_skill_page:
            return True 
        else:
            driver.get("https://www.linkedin.com/skill-assessments/hub/quizzes/")
            wait_until(driver, page_loaded=True)    
            is_skill_page = strtobool(driver.execute_script('return document.querySelector("header > div > h2").innerText === "Skill Assessments"'))
            if is_skill_page:
                return True          
            else:
                return False 
    except Exception as e:
        print(e)
        pass
    
    
def get_all_test(driver):
    for _ in range(0,6):
        # scroll down to "Show more assesments"
        driver.execute_script('var buttons = document.querySelectorAll("button");for (var i = 0; i < buttons.length; i++){if(buttons[i].innerText.includes("more")){buttons[i].scrollIntoView();};};')
        time.sleep(2)
        # show more 
        driver.execute_script('document.querySelector(".pv-detail-assessments__pager-row > button").click()')
        time.sleep(2)

    return driver.execute_script('return (function assesments(){var l=[];document.querySelectorAll(".pv-assessment-item__title").forEach((e)=>{l.push(e.innerText.toLowerCase())});return l})()')


def during_the_exam(exam_name, driver, selected_qa):
    
    still_questions = True
    counter = 0
    while still_questions:
        wait_until(driver, page_loaded=True)
        wait_until(driver, page_loaded=True)
        time.sleep(4)
        
        try:
            question_heading = driver.execute_script('return document.querySelector("h3").innerText')
        except Exception as e:
            print(e)
            question_heading = exam_name
            
        try:
            asessment_name  = driver.execute_script('return document.querySelector("h3").innerText.split(" Q")[0]')
        except Exception as e:
            print(e)
            asessment_name = exam_name
            
        try:
            try:
                question_number = driver.execute_script("return document.querySelector('h3').innerText.split(' Q')[1].split('/')[0]")
            except Exception as e:
                print(e)
                try:
                    question_number = driver.execute_script('return document.querySelector("span.t-16").innerText.replace("Q","").split("/")[0]')
                except Exception as e:
                    print(e)
                    question_number = driver.execute_script('return document.querySelector("footer > div > div > span").innerText.replace("Q","").split("/")[0]')
        except Exception as e:
            print(e)
            counter += 1
            question_number = counter
            
        try:
            try:
                question_text = driver.execute_script("return document.querySelector('#assessment-a11y-title > span').children.length > 1 ? document.querySelector('#assessment-a11y-title > span > span').innerText : document.querySelector('#assessment-a11y-title > span').innerText")
                if not question_text:
                    try:
                        question_text = driver.execute_script('return document.querySelector("section > p").innerText.split("\n")[0]') 
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
                question_text = driver.execute_script('return document.querySelector("section > p").innerText.split("\\n")[0]')
        
            still_questions = question_text
        except Exception:
            still_questions = False
            return 
                
        try:
            answers_list = driver.execute_script("""return (function answers(){var l=[];document.querySelectorAll("p[id^=skill-assessment]").forEach((e)=>{l.push(e.querySelector("span[aria-hidden]").innerText)});return l})();""")
        except Exception as e:
            try:
                answers_list = driver.execute_script("""return (function answers(){var l=[];document.querySelectorAll("p[id^=skill-assessment]").forEach((e)=>{l.push(e.querySelector("span").innerText.split("\n")[0])});return l})()""")
            except Exception as e:
                try:
                    answers_list = driver.execute_script("""return (function answers(){var l=[];document.querySelectorAll("div > ul > li").forEach((e)=>{l.push(e.innerText.split("\n")[0])});return l})()""")
                except Exception as e:
                    print(e)
                    
        try:         
            time_left = driver.execute_script('return document.querySelector("footer > div > div > span > div").innerText')
        except Exception as e:
            print(e)  
        
        found = False
        for question in selected_qa[0]:
            clean_q = re.sub(r'[^\w]', '', question_text.lower())
            if question == clean_q:
                print("We found the question:")
                print(question)
                print("------------------------")
                found = True 
                
        if not found:
            print("We dont have that question:")
            print(question)
            print("------------------------")
        else:
            found = False
    
        pick_answers = []    
        for answer in selected_qa[1]:
            for i,ans in enumerate(answers_list, start=0):
                clean_a = re.sub(r'[^\w]', '', ans.lower())
                if answer == clean_a:
                    pick_answers.append((i,answer))

    
        # make better random answer if multiple choice 
        if not pick_answers:
            driver.execute_script('document.querySelectorAll("p[id^=skill-assessment]")['+str(1)+'].click()')
            time.sleep(2)
            print("We do not have answers:")
            print(answers_list)
            print("------------------------")
        else:
            print("We found the answer/s:")
            print(pick_answers)
            print("------------------------")
                
        # pick answers
        # TODO: if multiple answers this will fail
        # we have to do a better search see qa.py for startingpoitn
        if len(pick_answers) > 1:
            pick_answers = [pick_answers[0]]
            
        for i in pick_answers:
            driver.execute_script('document.querySelectorAll("p[id^=skill-assessment]")['+str(i[0])+'].click()')
            time.sleep(2)

        try:
            next_button = driver.execute_script("Array.from(document.querySelectorAll('button')).find(el => el.innerText === 'Next').click();")
        except Exception as e:
            print(e)
            next_button = driver.execute_script('document.querySelector("footer").querySelector("button").click()')






"""

def pick_and_go(exam_name,options_list):

    if exam_name in options_list:
        driver.execute_script('''
            var availableTests = []
            var buttons = document.querySelectorAll('button > span.visually-hidden');
            for (var i = 0; i < buttons.length; i++){
                var btnTxt = buttons[i].innerText.trim();
                var btnArr = btnTxt.split(' ');
                btnArr.shift();
                btnArr.shift();
                var cleanArr = btnArr;
                btnTxt = cleanArr.join(',');
                btnTxt = btnTxt.replace(/,/g, ' ');
                availableTests.push(btnTxt);''' + "if (btnTxt.toLowerCase() === '"+exam_name.lower()+"') {buttons[i].click();};};")
    
        if exam_name:
            logging.info('Attempting to take: '+exam_name)
        else:
            logging.warning('Trying to start all exams..DANGERZONE')
    else:
        time.sleep(1)
        if len(options_list) > 0:
            exam_name = options_list[0] # -> exam is the first in the available list 
            driver.execute_script('''
                var availableTests = []
                var buttons = document.querySelectorAll('button > span.visually-hidden');
                for (var i = 0; i < buttons.length; i++){
                    var btnTxt = buttons[i].innerText.trim();
                    var btnArr = btnTxt.split(' ');
                    btnArr.shift();
                    btnArr.shift();
                    var cleanArr = btnArr;
                    btnTxt = cleanArr.join(',');
                    btnTxt = btnTxt.replace(/,/g, ' ');
                    availableTests.push(btnTxt);''' + "if (btnTxt.toLowerCase() === '"+exam_name.lower()+"') {buttons[i].click();};};")
        
                
            if exam_name:
                logging.info('Attempting to take: '+exam_name)
            else:
                logging.warning('Trying to start all exams..DANGERZONE')

        else:
            print("We did all exams. Bye")
            sys.exit()

        time.sleep(1)
        logging.info('Selected Exam: '+exam_name)
                
        time.sleep(2)
        driver.execute_script(''' 
            (function (el) {
                var buttons = document.querySelectorAll('button');
                for (var i = 0; i < buttons.length; i++){
                    var btnTxt = buttons[i].innerText.trim();
                    if (btnTxt.toLowerCase() === el.toLowerCase()) {
                        buttons[i].click()
                    };};}'''+ "('Start'));")
        logging.info('Starting Exam: '+exam_name)
        time.sleep(2)

        print("The choice:{0} is not available.".format(exam_name))
        logging.error(exam_name+' is not a valid exam name.')
        print('Here is a list of choices')
        for x in options_list:
            print(str(x))


def after_exam():
    time.sleep(8)
    # when you actrually pass an exam make this return score
    # we only know the selectors when not passed
    result = driver.execute_script("var result = document.querySelector('section > div > h3').innerText;return result;")
    score = driver.execute_script("var score = document.querySelector('section > div > p').innerText;return score;")

    logging.info('Test is done, going back to profile')
    time.sleep(1)
    driver.execute_script('''
        var buttons = document.querySelectorAll('button');
        for (var i = 0; i < buttons.length; i++){'''+"if(buttons[i].innerText.includes('Profile')){buttons[i].click();};};")

    print(result)
    print(score)

    return result,score

"""



if __name__ == '__main__':
    try:
        main()
    except:
        time.sleep(120)