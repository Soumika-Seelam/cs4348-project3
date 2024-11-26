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
- connected local repository to github
- test successful

### 3: 11/25 8:35 PM

- importing os and struct library
- created the header class which decides the structure
- create the create function
    - will allow the users to create a file with the chosen file name
    - with xxd can check what the binary contents of the file look like
    - if you make a file with the same name again, will ask if you want to abort
        - if you say yes, it will replace the file with the new one
        - if you say no, it will abort
- saw that local repository was not properly connected with github repository, fixed connection
- connected properly now!

### 4: 11/26 1:35 PM
- created the open function which checks whether a file is valid
- didn't add proper checking, python file passed as well (so added header data check for 8 bytes)
- python file still passed, so made it so that it had to have at least 512 bytes
- also added condition so that it will ask when you try to make non idx files if you want to proceed anyways
- went back and added proper checking to make sure that only index files would be accepted
- tested file with three case: proper index file, opening file which doesn't exist, and opening file which is not an index file
    - program properly handled all cases! 
- committed the new open code, and committed to github!

### 5: 11/26 2:10 PM
- created insert, insert into tree, and insert into leaf methods
    - had to also create a from_bytes method in the header class to process the bytes
    - also had to add a separate node class so we can insert nodes of the key and value pairs
    - tested with creating key value pair 10, 100
    - then made sure we could add another one 20, 200
    - then made sure it would detect if a duplicate one was being made
        - all test cases passed!

### 6: 11/26 2:26 PM
- now working on node-splitting: when a node is more than the accepted limit during insertion, have to split the node
    - middle key becomes parent key
    - the key and values that are left become child nodes
    - if the parent node is also full, then the splitting has to be propogated up the tree
    - running into some errors, node is not splitting even though the key limit is being reached
    - debugging with print statements
