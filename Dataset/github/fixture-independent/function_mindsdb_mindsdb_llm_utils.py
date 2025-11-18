from typing import List, Tuple
import re
import numpy as np
import pandas as pd

def get_completed_prompts(base_template: str, df: pd.DataFrame, strict=True) -> Tuple[List[str], np.ndarray]:
    columns = []
    spans = []
    matches = list(re.finditer('{{(.*?)}}', base_template))
    if len(matches) == 0:
        if strict:
            raise AssertionError('No placeholders found in the prompt, please provide a valid prompt template.')
        prompts = [base_template] * len(df)
        return (prompts, np.ndarray(0))
    first_span = matches[0].start()
    last_span = matches[-1].end()
    for m in matches:
        columns.append(m[0].replace('{', '').replace('}', ''))
        spans.extend((m.start(), m.end()))
    spans = spans[1:-1]
    template = [base_template[s:e] for s, e in list(zip(spans, spans[1:]))[::2]]
    template.insert(0, base_template[0:first_span])
    template.append(base_template[last_span:])
    empty_prompt_ids = np.where(df[columns].isna().all(axis=1).values)[0]
    df['__mdb_prompt'] = ''
    for i in range(len(template)):
        atom = template[i]
        if i < len(columns):
            col = df[columns[i]].replace(to_replace=[None], value='')
            df['__mdb_prompt'] = df['__mdb_prompt'].apply(lambda x: x + atom) + col.astype('string')
        else:
            df['__mdb_prompt'] = df['__mdb_prompt'].apply(lambda x: x + atom)
    prompts = list(df['__mdb_prompt'])
    return (prompts, empty_prompt_ids)