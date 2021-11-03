# Aglo assignment

## How to run program 
```bash
python3 main.py
```

1. input N as number of word that you want.
2. input each word per line
3. input target word

## To run test
*make sure you have pip installed*
```bash
# install python libs
pip install -r requirements.txt

# run test
py.test 
```

## Complexity analysis

algorithm explanation: 
1. iterate over wordlist.
2. split word into left and right. (left word should have equal length of word i)
3. if left word is the same as word i and dictionary contains right word, return the answer
4. split word into left and right. (right word should have equal length of word i)
5. if right word is the same as word i and dictionary contains left word, return the answer
6. mark word i as seen in dictionary

### Time complexity analysis
to iterate over list of words, it should be O(N) where N is number of words
in each word, there are following operations
- get length of string => O(1), python optimized (naive solution might be O(M))
- split the word in to left and right, worst case is O(M) where M is length of string
- dictionary look-up should be O(1) as the python dictionary is HashMap
- set word in dictionary should be O(1) as well

Thus, time complexity should be O(N*M) where N is number of word and M is word length
### Space complexity analysis
Except the array that we store input data (which should be O(n))

I use dictionary to store words that should growth linearly according to number of words in the dictionary

space complexity should be O(n)