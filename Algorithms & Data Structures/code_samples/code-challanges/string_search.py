import re


class StringSearch:
    """Class to implement string search strategies"""

    def partial(self, pattern):
        """Calculate partial match table: String -> [Int]"""
        ret = [0]

        for i in range(1, len(pattern)):
            j = ret[i - 1]
            while j > 0 and pattern[j] != pattern[i]:
                j = ret[j - 1]
            ret.append(j + 1 if pattern[j] == pattern[i] else j)
        return ret

    def search(self, T, P):
        """
        KMP search main algorithm: String -> String -> [Int]
        Return all the matching position of pattern string P in T
        """
        partial, ret, j = self.partial(P), [], 0

        for i in range(len(T)):
            while j > 0 and T[i] != P[j]:
                j = partial[j - 1]
            if T[i] == P[j]:
                j += 1
            if j == len(P):
                ret.append(i - (j - 1))
                j = partial[j - 1]

        return ret

    def find_all(self, sql_statement, sub):
        """Find all substrings in a string"""
        start = 0
        while True:
            start = sql_statement.find(sub, start)
            if start == -1:
                return
            yield start
            start += len(sub)

    def find_locations(self, pattern, input_string):
        """Alternative way to identify substrings using regular expressions"""
        matches = []
        for match in re.finditer(pattern, input_string):
            matches.append({"start": match.start(), "end": match.end()})
        return matches
