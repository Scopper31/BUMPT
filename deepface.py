from deepface import DeepFace
import json


def face_verify(img_1, img_2):
    try:
        result_dict = DeepFace.verify(img1_path=img_1, img2_path=img_2)

        with open('result.json', 'w') as file:
            json.dump(result_dict, file, indent=4, ensure_ascii=False)

        if result_dict.get('verified'):
            return True
        return False

    except Exception as _ex:
        return _ex


def main():
    img1_path = ''
    img2_path = ''
    print(face_verify(img_1=img1_path, img_2=img2_path))


if __name__ == '__main__':
    main()
