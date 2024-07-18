

import shlex
from opening import Opening

DB_VARS = ['ECO', 'OpeningCategory', 'OpeningType', 'Games', 'BlackWins', 'BlackWinRate', 'AvgWhiteElo', 'AvgBlackElo',
           'EloDiff']


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


def parse_file_into_openings(input_file, openings):
    # initialize local variables
    result = ''
    white_elo = 0
    black_elo = 0
    eco = ''
    unknown_eco_count = 0

    # open input file
    with open(input_file, encoding="utf8", errors='ignore') as f:
        # loop through lines
        while True:
            line = f.readline()

            # break out of loop if no more lines
            if not line:
                break

            # ignore empty lines
            if line == '\n':
                continue

            # remove brackets and periods from raw line
            clean_line = line.replace('[', '').replace(']', '').replace('.', '')
            # split into tokens, maintaining substrings enclosed by quotation marks as whole tokens
            words = shlex.split(clean_line)

            # check for the data fields we're interested in and save the associated data
            if words[0] == 'Result':
                result = words[1]
            elif words[0] == 'WhiteElo':
                white_elo = int(words[1])
            elif words[0] == 'BlackElo':
                black_elo = int(words[1])
            elif words[0] == 'ECO':
                eco = words[1]
            # use list of moves to indicate the end of a game record
            elif words[0].isnumeric():
                # make sure record has an ECO recorded
                if eco:
                    # add game data if opening already recorded
                    if eco in openings:
                        openings[eco].add_game(result, white_elo, black_elo)
                    # otherwise create new opening
                    else:
                        openings[eco] = Opening(eco, result, white_elo, black_elo)
                else:
                    # running count of games with no listed ECO
                    unknown_eco_count += 1

                # reinitialize local variables
                result = ''
                white_elo = 0
                black_elo = 0
                eco = ''
            # other data fields are ignored
            else:
                continue
    print("unknown eco count: " + str(unknown_eco_count))


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
