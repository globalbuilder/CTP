# apps/evaluations/forms.py

from django import forms
from .models import Evaluation, EvaluationItem, EvaluationTemplate, EvaluationCriteria
from django.forms import inlineformset_factory

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['template', 'comments']
        widgets = {
            'template': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'template': 'نموذج التقييم',
            'comments': 'التعليقات',
        }

EvaluationItemFormSet = inlineformset_factory(
    Evaluation,
    EvaluationItem,
    fields=('criteria', 'score'),
    extra=0,
    widgets={
        'criteria': forms.Select(attrs={'class': 'form-control'}),
        'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
    },
    labels={
        'criteria': 'المعيار',
        'score': 'الدرجة',
    }
)

# Dynamically generate formset based on selected template
def get_evaluation_item_formset(template):
    criteria = template.criteria.all()
    EvaluationItemFormSet = inlineformset_factory(
        Evaluation,
        EvaluationItem,
        fields=('criteria', 'score'),
        extra=0,
        widgets={
            'criteria': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        },
        labels={
            'criteria': 'المعيار',
            'score': 'الدرجة',
        }
    )
    return EvaluationItemFormSet
