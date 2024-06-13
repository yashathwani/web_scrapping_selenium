import json

import torch
import os
import warnings
from transformers import BertTokenizer, BertModel


os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore", message="`huggingface_hub` cache-system uses symlinks.*")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
# texts = ["my name is yash ", "Scaler School of technology"]


# def get_bert_embeddings(texts):
#     embeddings = []
#     for text in texts:
def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    token_embeddings = outputs.last_hidden_state
    mean_embeddings = torch.mean(token_embeddings, dim=1).squeeze().tolist()
    return json.dumps(mean_embeddings)

#     print(mean_embeddings)
#     # embeddings.append(mean_embeddings)
# return torch.stack(embeddings)
