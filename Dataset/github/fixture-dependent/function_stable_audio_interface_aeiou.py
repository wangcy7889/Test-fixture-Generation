from einops import rearrange
import numpy as np

def embeddings_table(tokens):
    from wandb import Table
    from pandas import DataFrame
    features, labels = ([], [])
    embeddings = rearrange(tokens, 'b d n -> b n d')
    for i in range(embeddings.size()[0]):
        for j in range(embeddings.size()[1]):
            features.append(embeddings[i, j].detach().cpu().numpy())
            labels.append([f'demo{i}'])
    features = np.array(features)
    labels = np.concatenate(labels, axis=0)
    cols = [f'dim_{i}' for i in range(features.shape[1])]
    df = DataFrame(features, columns=cols)
    df['LABEL'] = labels
    return Table(columns=df.columns.to_list(), data=df.values)