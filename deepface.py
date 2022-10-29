import face_recognition
from PIL import Image
import os
import pandas as pd
import pickle

import argparse


def convert_to_encodings(img_path):
    img = face_recognition.load_image_file(img_path)
    img_encodings = face_recognition.face_encodings(img)[0]
    return img_encodings


def compare_faces_encodings(img1_encodings, img2_encodings):
    result = face_recognition.compare_faces([img1_encodings], img2_encodings)
    if result[0]:
        return True
    else:
        return False


def compare_faces(img1_path, img2_path):
    img1_encodings = convert_to_encodings(img1_path)
    img2_encodings = convert_to_encodings(img2_path)
    return compare_faces_encodings(img1_encodings, img2_encodings)


def load_to_base(img_path, base_path, link):
    img = face_recognition.load_image_file(img_path)
    img_encodings = face_recognition.face_encodings(img)[0]
    with open(base_path, 'wb+') as base:
        if os.path.getsize(base_path) > 0:
            data = pickle.load(base)
            data[link] = img_encodings
            pickle.dump(data, base)
        else:
            data = {link: img_encodings}
            pickle.dump(data, base)


def check_base(base_path):
    with open(base_path, 'rb+') as base:
        t = pickle.load(base)
        print(t)


def find_in_base(img_path, base_path):
    img = face_recognition.load_image_file(img_path)
    img_encodings = face_recognition.face_encodings(img)[0]
    with open(base_path, "rb+")as base:
        data = pickle.load(base)

    for link, encoding in data.items():
        if compare_faces_encodings(img_encodings, encoding):
            return link
    return 'Nothing was found un base'


def extracting_faces(img_path, persons_dir):
    faces = face_recognition.load_image_file(img_path)
    faces_locations = face_recognition.face_locations(faces)
    count = 1
    for face_location in faces_locations:
        top, right, bottom, left = face_location

        face_img = faces[top:bottom, left:right]
        pil_img = Image.fromarray(face_img)
        pil_img.save(f"{persons_dir}/{img_path[:-4]}_face({count}).jpg")
        count += 1


def main():
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(dest='command')

    load = subparser.add_parser('load')
    load.add_argument('--img_path', type=str, required=True)
    load.add_argument('--base_path', type=str, required=True)
    load.add_argument('--link', type=str, required=True)
    load.set_defaults(func=load_to_base)

    find = subparser.add_parser('find')
    find.add_argument('--img_path', type=str, required=True)
    find.add_argument('--base_path', type=str, required=True)
    find.add_argument('--token', type=str, required=True)
    find.set_defaults(func=find_in_base)

    check = subparser.add_parser('check')
    check.add_argument('--base_path', type=str, required=True)
    check.set_defaults(func=check_base)

    args = parser.parse_args()

    if args.command == 'load':
        load_to_base(args.img_path, args.base_path, args.link)

    if args.command == 'check':
        check_base(args.base_path)

    if args.command == 'find':
        persons_dir = f'faces({args.token})'

        os.mkdir(persons_dir)

        extracting_faces(args.img_path, persons_dir)
        chosen_face_number = input('chosen_face_number ')
        chosen_face_path = f'{args.img_path[:-4]}_face({chosen_face_number}).jpg'
        chosen_face_abs_path = f'{persons_dir}/{chosen_face_path}'
        find_result = find_in_base(chosen_face_abs_path, args.base_path)
        print(find_result)

        os.remove(persons_dir)


if __name__ == '__main__':
    main()
