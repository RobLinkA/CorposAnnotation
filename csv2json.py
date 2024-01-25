import csv
import json
import os
import ast

def convert_tags_to_int_list(tag_str):
    try:
        # 使用ast.literal_eval安全地将字符串转换为列表
        tag_list = ast.literal_eval(tag_str)
        return [int(tag) for tag in tag_list]
    except:
        # 如果转换失败，则返回空列表
        return []

def convert_row(row):
    new_row = {}
    for key, value in row.items():
        # 对于tags字段进行特殊处理
        if key == 'tags':
            new_row[key] = convert_tags_to_int_list(value)
        else:
            new_row[key] = value
    return new_row

def convert_csv_to_json_v2(csv_file_path):
    json_data = {
        "version": 2,
        "data": {
            "api::collection-name.collection-name": {}
        }
    }

    with open(csv_file_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # 转换每一行，并确保id为整数
            converted_row = convert_row(row)
            key = int(row['id'])
            json_data["data"]["api::collection-name.collection-name"][key] = converted_row

    return json_data

def main():
    for file in os.listdir('.'):
        if file.endswith('.csv'):
            json_data = convert_csv_to_json_v2(file)
            json_file_name = file.replace('.csv', '.json')
            with open(json_file_name, 'w', encoding='utf-8') as jsonfile:
                json.dump(json_data, jsonfile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
