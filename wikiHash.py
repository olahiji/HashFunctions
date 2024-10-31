import wikipediaapi
import re
def wikipage(search_string):
    wiki_wiki = wikipediaapi.Wikipedia(
        'wikiHash owenlahiji@icloud.com',
        'en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    page = wiki_wiki.page(search_string)
    #print(page.text)
    if page.exists():
        return page.text
    else:
        return None


def first_sentence_length(essay): # Made by ChatGPT
    """Returns the length of the first sentence in the given essay."""
    # Use regex to split the essay at the end of sentences
    sentences = re.split(r'[.!?]', essay)

    # Get the first sentence and strip any extra whitespace
    first_sentence = sentences[0].strip()

    # Return the length of the first sentence
    return len(first_sentence)
def main():
    # Read strings from the file
    try:
        with open('key_strings.txt', 'r') as file:
            strings = file.readlines()
    except FileNotFoundError:
        print("The file 'key_strings.txt' was not found.")
        return

    # Create Wikipedia links
    texts = [wikipage(string.strip()) for string in strings]

    # Output links to the console
    #for text in texts:
        #print(text)
    # Optionally, write the links to a new file
    with open('wikipedia_hash.txt', 'w') as output_file:
        for text in texts:
            if text is None:
                output_file.write("0" +'\n')
            else:
                output_file.write(str(first_sentence_length(text)) + '\n')
if __name__ == "__main__":
    main()