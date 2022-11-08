"""my howemowork n3"""
import numpy as np

def check_kernel( kernel: np.array ) -> np.array:
    """check whether the kernel is in the right format and update it"""
    row, coll = np.shape(kernel)
    if row % 2 == 0 or coll % 2 == 0:
        kernel = np.pad(kernel, [(0, 1), (0, 1)], mode='constant')
    return kernel

def count_it( image: np.array, kernel: np.array ) -> np.array:
    """main function for filter"""
    kernel_shape = np.shape(kernel)
    image_shape = np.shape(image)
    new_image = np.zeros(shape=(image_shape), dtype=np.float64)
    padding = kernel_shape[0]//2
    ker = kernel_shape[0]
    image_pad = np.pad(image, pad_width=padding)
    for row in range(image_shape[0]):
        for coll in range(image_shape[1]):
            our_sum = np.clip(np.sum( image_pad[row: row + ker, coll: coll+ker] * kernel, dtype=np.float64), 0, 255)
            new_image[row][coll] = our_sum
    return new_image.astype(np.uint8)

def apply_filter(image: np.array, kernel: np.array) -> np.array:
    """ Apply given filter on image """
    # A given image has to have either 2 (grayscale) or 3 (RGB) dimensions
    assert image.ndim in [2, 3]
    # A given filter has to be 2 dimensional and square
    assert kernel.ndim == 2
    assert kernel.shape[0] == kernel.shape[1]
    kernel = check_kernel(kernel)
    image_shape = image.shape
    kernel.astype(np.float64)
    image.astype(np.float64)
    if image.ndim == 3:
        new_image = np.empty(image_shape)
        for i in range(3):
            l = count_it( (image[:, :, i:i+1]).reshape( image_shape[0:2] ), kernel ).reshape( (512, 512, 1) )
            new_image[:, :, i:i+1] = l
        image = new_image
    else:
        image = count_it( image, kernel )
    return image.astype(np.uint8)
#if __name__== "__main__":
#    from helpers import *
#    image = read_image('../tests/lenna.png')
#    #image_gray = np.average(image.astype(np.float), weights=[0.299, 0.587, 0.114], axis=2).astype(np.uint8)
#    s = apply_filter( image, identity_kernel)
