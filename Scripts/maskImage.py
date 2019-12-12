'''
arguments:
input_path that points to the folder with all of the offset images
output_path - folder that you want the masks saved to
blank_path - path to the cropped blank image you want to overlay on top of
'''

def maskImage(input_path, output_path, blank_path):
    for file in os.listdir(f'{input_path}'):
        image = cv2.imread(f'{input_path}/{file}')
        blank = cv2.imread(f'{balnk_path}')
        diff = cv2.absdiff(blank, Cropping(image))
        cv2.imwrite(f'{output_path}/{file}', diff)



def Cropping(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = 255*(gray < 128).astype(np.uint8)
    coords = cv2.findNonZero(gray)
    x, y, w, h = cv2.boundingRect(coords)
    image = image[y:y+h, x:x+w]
    image_resized = cv2.resize(image, (blank.shape[1], blank.shape[0]))
    return image_resized