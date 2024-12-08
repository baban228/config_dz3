
import yaml
import re
import sys


def parse_yaml(input_text):
    try:
        return yaml.safe_load(input_text)
    except yaml.YAMLError as exc:
        print(f"Ошибка синтаксиса YAML: {exc}")
        sys.exit(1)


def convert_to_custom_language(data, consts=None):

    if isinstance(data, dict):
        return convert_dict(data, consts)
    elif isinstance(data, list):
        return convert_list(data, consts)
    elif isinstance(data, str):
        return f'"{data}"'
    elif isinstance(data, (int, float)):
        return str(data)
    else:
        raise ValueError("Неизвестный тип данных")


def convert_dict(data, consts=None):

    result = "@{\n"
    for key, value in data.items():
        if key == "consts":
            result += convert_consts(value)
        elif key == "calculation":
            result += f"  {key} = {convert_expression(value, consts)};\n"
        else:
            result += f"  {key} = {convert_to_custom_language(value, consts)};\n"
    result += "}"
    return result


def convert_list(data, consts=None):
    return "[" + " ".join([convert_to_custom_language(item, consts) for item in data]) + "]"


def convert_consts(consts):
    result = ""
    for name, value in consts.items():
        result += f"  const {name} = {convert_to_custom_language(value)};\n"
    return result


def convert_expression(expression, consts):
    expr = expression.strip()
    if expr.startswith('^') and expr.endswith(']'):
        a = expr[2:-1]
        result = eval(a, consts)
        return f"{result}"
    else:
        raise ValueError(f"Некорректное выражение: {expr}")

def process_comments(input_text):
    lines = input_text.splitlines()
    result_lines = []

    for line in lines:
        if line.strip().startswith("#"):
            comment = line.strip()[1:].strip()
            if len(comment) > 50:
                result_lines.append(f"+/{comment}/+")
            else:
                result_lines.append(f"//{comment}")

    return "\n".join(result_lines)

def process_yaml(input_text):

    data = parse_yaml(input_text)

    consts = data.get("consts", {})

    output_lines = []
    if "consts" in data:
        output_lines.append(convert_consts(data["consts"]))
    for key, value in data.items():
        if key != "consts":
            output_lines.append(f"{key}: {convert_to_custom_language(value, consts)}")

    return "\n".join(output_lines)


if __name__ == "__main__":
    input_text = sys.stdin.read()

    try:
        output = process_yaml(input_text)
        input_text_with_comments = process_comments(input_text)
        output_with_comments = output + "\n" + input_text_with_comments
        print(output_with_comments)

    except ValueError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
