# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import shlex
from opening import Opening

DB_VARS = ['ECO', 'OpeningCategory', 'OpeningType', 'Games', 'BlackWins', 'BlackWinRate', 'AvgWhiteElo', 'AvgBlackElo', 'EloDiff']


def init_output(output_file):
    # open output file
    file = open(output_file, 'w')
    # print first column header without separator
    print(DB_VARS[0], file=file, end='')
    # print each column header with a preceding comma
    for i in range(1, len(DB_VARS)):
        print("," + DB_VARS[i], file=file, end='')
    # add a newline
    print(file=file)
    # close output file
    file.close()


def parse_result(result):
    if result == '1-0':
        return 1.0
    elif result == '0-1':
        return 0.0
    else:
        return 0.5


def parse_file_into_openings(input_file, openings):
    # initialize local variables
    result = 0
    white_elo = 0
    black_elo = 0
    eco = ''

    # open input file
    with open(input_file, encoding="utf8", errors='ignore') as f:
        # loop through lines
        while True:
            line = f.readline()
            # break out of loop if no more lines
            if not line:
                break
            clean_line = line.replace('[','').replace(']','').replace('.','')
            words = shlex.split(clean_line)
            if not words:
                continue
            if words[0] == 'Result':
                result = parse_result(words[1])
            elif words[0] == 'WhiteElo':
                white_elo = int(words[1])
            elif words[0] == 'BlackElo':
                black_elo = int(words[1])
            elif words[0] == 'ECO':
                eco = words[1]
            elif words[0].isnumeric():  # reached end of game record
                if eco:  # make sure record has an ECO recorded
                    # add game data if opening already recorded
                    if eco in openings:
                        openings[eco].add_game(result, white_elo, black_elo)
                    # otherwise create new opening
                    else:
                        openings[eco] = Opening(eco, result, white_elo, black_elo)
                # reinitialize local variables
                result = 0
                white_elo = 0
                black_elo = 0
                eco = ''
            else:
                continue


def write_csv(output_file, openings):
    with open(output_file, 'a') as f:
        for opening in openings:
            f.write(openings[opening].getLine())


def main():
    # set file names
    input_file = "ChessResults2023.pgn"
    output_file = "ChessResults2023.csv"

    # initialize csv file with headers
    init_output(output_file)

    # initialize dictionary of openings
    openings = {}

    # parse input file and feed data to openings dictionary
    parse_file_into_openings(input_file, openings)

    # write opening records to csv file
    write_csv(output_file, openings)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

