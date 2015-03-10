#!/usr/bin/python2

"""browser.py: A primitive web browser."""

__author__ = 'andrei.muntean.dev@gmail.com (Andrei Muntean)'

import os
import sys
import urllib

# Keeps track of visited web pages.
history = []

# Keeps track of the hyperlinks on the current web page.
hyperlinks = []

# Clears the screen.
def clear():
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

# Sends a request to the specified URL and returns a list of tokens.
def get(url):
    data = urllib.urlopen(url)
    return data.read().split()

# Gets the current url.
def current_url():
    if len(history) > 0:
        return history[-1]
    else:
        return ''

# Determines whether the specified token is an HTML tag.
def is_tag(token):
    return token[0] == '<' or token[-1] == '>'

# Tries to transform a string into a valid URL.
def to_url(string):
    if string[0] == '.':
        # Gets the current url.
        url = current_url()

        # Removes what follows after the last '/'.
        url = url[0:url.rfind('/')]

        # Appends this string to it, minus the '. at the start.
        url += string[1:]

        # Returns the new url.
        return url
    else:
        return string

# Shows the help menu.
def show_help():
    print 'q, quit -- Exits the program.'
    print 'b, back -- Goes to the previously accessed page.'
    print 'h, help -- Shows the help menu.'
    print 'Input a URL to access it.'
    print 'Input a number to access the hyperlinks from a page.'

# Transforms a list of strings into a web page.
def show_web_page(tokens):
    # Clears the list of hyperlinks.
    del hyperlinks[:]

    print 'URL: ' + current_url()

    for token in tokens:
        if is_tag(token):
            token = token.lower()

            if token == '<title>':
                print 'TITLE:',
            elif len(token) == 4 and token[1] == 'h':
                print '\nHEADING ' + token[2] + ':',
            elif token == '<p>':
                print '\nPARAGRAPH:',
            elif token == '<em>':
                print '\033[1m',
            elif token == '</em>':
                print '\033[0;0m',
            elif token.find('.html') > -1:
                start = token.find('"') + 1
                end = token.find('.html') + 5
                hyperlinks.append(token[start:end])
        else:
            print token,

    # Prints a newline.
    print
    print '----'

    if (len(hyperlinks) > 0):
        # Displays the hyperlinks.
        for index in range(0, len(hyperlinks)):
            print str(index + 1) + ': ' + hyperlinks[index]


# Goes to the previously accessed page.
def go_back():
    if len(history) >= 2:
        history.pop()
        goto(history.pop())
    elif len(history) == 1:
        goto(history.pop())

# Goes to the specified URL.
def goto(url):
    # Clears the screen.
    clear()

    # Sends a request to the server.
    tokens = get(url)

    # Keeps track of this url.
    history.append(url)

    # Displays the web page.
    show_web_page(tokens)

# Gets user input.
def get_input():
    return raw_input('> ')

# The main function.
def run():
    # Determines whether a URL was specified as an argument.
    if len(sys.argv) > 1:
        goto(sys.argv[1])

    while True:
        try:
            command = get_input()

            if command.isdigit():
                index = int(command) - 1

                if 0 <= index and index < len(hyperlinks):
                    # Go to the specified hyperlink.
                    goto(to_url(hyperlinks[index]))
            elif command == 'q' or command == 'quit':
                # Exit the program.
                break
            elif command == 'b' or command == 'back':
                # Go to a previous page.
                go_back()
            elif command == 'h' or command == 'help':
                # Shows the help page.
                show_help()
            elif command[:4] == 'http':
                # Go to the specified URL.
                goto(command)
            else:
                # Go to the specified URL.
                goto('http://' + command)
        except:
            print 'Invalid URL.'

# Runs the program.
run()