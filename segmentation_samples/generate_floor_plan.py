import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# NOTE: After running or compiling the python file closing the output will take us to next output , for eg first we close the original image then we get the preprocessed

#All the results with all the images are given in the samples folder the original image, the preprocessed image, the edge detection, the floor plan including....


def load_image(image_path):
    # Loading the image into grayscale for removing the colours and visibility of images through open cv
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Image not found or unable to load.")
    return image

def preprocess_image(image):
    # Apply Gaussian Blur to reduce noise 
    # The application of a mathematical function to an image in order to blur it.
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    return blurred

def edge_detection(image):
    # Using Canny edge detectors
    edges = cv2.Canny(image, 50, 150, apertureSize=3)
    return edges

def find_contours(edges):
    # Countouring the layers of the image
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def draw_floor_plan(contours, image_shape):
    # Creation of  a blank image for drawing
    floor_plan = np.zeros(image_shape, dtype=np.uint8)
    
    # Drawing the contours on the blank image
    cv2.drawContours(floor_plan, contours, -1, (255, 255, 255), 1) # Making the floor plan more prominent
    
    return floor_plan

def save_image(image, path):
    cv2.imwrite(path, image)

def main(image_path):
    # Load and preprocess the image as specified in the {file_path}
    image = load_image(image_path)
    preprocessed_image = preprocess_image(image)
    edges = edge_detection(preprocessed_image)
    contours = find_contours(edges)
    floor_plan = draw_floor_plan(contours, image.shape)
    
    # Defining the output directory and filenames
    output_dir = os.path.dirname(image_path)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    original_image_path = os.path.join(output_dir, f"{base_name}_original.jpg")
    preprocessed_image_path = os.path.join(output_dir, f"{base_name}_preprocessed.jpg")
    edges_image_path = os.path.join(output_dir, f"{base_name}_edges.jpg")
    floor_plan_image_path = os.path.join(output_dir, f"{base_name}_floor_plan.jpg")
    
    # Save the images
    save_image(image, original_image_path)
    save_image(preprocessed_image, preprocessed_image_path)
    save_image(edges, edges_image_path)
    save_image(floor_plan, floor_plan_image_path)
    
    # Optionally, display the images
    display_image(image, title='Original Image')
    display_image(preprocessed_image, title='Preprocessed Image')
    display_image(edges, title='Edge Detection')
    display_image(floor_plan, title='Floor Plan')

def display_image(image, title='Image'):
    plt.figure(figsize=(10, 10))
    plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

# image file path
dir = os.getcwd()
image_path = os.path.join(dir, 'New_Model.png')
main(image_path)
