import csv
import json
from paddleocr import PaddleOCR

def save_nlp_datas(ocr_datas, csv_datas, save_path):
    '''
    转换并保存数据集文件
    '''
    nlp_datas = []
    for data, filename in zip(ocr_datas, csv_datas.keys()):
        context = data[0]
        qas = []
        for qa in data[1]:
            question_id, question = qa
            qa = {
                "question": question,
                "id": question_id, 
                "answers": [
                    {
                        "text": "无", 
                        "answer_start": 0
                    }
                ]          
            }
            qas.append(qa)
        if qas!= []:
            data = {
                'paragraphs': [
                    {
                        "context": context,
                        "title": filename,
                        "qas": qas
                    }
                ]
            }
            nlp_datas.append(data)

    dataset = {
        'data': nlp_datas
    }

    with open(save_path, 'w') as f:
        json.dump(dataset, f, ensure_ascii=False)

def main():
    # 读取 csv 文件
    csv_datas = {}
    with open('data/test1-utf8.csv', 'r') as f:   #这里需要修改！！！！
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i==0:
                continue
            index, question_id, filename, question = row

            if filename in csv_datas:
                csv_datas[filename]['qas'].append([question_id, question])
            else:
                csv_datas[filename] = {
                    'qas':[[question_id, question]]
                }


    # 加载 OCR 模型
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    ocr_datas = []
    for filename, data in csv_datas.items():
        img_path = 'picture/%s' % filename     #这里需要修改！！！！

        # ocr 识别
        result = ocr.ocr(img_path, cls=True)

        # 拼接识别结果
        lines = [line[1][0] for line in result]
        context = "".join(lines)

        ocr_datas.append([context, data['qas']])

    save_nlp_datas(ocr_datas=ocr_datas, csv_datas=csv_datas, save_path='test.json')
if __name__=='__main__':
    main()