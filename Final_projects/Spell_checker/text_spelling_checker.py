import argparse
from spellchecker import SpellChecker

def check_spelling(input_file, output_file):
    '''main function'''
    # initalization
    spell = SpellChecker(language='en')

    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            for line in infile:
                corrected_line = []
                words = line.split()
                for word in words:
                    if not spell.unknown([word]):
                        corrected_line.append(word)
                    else:
                        suggestions = list(spell.candidates(word))
                        print(f"Found word '{word}', proposed options: {suggestions}")
                        print(f"Enter the number of the correct option or press Enter to leave '{word}':")
                        for i, suggestion in enumerate(suggestions, 1):
                            print(f"{i}: {suggestion}")
                        choice = input("Select an option (or press Enter): ").strip()
                        if choice.isdigit() and 1 <= int(choice):
                            corrected_line.append(suggestions[int(choice) - 1])
                        else:
                            corrected_line.append(word)
                
                outfile.write(' '.join(corrected_line) + '\n')

        print(f"The result was written to a file '{output_file}'.")

    except IOError:
        print("Error opening or writing file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to check and correct spelling in a text file.")
    parser.add_argument("-f", "--input-file", dest="input_file", required=True, help="Path to the input text file")
    parser.add_argument("-o", "--output-file", dest="output_file", required=True, help="Path to the output file to write the results")
    args = parser.parse_args()

    check_spelling(args.input_file, args.output_file)
