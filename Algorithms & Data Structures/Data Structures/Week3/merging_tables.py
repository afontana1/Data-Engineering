# python3
# Task. There are n tables stored in some database. The tables are numbered from 1 to n. All tables share
# the same set of columns. Each table contains either several rows with real data or a symbolic link to
# another table. Initially, all tables contain data, and i-th table has r[i] rows. You need to perform 𝑚 of
# the following operations:
# 1. Consider table number destination[i] Traverse the path of symbolic links to get to the data. That is,
# while destination[i] contains a symbolic link instead of real data do
# destination[i] <- symlink(destination[i])
# 2. Consider the table number source[i] and traverse the path of symbolic links from it in the same manner as for destination[i].
# 3. Now, destination[i] and source[i] are the numbers of two tables with real data. If destination[i] != source[i]
# copy all the rows from table source[i] to table destination[i] then clear the table source[i]
# and instead of real data put a symbolic link to destination[i] into it.
# 4. Print the maximum size among all n tables (recall that size is the number of rows in the table).
# If the table contains only a symbolic link, its size is considered to be 0.
# Input Format. The first line of the input contains two integers n and m — the number of tables in the database and the number of merge queries to perform, respectively.
# The second line of the input contains n integers r[i] — the number of rows in the i-th table.
# Then follow m lines describing merge queries. Each of them contains two integers destination[i] and
# source[i] — the numbers of the tables to merge.
# Output Format. For each query print a line containing a single integer — the maximum of the sizes of all
# tables (in terms of the number of rows) after the corresponding operation.


class Database:
    def __init__(self, row_counts):
        self.row_counts = row_counts  # row_counts[i] stores the number of rows in the i-th table, 0 if it contains symbol link
        self.max_row_count = max(
            row_counts
        )  # initial value of the maximal number of rows among all tables
        n_tables = len(row_counts)  # Number of tables
        self.ranks = [
            1
        ] * n_tables  # Rank of each disjoint set, starts with singleton for each table
        self.parents = list(
            range(n_tables)
        )  # Parent of each table after merging, starts with singleton (each table is parent of itself)

    def compare_max(
        self, k
    ):  # k is the index of newly merged table, compare the number of rows of new table with the maximum before merging
        if self.max_row_count < self.row_counts[k]:
            self.max_row_count = self.row_counts[k]

    def union(
        self, i, j
    ):  # We do not care if it's source or destination now under union by rank, merge shallow tree to larger tree using rank
        if self.ranks[i] > self.ranks[j]:
            self.parents[j] = i
            self.row_counts[i] += self.row_counts[
                j
            ]  # No matter which is merged to which, it does not affect the number of rows in total, and one of them must be 0
            self.row_counts[j] = 0
            self.compare_max(
                i
            )  # Compare the number of rows of merged disjoint set with previous record
        else:
            self.parents[i] = j
            self.row_counts[j] += self.row_counts[
                i
            ]  # No matter which is merged to which, it does not affect the number of rows in total, and one of them must be 0
            self.row_counts[i] = 0
            self.compare_max(
                j
            )  # Compare the number of rows of merged disjoint set with the maximum to check if merging operations leads to a new table with more rows than before
            if (
                self.ranks[i] == self.ranks[j]
            ):  # In case of merging two trees of the same height, increase the rank by 1
                self.ranks[j] += 1

    def merge(self, src, dst):
        # https://en.wikipedia.org/wiki/Disjoint-set_data_structure#Operations
        src_parent = self.get_parent(src)  # Parent of source table
        dst_parent = self.get_parent(dst)  # PArent of destination table

        if (
            src_parent == dst_parent
        ):  # If they share the same parent, no merging operations as they are already in the same disjoint set
            return False
        self.union(src_parent, dst_parent)  # Otherwise, merge them using union by rank
        return True

    def get_parent(
        self, table
    ):  # Apply a path compression algorithm here to shorten the tree height between children nodes and their parents
        if table != self.parents[table]:
            self.parents[table] = self.get_parent(self.parents[table])
        return self.parents[table]


def main():
    n_tables, n_queries = map(int, input().split())
    counts = list(map(int, input().split()))
    assert len(counts) == n_tables
    db = Database(counts)
    for i in range(n_queries):
        dst, src = map(int, input().split())
        db.merge(src - 1, dst - 1)
        print(db.max_row_count)


if __name__ == "__main__":
    main()
