import requests as rq
import pandas as pd

API_URL = "https://codeforces.com/api/"
WEB_URL = "https://codeforces.com/"


# "https://codeforces.com/api/contest.list"
def get_contests(contest_type="Div. 2"):
    rs = rq.get(f'{API_URL}contest.list')
    all_contests = rs.json()["result"]

    all_contests = sorted(all_contests, reverse=True, key=lambda d: d['startTimeSeconds'])  
    div2_equevalent=set()

    for contest in all_contests:
        if(contest["phase"] == "FINISHED"):
            name = contest["name"]
            if name.find(contest_type) != -1:
                div2_equevalent.add(contest["id"])

    return set(div2_equevalent)


# https://codeforces.com/api/problemset.problems
def get_problems(idx="C",contest_type="Div. 2"):
    rs = rq.get(f'{API_URL}/problemset.problems')
    problems = rs.json()["result"]["problems"]
    contests = get_contests(contest_type)
    c_problems=[]
    for problem in problems:
        contestID = problem["contestId"]
        if (contestID in contests) and problem["index"]==idx:
            c_problems.append(problem)
    return c_problems


#https://codeforces.com/api/user.status?handle=Banik1313
def get_participated_contests(handle="Banik1313"):
    url = f"{API_URL}user.status?handle={handle}"
    rs = rq.get(url)
    submissions = rs.json()["result"]

    contests = set()
    for sub in submissions:
        contests.add(sub["contestId"])
    
    return contests


# https://codeforces.com/api/contest.status?contestId=1932&handle=Banik1313
def get_unsolved(handle="Banik1313",contest_type="Div. 2",idx="C"):
    problems = get_problems(idx,contest_type)
    participated_contests = get_participated_contests(handle)

    unsolved = []

    while(len(problems) > 0):
        skipped=[]
        for problem in problems:
            contestId = problem["contestId"]
            if(contestId not in participated_contests):
                unsolved.append(problem)
                continue

            url = f'{API_URL}contest.status?contestId={contestId}&handle={handle}'
            rs = rq.get(url)
            if(rs.ok):
                solved = rs.json()["result"]
            else:
                print("skipped"," : ",contestId)
                skipped.append(problem)
                continue
            if(len(solved) == 0):
                continue

            isSolved = False
            for sol in solved:
                prob = sol["problem"]
                if prob["name"] == problem["name"]:
                    isSolved=True
                    break
            
            if(not isSolved):
                unsolved.append(problem)

        problems=skipped
    
    return unsolved

def get_list(problems:pd.DataFrame,problem_num=50):
    problems.drop("type", axis=1, inplace=True)
    problems.drop("points", axis=1, inplace=True)
    problems.sort_values(by=["rating"], ascending=False, inplace=True)
    problems = problems.head(problem_num)

    problem_urls= []
    for index,row in problems.iterrows():
        contestId=row["contestId"]
        idx=row["index"]

        problem_url = gen_url(contestId,idx)
        problem_urls.append(problem_url)

    problems.insert(4,"Problem_url",problem_urls,True)

    problems.drop("rating", axis=1, inplace=True)
    problems.drop("index", axis=1, inplace=True)

    problems = problems.sample(frac=1).reset_index(drop=True)
    
    return problems


# https://codeforces.com/contest/593/problem/C
def gen_url(contestId,idx="C"):
    url = f'{WEB_URL}contest/{contestId}/problem/{idx}'

    return url