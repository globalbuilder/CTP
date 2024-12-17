# apps/evaluations/forms.py

from django import forms
from .models import Evaluation, SCORE_CHOICES

STUDENT_CRITERIA = [
    "المحافظة على أوقات الدوام.",
    "الالتزام بإجراءات وأنظمة العمل.",
    "المظهر العام للمتدرب.",
    "إنجاز ما يكلف به المتدرب بشكل مناسب.",
    "المرونة والقدرة على التكيف.",
    "التعامل مع الزملاء والمدربين.",
    "القدرة على استيعاب المعلومات.",
    "القدرة على تحمل المسؤولية.",
    "المبادرة والقدرة على الابتكار والإبداع.",
    "الحرص على جدية التدريب.",
]

ENTITY_CRITERIA = [
    "جدية التدريب.",
    "الخبرة التي يقدمها التدريب.",
    "مناسبة مكان التدريب.",
    "خبرة مسؤولة التدريب.",
    "جدية مسؤولة التدريب.",
    "الوقت المخصص للتدريب.",
    "متابعة خطة التدريب.",
    "مساعدة موظفات الجهة التدريبية.",
    "الاستفادة من برنامج التدريب العملي.",
    "مدى توافق برنامج التدريب مع التخصص.",
]

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
            'comments',
            'c1_score', 'c2_score', 'c3_score', 'c4_score', 'c5_score',
            'c6_score', 'c7_score', 'c8_score', 'c9_score', 'c10_score'
        ]
        widgets = {
            'comments': forms.Textarea(attrs={'class': 'form-control'}),
            'c1_score': forms.RadioSelect(choices=SCORE_CHOICES),
            'c2_score': forms.RadioSelect(choices=SCORE_CHOICES),
            'c3_score': forms.RadioSelect(choices=SCORE_CHOICES),
            'c4_score': forms.RadioSelect(choices=SCORE_CHOICES),
            'c5_score': forms.RadioSelect(choices=SCORE_CHOICES),
            'c6_score': forms.RadioSelect(choices=SCORE_CHOICES),
            'c7_score': forms.RadioSelect(choices=SCORE_CHOICES),
            'c8_score': forms.RadioSelect(choices=SCORE_CHOICES),
            'c9_score': forms.RadioSelect(choices=SCORE_CHOICES),
            'c10_score': forms.RadioSelect(choices=SCORE_CHOICES),
        }
        labels = {
            'comments': 'التعليقات',
        }

    def __init__(self, *args, **kwargs):
        self.evaluation_type = kwargs.pop('evaluation_type', 'student')
        super().__init__(*args, **kwargs)

        if self.evaluation_type == 'student':
            criteria = STUDENT_CRITERIA
        else:
            criteria = ENTITY_CRITERIA

        # Assign labels dynamically to criteria fields
        for i in range(1, 11):
            self.fields[f'c{i}_score'].label = criteria[i-1]
