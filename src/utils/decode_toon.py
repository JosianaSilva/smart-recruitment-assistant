import json
import re
from typing import Any, Dict, List, Union

def decode_toon_to_json(toon_string: str) -> str:
    """
    Decodifica uma string no formato TOON e retorna como JSON.
    
    Args:
        toon_string: String no formato TOON
        
    Returns:
        String JSON formatada
    """
    try:
        decoded_data = _parse_toon(toon_string)
        
        json_output = json.dumps(decoded_data, indent=2, ensure_ascii=False)
        
        return json_output
    
    except Exception as e:
        raise ValueError(f"Erro ao decodificar TOON: {str(e)}")

def _parse_toon(toon_string: str) -> Dict[str, Any]:
    """
    Parse interno do formato TOON.
    """
    result = {}
    lines = toon_string.strip().split('\n')
    current_parent = None
    
    for line in lines:
        original_line = line
        line = line.strip()
        if not line:
            continue
        
        indent_level = len(original_line) - len(original_line.lstrip())
        
        # Parse de arrays
        array_match = re.match(r'^(\w+)\[(\d+)\]:\s*(.+)$', line)
        if array_match:
            key, count, values = array_match.groups()
            value_list = [v.strip() for v in values.split(',')]
            
            if indent_level > 0 and current_parent:
                result[current_parent][key] = value_list
            else:
                result[key] = value_list
            continue
        
        # Parse de objetos aninhados
        if line.endswith(':'):
            key = line[:-1].strip()
            if indent_level == 0:
                result[key] = {}
                current_parent = key
            continue
            
        # Parse de propriedades de objetos
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if indent_level > 0 and current_parent:
                result[current_parent][key] = _convert_value(value)
            else:
                result[key] = _convert_value(value)
    
    return result

def _convert_value(value: str) -> Union[str, int, float, bool]:
    """
    Converte string para o tipo apropriado.
    """
    if value.lower() == 'true':
        return True
    if value.lower() == 'false':
        return False
    
    try:
        if '.' in value:
            return float(value)
        return int(value)
    except ValueError:
        pass

    return value
