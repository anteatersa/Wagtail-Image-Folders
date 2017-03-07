from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from wagtail.wagtailadmin.utils import PermissionPolicyChecker
from wagtail.wagtailimages.models import get_folder_model
from wagtail.wagtailimages.forms import get_folder_form
from wagtail.wagtailimages.permissions import permission_policy

permission_checker = PermissionPolicyChecker(permission_policy)


@permission_checker.require('add')
def add(request, add_to_folder=False):
    ImageFolder = get_folder_model()
    ImageFolderForm = get_folder_form(ImageFolder)

    parent_folder = False
    if add_to_folder:
        parent_folder = get_object_or_404(ImageFolder, id=add_to_folder)

    if request.method == 'POST':
        # Build a form for validation
        form = ImageFolderForm(request.POST)

        if form.is_valid():
            error = False

            folder = ImageFolder(
                title=form.cleaned_data['title'].strip()
            )
            if parent_folder:
                folder.folder = parent_folder

            try:
                # Check if the folder is present in the DB or physically present in the OS
                folder.validate_folder()
            except ValidationError as e:
                error = True
                form._errors['title'] = e.message

        if not error:
            # Save folder
            folder.save()

            # Success! Send back to index or image specific folder
            response = redirect('wagtailimages:index')
            response['Location'] += '?folder={0}'.format(folder.id)
            return response
        else:
            # Validation error
            return render(request, 'wagtailimages/folder/add.html', {
                'error_message': 'Error adding folder',
                'help_text': '',
                'parent_folder': parent_folder,
                'form': form,
            })
    else:
        form = ImageFolderForm()

        return render(request, 'wagtailimages/folder/add.html', {
            'help_text': '',
            'parent_folder': parent_folder,
            'form': form,
        })


@permission_checker.require('change')
def edit(request, folder_id):
    ImageFolder = get_folder_model()
    ImageFolderForm = get_folder_form(ImageFolder)
    folder = get_object_or_404(ImageFolder, id=folder_id)

    if request.method == 'POST':
        # Build a form for validation
        form = ImageFolderForm(request.POST)

        if form.is_valid():

            folder.title = form.cleaned_data['title']

            try:
                # Check if the folder is present in the DB or physically present in the OS
                folder.validate_folder()
            except ValidationError as e:
                form._errors['title'] = e.message
                # Validation error
                return render(request, 'wagtailimages/folder/edit.html', {
                    'error_message': 'Error adding folder',
                    'help_text': '',
                    'form': form,
                })

            folder.save()

            # Success! Send back to index or image specific folder
            response = redirect('wagtailimages:index')
            response['Location'] += '?folder={0}'.format(folder.id)
            return response
        else:
            # Validation error
            return render(request, 'wagtailimages/folder/edit.html', {
                'error_message': 'Error adding folder',
                'help_text': '',
                'form': form,
            })
    else:
        form = ImageFolderForm(instance=folder)

    return render(request, 'wagtailimages/folder/edit.html', {
        'help_text': '',
        'folder': folder,
        'form': form,
    })


@permission_checker.require('change')
def delete(request, folder_id):
    ImageFolder = get_folder_model()
    folder = get_object_or_404(ImageFolder, id=folder_id)

    if request.method == 'POST':
        # POST if confirmation of delete

        # try find a parent folder
        parent_folder = folder.get_parent()

        # Delete folder
        folder.delete()

        # Success! Send back to index or image specific folder
        response = redirect('wagtailimages:index')
        if parent_folder:
            response['Location'] += '?folder={0}'.format(parent_folder.id)
        return response

    return render(request, 'wagtailimages/folder/confirm_delete.html', {
        'folder': folder,
        # 'form': form,
    })
