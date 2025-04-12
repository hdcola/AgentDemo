import json
import os
from typing import Dict, List, Any, Optional


def read_form_schema(file_path: str) -> Optional[List[Dict[str, Any]]]:
    """
    读取表单字段定义的JSON文件，如果文件不存在则创建

    Args:
        file_path: JSON文件路径

    Returns:
        表单字段列表，每个字段是包含name、type、required等属性的字典
        如果解析出错，返回None
    """
    try:
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}，创建新文件")
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # 创建空的表单结构
            empty_schema = []
            # 写入空结构到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(empty_schema, f, ensure_ascii=False, indent=2)
            return empty_schema

        with open(file_path, 'r', encoding='utf-8') as f:
            form_schema = json.load(f)
            return form_schema
    except json.JSONDecodeError:
        print(f"JSON格式错误: {file_path}")
        return None
    except Exception as e:
        print(f"读取文件出错: {e}")
        return None


def write_form_schema(file_path: str, form_schema: List[Dict[str, Any]]) -> bool:
    """
    将表单字段定义写入JSON文件

    Args:
        file_path: 要写入的JSON文件路径
        form_schema: 表单字段列表，每个字段是包含name、type、required、description等属性的字典
                    description属性用于说明该表单字段的用途或者填写要求

    Returns:
        bool: 写入成功返回True，否则返回False
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(form_schema, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"写入文件出错: {e}")
        return False


# 使用示例
if __name__ == "__main__":
    # 示例表单字段
    example_schema = [
        {
            "name": "username",
            "type": "string",
            "required": True,
            "description": "用户名，长度需在3-20个字符之间"
        },
        {
            "name": "age",
            "type": "number",
            "required": False,
            "description": "年龄，请输入正整数"
        },
        {
            "name": "email",
            "type": "string",
            "required": True,
            "description": "电子邮箱地址，用于接收通知"
        }
    ]

    file_path = "./form_schema.json"
    # 写入示例数据
    if write_form_schema(file_path, example_schema):
        print(f"表单结构已写入: {file_path}")

    # 读取数据
    loaded_schema = read_form_schema(file_path)
    if loaded_schema:
        print("读取的表单结构:")
        for field in loaded_schema:
            print(
                f"- {field['name']} ({field['type']}): {'必填' if field.get('required') else '选填'}")
            print(f"  说明: {field.get('description', '无')}")
