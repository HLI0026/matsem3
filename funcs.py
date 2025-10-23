import numpy as np
import matplotlib.pyplot as plt

def get_p2_triang(k, only_p1=False):

    N = k+1
    x = np.linspace(-1, 1, N)
    y = np.linspace(-1, 1, N)
    X, Y = np.meshgrid(x, y)
    V = np.column_stack([X.ravel(), Y.ravel()])

    p1_indexes = []
    p1_coords = []
    for i in range(k):
        for j in range(k):
            d0 = i * N + j
            d1 = d0 + 1
            d2 = d0 + (N + 1)

            h0 = d0
            h1 = d1 + N 
            h2 = d2 - 1 

            p1_indexes.append([d0, d1, d2])
            p1_indexes.append([h0, h1, h2])

            p1_coords.append([V[d0], V[d1], V[d2]])
            p1_coords.append([V[h0], V[h1], V[h2]])

    if only_p1:
        return p1_indexes, p1_coords

    p2_indexes = []
    p2_coords = []
    for (i1, i2, i3), (c1, c2, c3) in zip(p1_indexes, p1_coords):
        mid_1_i = (i2 + i1) 
        mid_2_i = (i3 + i2) 
        mid_3_i = (i1 + i3) 

        mid_1_c = (c1 + c2) / 2
        mid_2_c = (c2 + c3) / 2
        mid_3_c = (c3 + c1) / 2

        p2_indexes.append([i1 * 2 , mid_1_i, i2 * 2, mid_2_i, i3 * 2, mid_3_i])
        p2_coords.append([c1, mid_1_c, c2, mid_2_c, c3, mid_3_c])

    return np.array(p2_indexes), np.array(p2_coords)

def plot_p2_mesh(p2_idx, p2_coords):
    plt.figure(figsize=(16, 16))
    corner_points = p2_coords[0]
    
    for tri_i, tri_c in zip(p2_idx, p2_coords):
        p1_tri_coords = tri_c[0::2]
        triangle = plt.Polygon(p1_tri_coords, fill=None, edgecolor='gray', linestyle='-')
        plt.gca().add_patch(triangle)
        x, y = tri_c[:, 0], tri_c[:, 1]
        plt.scatter(x, y, color='black', s=10)
        
        for i,(x,y) in enumerate(zip(x, y)):
            plt.text(x, y, tri_i[i], color='green', fontsize=12, ha='right', va='top')

def print_idx_coords_per_triag(p2_idx, p2_coords,triags_to_print=None):
    
    triags_to_print = list(triags_to_print) if triags_to_print is not None else None
    
    if triags_to_print is None:
        triags_to_print = range(len(p2_idx))

    for i, (tri_i, tri_c) in enumerate(zip(p2_idx, p2_coords)):
        if i not in triags_to_print:
            continue
        print(f"=============Triangle {i}:=============")
        p1_tri_coords = tri_c[0::2]
        x, y = tri_c[:, 0], tri_c[:, 1]
        for j,(x,y) in enumerate(zip(x, y)):
            print(f"Index: {tri_i[j]}, Coord: ({x:.2f}, {y:.2f})")

        