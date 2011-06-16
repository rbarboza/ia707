#!/usr/bin/env python

"""
SYNOPSIS

    %prog [-v] [-t win_more_pontuation] [-r win_pontuation] [-p lose_pontuation] [-s lose_more_pontuation] strategy_a strategy_b

DESCRIPTION

    TODO This describes how to use this script.
    This docstring will be printed by the script if there is an error or
    if the user requests help (-h or --help).

EXAMPLES

    %prog 1010101010000101010100101110101011010101010010101010100101010011001011 0010101010100101010100110010010010101001011010010100101010100100101001
    TODO: Show more examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    Roberto Barboza Jr <rbarboza@gmail.com>

LICENSE

    This script is in the public domain.

VERSION

    
"""

import sys
import os
import traceback
import optparse
import time
from itertools import combinations_with_replacement

def evaluate_play(a_play, b_play):
    if a_play == '0' and b_play == '0':
        return (options.win,options.win)
    if a_play == '1' and b_play == '0':
        return (options.win_more,options.lose_more)
    if a_play == '0' and b_play == '1':
        return (options.lose_more,options.win_more)
    if a_play == '1' and b_play == '1':
        return (options.lose,options.lose)

def strategy_execution(strat):
    return strat['strategy'][int(strat['memory'],2)]

def update_memory(strat, my_play, its_play):
    strat['memory'] = strat['memory'][2:]+my_play+its_play

def i_wanna_play_a_game(a_strat_string, b_strat_string):

    strat_a = {'memory':a_strat_string[:6], 'strategy':a_strat_string[6:]}
    strat_b = {'memory':b_strat_string[:6], 'strategy':b_strat_string[6:]}

    cycle_detect_struct = []

    total_score_a = 0
    total_score_b = 0
    while True:
        a_play = strategy_execution(strat_a)
        b_play = strategy_execution(strat_b)

        if (not strat_a['memory'] in cycle_detect_struct) or len(cycle_detect_struct) < 3:
            cycle_detect_struct.append(strat_a['memory'])
        else:
            break

        current_score_a, current_score_b = evaluate_play(a_play, b_play)
        total_score_a += current_score_a
        total_score_b += current_score_b

        update_memory(strat_a, a_play, b_play)
        update_memory(strat_b, b_play, a_play)

    return float(total_score_a)/len(cycle_detect_struct), float(total_score_b)/len(cycle_detect_struct)

def main ():

    global options, args

    if options.mode == 'a':
        a_score, b_score = i_wanna_play_a_game(args[0], args[1])
        print 'Strategy[0] score: ' + a_score
        print 'Strategy[1] score: ' + b_score

    elif options.mode == 'b':
        avg_score = [0 for strat in args]
        for strat_a, strat_b in combinations_with_replacement(range(len(args)), 2):
            a_score, b_score = i_wanna_play_a_game(args[strat_a], args[strat_b])
            avg_score[strat_a] += a_score
            avg_score[strat_b] += b_score

            print 'Strategy[%d] score: %d'%(strat_a, a_score)
            print 'Strategy[%d] score: %d'%(strat_b, b_score)

        for i, score in enumerate(avg_score):
            print i, score/len(avg_score)


if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(
                formatter=optparse.TitledHelpFormatter(),
                usage=globals()['__doc__'],
                version='%prog v0.1')
        parser.add_option ('-v', '--verbose'  , action='store_true', default=False, help='verbose output')
        parser.add_option ('-t', '--win_more' , action='store'     , default=5    , help='Win more pontuation')
        parser.add_option ('-r', '--win'      , action='store'     , default=3    , help='Win pontuation')
        parser.add_option ('-p', '--lose'     , action='store'     , default=1    , help='Lose pontuation')
        parser.add_option ('-s', '--lose_more', action='store'     , default=0    , help='Lose more pontuation')
        parser.add_option ('-m', '--mode'     , action='store'     , default='a'  , help='Relates to %prog functionality')
        (options, args) = parser.parse_args()
        if len(args) < 2:
            parser.error ('missing argument')
        if len(args) > 2 and options.mode == 'a':
            parser.error ('Wrong number of arguments for this mode.')
        for index,strat in enumerate(args):
            if len(strat) != 70:
                parser.error ('Strategy %d is too short or long: %d'%(index, len(strat)))
        if not(options.win_more > options.win and options.win > options.lose and options.lose > options.lose_more):
            parser.error ('Following relation must be satisfied: t > r > p > s')
        if not(options.win > ((options.win_more + options.lose_more)/2)):
            parser.error ('Following relation must be satisfied: r > (t + s)/2')
        if options.mode not in 'ab':
            parser.error ('Inexistent mode.')
        if options.verbose: print time.asctime()
        exit_code = main()
        if exit_code is None:
            exit_code = 0
        if options.verbose: print time.asctime()
        if options.verbose: print 'TOTAL TIME IN MINUTES:',
        if options.verbose: print (time.time() - start_time) / 60.0
        sys.exit(exit_code)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

# vim:set sr et ts=4 sw=4 ft=python fenc=utf-8: // See Vim, :help 'modeline'
