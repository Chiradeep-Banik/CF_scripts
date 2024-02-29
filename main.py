#! env/bin/python3.11
import pandas as pd
import sys
from utils import get_unsolved,get_list

no_of_questions = 30
if(len(sys.argv) > 1):
    no_of_questions=int(sys.argv[1])

unsolved_problems=get_unsolved(handle="Banik1313",contest_type="Div. 2",idx="C")

unsolved = pd.DataFrame(unsolved_problems[0:200])

problem_list = get_list(unsolved,no_of_questions)

problem_list.to_csv("unsolved_problems.csv",index=False)

