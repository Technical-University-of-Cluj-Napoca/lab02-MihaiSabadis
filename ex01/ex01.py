from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    anagrams = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        anagrams[key].append(s)
    return list(anagrams.values())

if __name__ == "__main__":
    input_strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    result = group_anagrams(input_strs)
    print(result)  # Output: [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]