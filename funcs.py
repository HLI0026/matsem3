import numpy as np
import matplotlib.pyplot as plt

def get_p2_triang(k):
    """
    Generate triangulation for square (-1,1)x(-1,1)
    using 2x denser grid for P2 elements.
    """
    N = 2 * k + 1              # number of nodes per side
    x = np.linspace(-1, 1, N)
    y = np.linspace(-1, 1, N)
    X, Y = np.meshgrid(x, y)
    V = np.column_stack([X.ravel(), Y.ravel()])  # all grid nodes

    elem = []     
    elem_coords = []  

    for j in range(0, N - 1, 2):      # step of 2 because P1 corners are every other node
        for i in range(0, N - 1, 2):
            v00 = j * N + i           # bottom-left
            v02 = j * N + i + 2       # bottom-right
            v20 = (j + 2) * N + i     # top-left
            v22 = (j + 2) * N + i + 2 # top-right

            # mid-edge nodes
            vmid_bottom = j * N + i + 1          # bottom middle
            vmid_left   = (j + 1) * N + i        # left middle
            vmid_right  = (j + 1) * N + i + 2    # right middle
            vmid_top    = (j + 2) * N + i + 1    # top middle
            vmid_diag   = (j + 1) * N + i + 1    # center point (diagonal crossing)

            tri1 = [v00, v02, v22,
                    vmid_bottom, vmid_diag, vmid_right]  # P2 order
            elem.append(tri1)
            elem_coords.append(V[tri1])

            tri2 = [v00, v22, v20,
                    vmid_diag, vmid_top, vmid_left]
            elem.append(tri2)
            elem_coords.append(V[tri2])

    return np.array(elem), np.array(elem_coords), V

def plot_p2_mesh(p2_idx, p2_coords):
    plt.figure(figsize=(8, 8))
    ax = plt.gca()
    
    for tri_i, tri_c in zip(p2_idx, p2_coords):
        corner_coords = tri_c[:3]  # first three nodes are corners
        triangle = plt.Polygon(corner_coords, fill=None, edgecolor='gray', linestyle='-')
        ax.add_patch(triangle)
        
        x, y = tri_c[:, 0], tri_c[:, 1]
        ax.scatter(x, y, color='black', s=20)
        
        for idx, (xi, yi) in zip(tri_i, tri_c):
            ax.text(xi, yi, str(idx), color='green', fontsize=10, ha='right', va='top')
    
    ax.set_aspect('equal')
    plt.show()


def print_idx_coords_per_triag(p2_idx, p2_coords, triags_to_print=None):
    triags_to_print = list(triags_to_print) if triags_to_print is not None else range(len(p2_idx))

    for i, (tri_i, tri_c) in enumerate(zip(p2_idx, p2_coords)):
        if i not in triags_to_print:
            continue
        print(f"============= Triangle {i} =============")
        for idx, coord in zip(tri_i, tri_c):
            print(f"Index: {idx}, Coord: ({coord[0]:.2f}, {coord[1]:.2f})")
        