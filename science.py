from ete3 import Tree
from functools import cache

aquifex = "1aquifex-tRNA.fasta"


def matrix_printer(fasta_objects, choice):
    """visualization in the dev phase"""
    for i in range(len(fasta_objects)):
        if i == 0:
            print(" " * 8, end="")
        print(fasta_objects[i][1], end=" ")
        if len(fasta_objects[i][1]) < 6:
            print(" ", end="")
    print("")
    for i in range(len(fasta_objects)):
        print(fasta_objects[i][1], end="  ")
        if len(fasta_objects[i][1]) < 6:
            print(" ", end="")

        for j in range(i):
            print("{:.4f}".format(dist_array(fasta_objects, choice)[i][j]), end=" ")
        print("")


def fasta_reader(fasta_name):
    """returns the def and seq array, which is then used by the get_name() and zip_fasta_objects().
      the program builds on the last submission."""
    def_array = []  # definition array (<)
    seq_array = []  # sequence array
    f = open(fasta_name, "r")
    morelines = True
    while morelines:
        seq = ""
        moreseq = True
        while moreseq:
            nxtline = f.readline()
            if not nxtline:
                morelines = False
                break
            elif nxtline[0] != ">":
                seq += nxtline.strip()
            else:
                def_array.append(nxtline.strip())
                moreseq = False
        if seq:  # if seq is not an empty string => True
            seq_array.append(seq)

    return def_array, seq_array


def get_name(def_array):
    shift = def_array.find("trna")  # returns index of "trna" in string
    name = "trna"
    steps = 0
    while def_array[shift + len("trna") + steps].isnumeric():   # if the following digit after "trna" is number => append
        name += def_array[shift + len("trna") + steps]
        steps += 1
    return name


def zip_fasta_objects(fasta_name):  # zips results
    def_array, seq_array = fasta_reader(fasta_name)
    name = [get_name(def_array[i]) for i in range(len(def_array))]
    fasta_objects = [(seq_array[i], name[i]) for i in range(len(name))]  # creates tuple with trna name and sequence

    return fasta_objects


def hamming_distance(obj1, obj2):
    """Calculates hamming distance for two objects at the time.
    The method we have used is better explained in the protocol."""
    len_obj1, len_obj2 = len(obj1), len(obj2)
    get_min_len = min(len_obj1, len_obj2)
    get_diff = max(len_obj1, len_obj2) - min(len_obj1, len_obj2)
    count = 0
    for i in range(get_min_len):
        if obj1[i] != obj2[i]:
            count += 1
    dist = (count + get_diff) / get_min_len  # float number between 1 and 0 as absolute distance between obj1, obj2

    return dist


@cache  # decorator to speed up the recursive function (https://docs.python.org/3/library/functools.html)
def lev_distance(x, y):
    if not x:   # if x is empty string
        return len(y)
    if not y:   # if y is empty string
        return len(x)
    return min(lev_distance(x[1:], y[1:]) + (x[0] != y[0]),     # if x[0] != y[0] == True => 1, else 0
               lev_distance(x[1:], y) + 1,
               lev_distance(x, y[1:]) + 1)


def dist_array(fasta_objects, choice):  # manages hamming and lev_distances and creates matrix for the changing values
    if choice == "1":
        func = hamming_distance
    else:
        func = lev_distance
    distance_arr = []

    for i in range(len(fasta_objects)):
        line_arr = []
        for j in range(len(fasta_objects)):
            if func == lev_distance:
                len_obj1, len_obj2 = len(fasta_objects[i][0]), len(fasta_objects[j][0])
                get_max_len = max(len_obj1, len_obj2)
            else:
                get_max_len = 1
            line_arr.append(func(fasta_objects[i][0], fasta_objects[j][0]) / get_max_len)
        distance_arr.append(line_arr)
    return distance_arr


def find_smallest_dist(dist_arr):   # func of upgma clustering
    smallest_number = 1
    for i in range(len(dist_arr)):
        for j in range(i):
            if float(dist_arr[i][j]) < smallest_number:
                smallest_number = dist_arr[i][j]
                x, y = i, j
    return x, y


