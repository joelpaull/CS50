import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Incorrect commandline argument count")
        return 1

    database = sys.argv[1]
    sequence = sys.argv[2]

    # TODO: Read database file into a variable
    database_list = []
    with open(database, "r") as database_file:
        database_reader = csv.DictReader(database_file)
        for row in database_reader:
            database_list.append(row)
        for i in database_list:
            for key in i:
                if i[key].isalpha():
                    pass
                else:
                    i[key] = int(i[key])

    # TODO: Read DNA sequence file into a variable
        with open(sequence, "r") as sequence_file:
            sequence_data = sequence_file.read()

    # TODO: Find longest match of each STR in DNA sequence
            STRs = database_reader.fieldnames[1:]
            STR_count = {}
            for STR in STRs:
                STR_count[STR] = longest_match(sequence_data, STR)

    # TODO: Check database for matching profiles
            match_count = {}
            for profile in database_list:
                matches = 0
                for STR in STRs:
                    if int(profile[STR]) == STR_count[STR]:
                        matches += 1
                match_count[profile["name"]] = matches
            total = len(STRs)
            matched_name = "No Match"
            for name, num in match_count.items():
                if num == total:
                    matched_name = name

            print(matched_name)
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
