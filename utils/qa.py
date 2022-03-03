from pathlib import Path
import re

try:
    from utils.levenshtein import levenshtein_ratio_and_distance
except:
    from levenshtein import levenshtein_ratio_and_distance
 

path = Path('.')   

def search_string_in_everything(sstring):
    all_files = path.glob('**/*.md')
    for file in all_files:
        mep = []
        with open(file, 'r') as outfile:
            mep = outfile.readlines()
        for line in mep:
            clean_s = re.sub(r'[^\w]', '', sstring.lower())
            clean_l = re.sub(r'[^\w]', '', line.lower())
            if clean_s in clean_l or clean_s == clean_l:
                return True 
    return False 
             

def grab_qa_for(quiz="linux"): 
    #quiz = quiz.replace("assessment","")
    
    answer_re   = re.compile('-\s\[x\]\s(.+)')
    question_re = re.compile('#+\sQ\d+\.\s(.+)')
    alt_question_re = re.compile(r"\d+\.\s(.+)")

    edits = (100,0,0,0)
    
    c_questions = []
    dirty_questions = []
    
    c_answers   = []
    dirty_answers   = []
    the_file = ""
    
    all_files = [f for f in path.glob('**/*.md') if quiz in str(f)]
    
    if not all_files:
        for child_dir in path.glob('*/'):
            if child_dir.is_dir() and "quizzes" in str(child_dir):
                for file in child_dir.glob('*/'):
                    subdir = str(file).replace(str(file.parent),"").replace("/","")
                    test = levenshtein_ratio_and_distance(quiz,subdir)
                    if edits[0] > int(test):
                        files = [e for e in file.iterdir() if e.is_file()]
                        edits = (test,quiz,file,files)  
                       

        all_files = edits[3]

    if len(all_files) > 1:
        best_index = 0 
        curr = 0 
        for num, filename in enumerate(all_files, start=0):
            test = levenshtein_ratio_and_distance(quiz,filename.name)
            if num == 0:
                curr = test
            if test < curr and quiz in filename.name:
                best_index = num     
                
        the_file = all_files[best_index]           
        all_files = [all_files[best_index]]
        
           

    if len(all_files) == 1:
        file = all_files[0]
        the_file = file
        
        mep = []
        with open(file, 'r') as outfile:
            mep = outfile.readlines()
            
        for line in mep:
            question = question_re.match(line.strip())
            answer   = answer_re.match(line.strip())
        
            if question:
                clean_q = re.sub(r'[^\w]', '', question.group(1).lower())
                c_questions.append(clean_q)
                dirty_questions.append(question.group(1))
                
            if answer:
                clean_a = re.sub(r'[^\w]', '', answer.group(1).lower())
                c_answers.append(clean_a)
                dirty_answers.append(answer.group(1))
                
                
    total_qa = []        
    if the_file:
        with open(the_file, 'r') as outfile:
            total_qa = outfile.read().split("##")
                
        qa_pairs = []
        for question_answer in total_qa:
            question_answer = str(question_answer.replace("#",""))
            qa_lines = question_answer.split("\n")
            
            curr_q = ""
            curr_a = []
            
            for q_line in qa_lines:
                question = alt_question_re.findall(q_line.strip())
                if question:
                    curr_q = re.sub(r'[^\w]', '', question[0].lower())
                    
            for a_line in qa_lines:            
                answer   = answer_re.match(a_line.strip())
                if answer:
                    curr_a.append(re.sub(r'[^\w]', '', answer.group(1).lower()))

            if curr_a and curr_q:
                qa_pairs.append({
                    curr_q : curr_a
                })

    return (c_questions, c_answers), qa_pairs

