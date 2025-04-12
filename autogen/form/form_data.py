import json
import os
from typing import Dict, Any
import sys
import os.path

# 导入表单结构模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def read_form_data(file_path: str) -> Dict[str, Any]:
    """
    读取用户已填写的表单数据，如果文件不存在则创建空表单

    Args:
        file_path: 表单数据文件路径

    Returns:
        Dict: 表单数据字典，键为字段名，值为用户填写的数据
    """
    try:
        if not os.path.exists(file_path):
            print(f"表单数据文件不存在: {file_path}，创建新文件")
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # 创建空的表单数据
            empty_form_data = {}
            # 写入空数据到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(empty_form_data, f, ensure_ascii=False, indent=2)
            return empty_form_data

        with open(file_path, 'r', encoding='utf-8') as f:
            form_data = json.load(f)
            return form_data
    except json.JSONDecodeError:
        print(f"JSON格式错误: {file_path}")
        return {}
    except Exception as e:
        print(f"读取表单数据出错: {e}")
        return {}


def update_form_field(file_path: str, field_name: str, field_value: Any) -> bool:
    """
    更新表单中的一个字段数据，如果文件不存在则创建

    Args:
        file_path: 表单数据文件路径
        field_name: 要更新的字段名
        field_value: 字段的新值

    Returns:
        bool: 更新成功返回True，否则返回False
    """
    try:
        # 先读取现有数据
        form_data = read_form_data(file_path)

        # 更新字段值
        form_data[field_name] = field_value

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(form_data, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"更新表单字段出错: {e}")
        return False


def validate_form_data(schema_path: str, data_path: str) -> Dict[str, str]:
    """
    验证表单数据是否符合表单结构定义

    Args:
        schema_path: 表单结构文件路径
        data_path: 表单数据文件路径

    Returns:
        Dict[str, str]: 验证结果，键为字段名，值为验证结果描述
    """
    validation_results = {}

    # 读取表单结构和数据
    schema = read_form_schema(schema_path)
    data = read_form_data(data_path)

    if not schema:
        return {"error": "无法读取表单结构"}

    for field in schema:
        field_name = field['name']
        if field.get('required', False) and field_name not in data:
            validation_results[field_name] = "必填字段未填写"
        elif field_name in data:
            # 可以添加更多类型验证逻辑
            validation_results[field_name] = "已正确填写"

    return validation_results


# 使用示例
if __name__ == "__main__":
    form_schema_path = "./form_schema.json"
    form_data_path = "./form_data.json"

    # 填写表单字段
    update_form_field(form_data_path, "username", "张三")
    print("已更新用户名字段")

    update_form_field(form_data_path, "age", 28)
    print("已更新年龄字段")

    update_form_field(form_data_path, "email", "zhangsan@example.com")
    print("已更新邮箱字段")

    # 读取已填写的表单数据
    filled_form = read_form_data(form_data_path)
    print("\n已填写的表单数据:")
    for field_name, field_value in filled_form.items():
        print(f"- {field_name}: {field_value}")

    # 验证表单数据
    validation_results = validate_form_data(form_schema_path, form_data_path)
    print("\n表单验证结果:")
    for field_name, result in validation_results.items():
        print(f"- {field_name}: {result}")
