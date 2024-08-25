from behave import given, when, then
from django.urls import reverse
from django.test import Client


@given('I am on the homepage')
def step_impl(context):
    context.client = Client()
    context.response = context.client.get(reverse('siedlung_home'))
    assert context.response.status_code == 200


@when('I click the "Create Siedlung" button')
def step_impl(context):
    context.response = context.client.get(reverse('siedlung_create'))
    assert context.response.status_code == 200


@when('I am on the Siedlung creation page')
def step_impl(context):
    assert 'Neue Siedlung' in context.response.content.decode()


@when('I fill in the Siedlung details')
def step_impl(context):
    context.siedlung_data = {
        'internal_id': 'DOG',
        'bezeichnung': 'Doghausen',
        'anlagewert': '1500200',
        'versicherungswert': '1510000',
        'baurechtszins': '15000',
        'betriebsquote_zuschlag': '1.25'
    }


@when('I click the "Save" button')
def step_impl(context):
    context.response = context.client.post(reverse('siedlung_create'), data=context.siedlung_data)
    assert context.response.status_code == 302  # Expecting a redirect


@then('I should be redirected to the Siedlung home page')
def step_impl(context):
    assert context.response.url == reverse('siedlung_home')


@then('I should see the newly created Siedlung listed')
def step_impl(context):
    response = context.client.get(reverse('siedlung_home'))
    assert 'DOG' in response.content.decode()
