from django import forms

from forum.models import Post, Thread


class NewThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ("subject",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Thread form has one visible field only
        self.visible_fields()[0].field.widget.attrs["class"] = "form-control"

    def save(self, slug=None, user=None, commit=True):
        thread = super().save(commit=False)
        thread.slug = slug
        thread.started_by = user
        if commit:
            thread.save()
        return thread


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("text",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].label = "Comment"
        # Post form has one visible field only
        self.visible_fields()[0].field.widget.attrs["class"] = "form-control"

    def save(self, thread=None, user=None, commit=True):
        post = super().save(commit=False)
        post.thread = thread
        post.written_by = user
        if commit:
            post.save()
        return post


class CombinedFormBase(forms.Form):
    form_classes = []

    def __init__(self, *args, **kwargs):
        super(CombinedFormBase, self).__init__(*args, **kwargs)
        for f in self.form_classes:
            name = self._attribute_name_from_class(f)
            setattr(self, name, f(*args, **kwargs))
            form = getattr(self, name)
            self.fields.update(form.fields)
            self.initial.update(form.initial)

    def _attribute_name_from_class(self, cls):
        name = ""
        for i, v in enumerate(cls.__name__):
            name += v if v == v.lower() else f"_{v.lower()}" if i else v.lower()
        return name

    def is_valid(self):
        is_valid = True
        for f in self.form_classes:
            name = self._attribute_name_from_class(f)
            form = getattr(self, name)
            if not form.is_valid():
                is_valid = False
        # is_valid will trigger clean method,
        # so it should be called after all other forms is_valid are called
        # otherwise clean_data will be empty
        if not super(CombinedFormBase, self).is_valid():
            is_valid = False
        for f in self.form_classes:
            name = self._attribute_name_from_class(f)
            form = getattr(self, name)
            self.errors.update(form.errors)
        return is_valid

    def clean(self):
        cleaned_data = super(CombinedFormBase, self).clean()
        for f in self.form_classes:
            name = self._attribute_name_from_class(f)
            form = getattr(self, name)
            cleaned_data.update(form.cleaned_data)
        return cleaned_data


class StartNewThreadForm(CombinedFormBase):
    new_post_form = new_thread_form = None
    form_classes = (NewThreadForm, NewPostForm)


class AddNewPostForm(CombinedFormBase):
    new_post_form = None
    form_classes = (NewPostForm,)
