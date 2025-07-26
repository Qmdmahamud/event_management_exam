from django import forms
from tasks.models import Task
# from tasks.forms import StyledFormMIxin

class StyledFormMixin:
    default_classes="border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-300 focus:ring-rose-500 "
    def apply_styled_widges(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter {field.label.lower()}",
                    'rows':5
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':"space-y-2"
                    
                })
            else:
                field.widget.attrs.update({
                    'class':self.default_classes
                })
class TaskForm(forms.Form):
    title=forms.CharField(max_length=250)
    description=forms.CharField(widget=forms.Textarea,label='Task Description')
    due_date=forms.DateField(widget=forms.SelectDateWidget,label="Due Date")
    assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[])


    def __init__(self,*args,**kwargs):
        employees=kwargs.pop("employees",[])
        super().__init__(*args,**kwargs)
        self.fields['assigned_to'].choices=[(emp.id,emp.name) for emp in employees]


class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields=['title','description','due_date','assigned_to']
        widgets={
            'due_date':forms.SelectDateWidget(),
            'assigned_to':forms.CheckboxSelectMultiple(),
        }
        # widgets={
        #     'title':forms.TextInput(attrs={
        #         'class':"border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-300 focus:ring-rose-500 " ,
        #         'placeholder':"Enter a Task Titel"
                
        #     }),
        #     'description':forms.Textarea(attrs={
        #         'class':"border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-300 focus:ring-rose-500 " ,
        #         'placeholder':"Descripbe the Task"}),
        #         'rows':5,
        #     'due_date':forms.SelectDateWidget(
        #         attrs={
        #         'class':"border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-300 focus:ring-rose-500 " ,
        #         }
        #     ),
        #     'assigned_to':forms.CheckboxSelectMultiple(attrs={
        #         'class':"border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-300 focus:ring-rose-500 " ,
        #         }
        #     )
        # }
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widges()
