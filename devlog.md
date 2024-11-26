# Devlog


## Project Understanding
### 1: 11/25 7:45 PM

I first read through the project requirements, from which I understood that:
    - The program I need to create is one that will manage a B-tree that is file based
    - users should be able to search, insert, open, and perform operation on the index file
    - need to make sure that index file follows a structure that is binary, and has header and node blocks
    - the structure has to be able to work with at most 3 nodes (at a single time)
- More details
    - minimum degree of 10 for the b-tree (because it should only be able to have max 19 keys and 20 child pointers)
    - big-endian format for the header block and all of the numbers
    - program should be able to handle invalid input and file errors as well
- My plan:
    - set up git repo with python file and devlog.md
    - write the utility functions
        - should be able to read/write the blocks to a binary file
        - big-endian conversation should be handled
    - create command
        - needs to create an index file with a proper header
    - update devlog throughout!

## Development
### 2: 11/25 8:22 PM

- i created the github
- i created both files devlog.md and btree_manager.py
- first commit with files
- created main function to test whether project was working or not
- test successful
