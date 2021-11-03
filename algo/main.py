from typing import List, Optional

from collections import defaultdict

d: dict = defaultdict(lambda: 0)


def solve(wordlist: List[str], target: str) -> Optional[tuple]:
    d.clear()  # make sure we have a clean dictionary
    len_target = len(target)
    for word in wordlist:
        len_word = len(word)
        word_as_left = target[:len_word]
        right = target[len_word:]

        if word == word_as_left and d[right] == 1:
            return word, right

        len_left = len_target - len_word
        left = target[:len_left]
        word_as_right = target[len_left:]

        if word == word_as_right and d[left] == 1:
            return left, word

        d[word] = 1
    return None


def main():
    word_list = []
    n = int(input("input number of word: "))
    for i in range(n):
        word = input()
        word_list.append(word)
    target = input()

    print(solve(word_list, target))


if __name__ == '__main__':
    main()
