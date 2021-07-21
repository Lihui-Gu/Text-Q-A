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
            question_id, question, answer = qa
            start = context.find(answer)
            if start==-1:
                continue
            qa = {
                "question": question,
                "id": question_id, 
                "answers": [
                    {
                        "text": answer, 
                        "answer_start": start
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
    with open('data/train-utf8.csv', 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i==0:
                continue
            index, question_id, filename, question, answer = row

            if filename in csv_datas:
                csv_datas[filename]['qas'].append([question_id, question, answer])
            else:
                csv_datas[filename] = {
                    'qas':[[question_id, question, answer]]
                }


    # 加载 OCR 模型
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    ocr_datas = []
    for filename, data in csv_datas.items():
        img_path = 'data/image/%s' % filename

        # ocr 识别
        result = ocr.ocr(img_path, cls=True)

        # 拼接识别结果
        lines = [line[1][0] for line in result]
        context = "".join(lines)

        ocr_datas.append([context, data['qas']])


    # 转换并保存数据集
    # 最后 200 张图像作为验证集
    save_nlp_datas(ocr_datas=ocr_datas[:-200], csv_datas=csv_datas, save_path='train.json')
    save_nlp_datas(ocr_datas=ocr_datas[-200:], csv_datas=csv_datas, save_path='dev.json')

if __name__=='__main__':
    main()