# An script to explore some branches of the search tree in parallel
# for some logics that may create an important number of cases (as KD). 

import maude
import multiprocessing
import importlib


def check(t, num):
    #maude = importlib.import_module('maude')
    #maude.init()
    #maude.load('KD')
    KD = maude.getModule('CHECK-ANALITICITY-BOX')
    strat = KD.parseStrategy("depC ; depA ; guess ! ; value' ! ; guess ! ; one(simplify) ! ; check")
    for x,_ in t.srewrite(strat,depth=True):
        print(f'{num} : {x}')

    print(f'DONE({num})')


if __name__ == '__main__':
    #multiprocessing.set_start_method('spawn')
    maude.init()
    maude.load('KD')
    KD = maude.getModule('CHECK-ANALITICITY-BOX')
    procs = []
    strat = KD.parseStrategy('guess !')
    t = KD.parseTerm('initBox')

    for x,i in t.srewrite(strat, depth=True):
        procs.append(multiprocessing.Process(target=check, args=(x, i )))

    for p in procs:
        p.start()

    for p in procs:
        p.join()

