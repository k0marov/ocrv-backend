from rest_framework.response import Response
from rest_framework import renderers, status
from rest_framework.decorators import api_view
from api import api_logger
import os
import csv

logger = api_logger.get_logger(__name__)
json_renderer = renderers.JSONRenderer()


@api_view(['GET'])
def index(request):
    return Response('Test backend page')


@api_view(['GET'])
def texts(request):
    texts_list = []
    if not os.path.isfile('./texts.csv'):
        return Response({'display_message': 'Файл не найден'}, status=status.HTTP_404_NOT_FOUND)

    isHeaderRow = True
    with open('texts.csv', 'r', encoding='utf-8', newline='') as file:
        texts_csv = csv.reader(file, delimiter='\t', skipinitialspace=True)
        # итерируемся по строкам CSV-файла
        for row in texts_csv:
            # пропускаем первую строку с заголовками
            if isHeaderRow:
                isHeaderRow = False
                continue
            texts_list.append({'id': row[0], 'text': row[1], 'note': row[2]})

    # если нет текстов
    if not texts_list:
        return Response({'display_message': 'Тексты не найдены'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'texts': texts_list})


@api_view(['POST'])
def speeches():
    # file = request.files['speech']
    # if file and allowed_file(request.json['text_id']):
    #     filename = secure_filename(request.json['text_id'])
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # logger.info(f"Success text id: {request.json['text_id']}; retries: {request.json['retries']}")
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def skips(request):
    # логируем
    logger.info(f'Skipped text id: {request.data["text_id"]}; retries: {request.data["retries"]}')
    return Response(status=status.HTTP_200_OK)
