from pathlib import Path
import re

try:
    from utils.levenshtein import levenshtein_ratio_and_distance
except:
    from levenshtein import levenshtein_ratio_and_distance
 

path = Path('.')   

def grab_qa_for(quiz="linux"): 
    #quiz = quiz.replace("assessment","")
    
    answer_re   = re.compile('-\s\[x\]\s(.+)')
    question_re = re.compile('#+\sQ\d+\.\s(.+)')
    alt_question_re = re.compile('\d+\.\s(.+)')

    edits = (100,0,0,0)
    
    c_questions = []
    dirty_questions = []
    
    c_answers   = []
    dirty_answers   = []
    
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


    if len(all_files) > 1:
        best_index = 0 
        curr = 0 
        for num, filename in enumerate(all_files, start=0):
            test = levenshtein_ratio_and_distance(quiz,filename.name)
            if num == 0:
                curr = test
            if test < curr and quiz in filename.name:
                best_index = num                
        all_files = [all_files[best_index]]
           

    if len(all_files) == 1:
        file = all_files[0]
        
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

        """
        total_qa = []
        with open(file, 'r') as outfile:
            total_qa = outfile.read().split("###")
            
        for x in total_qa:
            x = str(x.replace("#",""))
            print(x)
            print('--')
            question = alt_question_re.match(x.strip())
            answer   = answer_re.match(x.strip())

            print(question)
            if question and answer:
                clean_q = re.sub(r'[^\w]', '', question.group(1).lower())
                clean_a = re.sub(r'[^\w]', '', answer.group(1).lower())
                
                print(clean_q,clean_a)
        """

            
    return (c_questions, c_answers), (dirty_questions, dirty_answers)

grab_qa_for(quiz="linux")