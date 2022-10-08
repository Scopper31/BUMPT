import face_recognition
from PIL import Image, ImageDraw
import pickle
import cv2


def extracting_faces(img_path):
    faces = face_recognition.load_image_file(img_path)
    #print(faces)
    faces_locations = face_recognition.face_locations(faces)

    for face_location in faces_locations:
        top, right, bottom, left = face_location

        face_img = faces[top:bottom, left:right]
        pil_img = Image.fromarray(face_img)
        pil_img.save(f"{img_path[:-4]}_face.jpg")


'''def find_in_base(img_path, base_path):
    img = face_recognition.load_image_file(img_path)
    img_encodings = face_recognition.face_encodings(img)[0]
    #base =  # хз
    for base_item in base:
        base_item_encodings = face_recognition.face_encodings(base_item[0])[0]
        #if compare_faces
'''


def compare_faces(img1_path, img2_path):
    img1 = face_recognition.load_image_file(img1_path)
    img1_encodings = face_recognition.face_encodings(img1)[0]
    #print(img1_encodings)

    img2 = face_recognition.load_image_file(img2_path)
    img2_encodings = face_recognition.face_encodings(img2)[0]

    result = face_recognition.compare_faces([img1_encodings], img2_encodings)
    if result[0]:
        return True
    else:
        return False


def main():
    img_path1 = '/content/i1.jpg'
    img_path2 = '/content/i2.jpg'
    extracting_faces(img_path2)
    print(compare_faces(img_path1, img_path2))


if __name__ == '__main__':
    main()

