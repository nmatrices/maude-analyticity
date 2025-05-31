# An script to explore some branches of the search tree in parallel
# for some logics that may create an important number of cases (as KD, K4). 

import maude
import multiprocessing
import importlib
import argparse


def check(t, num):
    #maude = importlib.import_module('maude')
    #maude.init()
    #maude.load('KD')
    LOGIC = maude.getModule('CHECK-ANALITICITY-BOX')
    strat = LOGIC.parseStrategy("depC ; depA ; guess ! ; value' ! ; guess ! ; ignore ; (match no-case ? fail : idle) ; one(simplify) ! ; check") 
    for x,_ in t.srewrite(strat,depth=True):
        print(f'{num} : {x}')

    print(f'DONE({num})')

def main():
    parser = argparse.ArgumentParser(description="Checking in parallel the correctness of extensions")
    parser.add_argument("--module", help="Maude file with the description of the logic (e.g., K4)")
    args = parser.parse_args()


    maude.init()

    maude.load(f'{args.module}')
    LOGIC = maude.getModule('CHECK-ANALITICITY-BOX')
    procs = []
    strat = LOGIC.parseStrategy('guess !')
    t = LOGIC.parseTerm('initBox')

    for x,i in t.srewrite(strat, depth=True):
        procs.append(multiprocessing.Process(target=check, args=(x, i )))

    for p in procs:
        p.start()

    for p in procs:
        p.join()


if __name__ == '__main__':
    main()
