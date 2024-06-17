from django.shortcuts import render
#from .token_analysis_model import TokenAnalysisModel
import os
import pickle
import torch
from transformers import BertTokenizer, BertModel
from django.http import JsonResponse
from .models import TokenAnalysis

def load_model():
    with open('token_analysis_model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

def load_bert():
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    bert_model = BertModel.from_pretrained('bert-base-uncased')
    return tokenizer, bert_model

def analyze_token(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        
        tokenizer, bert_model = load_bert()
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        outputs = bert_model(**inputs)
        features = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        
        model = load_model()
        predictions = model.predict(features)[0]
        
        #return JsonResponse({'prediction': int(prediction)})
        return render(request, 'token_feature_analysis_result.html', {'predictions': predictions})

    return render(request, 'token_feature_analysis.html')

def token_analyis(request, symbol):
    token = TokenAnalysis.objects.get(symbol=symbol) # get the token Ex: Bitcoin
    context = {
        'token': token,
    }
    return render(request, 'token_analysis.html', context)

def token_search(request):
    query = request.GET.get('query', '')
    if query:
        tokens = TokenAnalysis.objects.filter(name__icontains=query)[:6]
        results = [{'name': token.name, 'symbol': token.symbol} for token in tokens]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


# def analyze_token(request):
#     if request.method == 'POST':
#         document = request.POST['document']
#         aspect = request.POST['aspect']
#         model = TokenAnalysisModel()
#         predictions = model.predict([document], aspect)
#         return render(request, 'token_analysis_result.html', {'predictions': predictions})
#     return render(request, 'token_analysis.html')
