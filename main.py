import pandas as pd
from utils import get_unsolved,get_list


unsolved_problems=get_unsolved(handle="Banik1313",contest_type="Div. 2",idx="C")

unsolved = pd.DataFrame(unsolved_problems[0:200])

problem_list = get_list(unsolved,30) 

problem_list.to_csv("unsolved_problems.csv",index=False)