def new_distance_matrix(x, y, m):
    # Swap if the indices are not ordered
    if y < x:
        x, y = y, x

    row = []
    for i in range(0, x):   # calculates new value of new row in matrix
        row.append((m[x][i] + m[y][i]) / 2)
    m[x] = row

    for i in range(x + 1, y):   # from smaller to bigger value
        m[i][x] = (m[i][x] + m[y][i]) / 2   # new matrix col

    for i in range(y + 1, len(m)):  # from bigger value to end of matrix
        m[i][x] = (m[i][x] + m[i][y]) / 2   # new matrix col
        del m[i][y]

    del m[y]    # del old bigger row/col


def new_label(x, y, label):  # creates new label with the two old ones and deletes bigger col/row label
    if y < x:
        x, y = y, x

    label[x] = "(" + label[x] + "," + label[y] + ")"    # modifies label[x] in arr, arrays are global instances
    del label[y]


def UPGMA_clustering(fasta_objects, choice):
    label = [fasta_objects[i][1] for i in range(len(fasta_objects))]
    m = dist_array(fasta_objects, choice)   # creates matrix with prefered algo
    while len(label) > 1:
        x, y = find_smallest_dist(m)
        new_distance_matrix(x, y, m)
        new_label(x, y, label)
    print("UPGMA Tree:\n",
          Tree(label[0] + ";"))  # formatting return for Tree() function


def net_divergence(m):
    """function of the NJ clustering, which deals with the different steps of the neighbourjoining clustering method."""
    net_div_arr = []
    for row in range(len(m)):
        net_div_row = 0
        for col in range(len(m)):
            net_div_row += m[row][col]
        net_div_arr.append(net_div_row)

    smallest_value = max(net_div_arr)

    for i in range(len(net_div_arr)):
        for j in range(len(net_div_arr)):
            if (m[i][j] - ((net_div_arr[i] + net_div_arr[j]) / (len(net_div_arr) - 2))) < smallest_value and i != j:
                smallest_value = m[i][j] - ((net_div_arr[i] + net_div_arr[j]) / (len(net_div_arr) - 2))
                pos_row, pos_col = i, j
    #  if the leaf distance is needed
    #  dist_from_pos_row = m[pos_col][pos_row] / 2 + (
    #              (net_div_arr[pos_row] - net_div_arr[pos_col]) / (2 * (len(net_div_arr) - 2)))
    #  dist_from_pos_col = m[pos_row][pos_col] - dist_from_pos_row
    bigger_number = max(pos_row, pos_col)
    smaller_number = min(pos_row, pos_col)

    new_u_value = []
    for i in range(len(m)):
        if i != pos_row and i != pos_col:
            new_u_value.append((m[pos_row][i] + m[pos_col][i] - m[pos_col][pos_row]) / 2)
        if i == bigger_number - 1:
            new_u_value.append(0)

    del m[smaller_number]

    for i in range(len(m)):
        m[i].pop(smaller_number)

    new_matrix = []
    for i in range(len(m)):
        new_row = []
        for j in range(len(m)):
            if i == bigger_number - 1:
                new_row.append(new_u_value[j])
            elif j == bigger_number - 1:
                new_row.append(new_u_value[i])
            else:
                new_row.append(m[i][j])
        new_matrix.append(new_row)
    return new_matrix, pos_col, pos_row


def neighbour_joining(fasta_objects, choice):
    m = dist_array(fasta_objects, choice)
    trna_label_arr = [fasta_objects[i][1] for i in range(len(fasta_objects))]
    nj_safe = []
    while len(m) > 2:
        new_matrix, col, row = net_divergence(m)
        bigger_num = max(col, row)
        smaller_num = min(col, row)
        m = new_matrix
        trna_name1, trna_name2 = trna_label_arr[row], trna_label_arr[col]
        trna_label_arr.pop(smaller_num)
        trna_label_arr.insert(bigger_num, "(" + str(trna_name1) + "," + str(trna_name2) + ")")
        trna_label_arr.pop(bigger_num - 1)
        nj_safe.append(trna_name1 + "," + trna_name2)
    unrooted = Tree(nj_safe[-2] + "," + nj_safe[-1] + ";")
    print("NJ-Tree:")
    print(unrooted)


def main():
    fasta_objects = zip_fasta_objects(aquifex)
    choice_algo = input("hamming=1, levenshtein=2:\n")
    choice_cluster = input("UPGMA=1, NJ=2:\n")
    match choice_cluster:
        case "1":
            return UPGMA_clustering(fasta_objects, choice_algo)
        case "2":
            return neighbour_joining(fasta_objects, choice_algo)
    #   matrix_printer(fasta_objects, choice_algo)  # for development purposes


if __name__ == '__main__':
    main()