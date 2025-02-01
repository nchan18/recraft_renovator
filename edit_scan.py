# filepath: /home/nitin/Documents/recraft_renovator/remove_ceiling.py
import trimesh
import numpy as np

def remove_ceiling(mesh, height_threshold):
    # Find faces above the height threshold
    face_centers = mesh.triangles_center
    ceiling_faces = np.where(face_centers[:, 2] > height_threshold)[0]

    # Remove the ceiling faces
    mesh.update_faces(~np.isin(np.arange(len(mesh.faces)), ceiling_faces))
    return mesh

if __name__ == '__main__':
    # Load the .glb file
    mesh = trimesh.load('house.glb')

    # Define the height threshold to identify the ceiling
    height_threshold = 2.5  # Adjust this value based on your mesh

    # Remove the ceiling
    modified_mesh = remove_ceiling(mesh, height_threshold)

    # Save the modified mesh
    modified_mesh.export('house_no_ceiling.glb')