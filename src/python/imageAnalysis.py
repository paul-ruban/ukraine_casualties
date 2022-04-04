import os
import io
import sys
from google.cloud import vision

def detect_document():
    """Detects document features in an image."""
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/odymov/Documents/Altiteck/UkraineCasualties/Code/ukraine_casualties/keys/keyFile.json"
    client = vision.ImageAnnotatorClient()

    # path = '/Users/odymov/Documents/Altiteck/UkraineCasualties/Code/ukraine_casualties/data/images/IMG_20220315_233750_090.jpg'
    path = '/Users/odymov/Documents/Altiteck/UkraineCasualties/Code/ukraine_casualties/data/images/IMG_20220403_113153_300.jpeg'

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))

                    for symbol in word.symbols:
                        print('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))



# def analyseImage():
#     # pics = ['https://i.imgur.com/2EUmDJO.jpg', 'https://i.imgur.com/FPMomNl.png']
#     pics = ['../data/images/IMG_20220315_233750_090.jpg']

#     client = vision.ImageAnnotatorClient()
#     image = vision.types.Image()

#     for pic in pics:
#         image.source.image_uri = pic
#         response = client.face_detection(image=image)

#         print('=' * 79)
#         print('File: {pic}')
#         for face in response.face_annotations:
#             likelihood = vision.enums.Likelihood(face.surprise_likelihood)
#             vertices = [f'({v.x},{v.y})' for v in face.bounding_poly.vertices]
#             print(f'Face surprised: {likelihood.name}')
#             print(f'Face bounds: {",".join(vertices)}')

if __name__ == '__main__':
    globals()[sys.argv[1]]()
