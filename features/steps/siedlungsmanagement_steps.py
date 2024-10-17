import random
import string
import sys

from behave import given, when, then
from django.urls import reverse
from django.test import Client
from siedlungsmanager.models import Siedlung, Objekt


# TODO Extract into utility class RandomHelper
def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


def generate_random_number(min_val, max_val):
    return random.randint(min_val, max_val)


def generate_random_percentage(min_val, max_val):
    return round(random.uniform(min_val, max_val), 2)


def generate_random_currency_value(min_val, max_val):
    whole_number = random.randint(min_val, max_val)
    first_decimal = random.randint(0, 9)
    second_decimal = random.choice([0, 5])
    return whole_number + 0.1 * first_decimal + 0.01 * second_decimal


def random_punkte_choice():
    # Get just the values (first item of each tuple) from PUNKTE_CHOICES
    punkte_values = [choice[0] for choice in Objekt.PUNKTE_CHOICES]
    return random.choice(punkte_values)


# TODO Extract into utility class ResponseAssertions
def assert_status_code(response, expected_status=200, message="Failed to navigate to page"):
    assert response.status_code == expected_status, (f"{message}. "
                                                     f"Status code: {response.status_code}. "
                                                     f"Expected: {expected_status}")


@given('I am on the homepage')
def step_impl(context):
    context.client = Client()
    # get url with django reverse function
    # returns a real url
    url = reverse('siedlung_home')
    # get url and save response within context
    context.response = context.client.get(url)
    assert_status_code(context.response, message="Failed to navigate to homepage")


@given('I am on the Siedlung details')
def step_impl(context):
    context.client = Client()
    url = reverse('siedlung_detail', args=[context.siedlung.pk])
    context.response = context.client.get(url)
    assert_status_code(context.response, message="Failed to navigate to Siedlung page")


@given('an existing Siedlung without Objekt')
def step_impl(context):
    siedlung = Siedlung.objects.create(
        internal_id=generate_random_string(5),
        bezeichnung=generate_random_string(20),
        anlagewert=generate_random_number(0, sys.maxsize),
        versicherungswert=generate_random_number(0, sys.maxsize),
        baurechtszins=generate_random_number(0, sys.maxsize),
        betriebsquote_zuschlag=generate_random_percentage(0, 100),
    )

    # add siedlung to context
    context.siedlung = Siedlung.objects.get(internal_id=siedlung.internal_id)


@when('I navigate to the homepage')
def step_impl(context):
    # TODO create helper for url making so the I navigate to is reusable
    url = reverse('siedlung_home')
    context.response = context.client.get(url)
    assert_status_code(context.response, message="Failed to navigate to homepage")


@when("I create a Siedlung")
def step_impl(context):
    context.response = context.client.get(reverse('siedlung_create'))
    assert_status_code(context.response, message="Failed to navigate to Siedlung create page")


@when("I fill in the Siedlung details")
def step_impl(context):
    assert 'Neue Siedlung' in context.response.content.decode()
    context.siedlung_data = {
        'internal_id': generate_random_string(5),
        'bezeichnung': generate_random_string(50),
        'anlagewert': generate_random_number(0, sys.maxsize),
        'versicherungswert': generate_random_number(0, sys.maxsize),
        'baurechtszins': generate_random_number(0, sys.maxsize),
        'betriebsquote_zuschlag': generate_random_percentage(0, 100)
    }
    # save target siedlung for later assert
    context.target_siedlung = context.siedlung_data['internal_id']


@when("I save the Siedlung")
def step_impl(context):
    context.response = context.client.post(reverse('siedlung_create'), data=context.siedlung_data)
    # Expecting a redirect
    assert_status_code(context.response, expected_status=302, message="Failed to save the Siedlung")


@when('I create a new Objekt')
def step_impl(context):
    # check if in context of siedlung
    assert context.siedlung.internal_id in context.response.content.decode()
    url = reverse('objekt_create', args=[context.siedlung.pk])
    context.response = context.client.get(url)
    assert_status_code(context.response, message="Failed to navigate to Objekt create page.")

    # Initialize an empty dictionary to store form data
    context.form_data = {}


@when('I define the Bereich {bereich_type}')
def step_impl(context, bereich_type):
    assert 'Neues Objekt' in context.response.content.decode()
    context.form_data['bereich'] = bereich_type


@when('I fill in the other Objekt details')
def step_impl(context):
    context.form_data.update({
        'internal_oid': generate_random_string(10),
        'bezeichnung': generate_random_string(40),
        'punkte': random_punkte_choice(),
        'aktuelle_miete': generate_random_currency_value(500, 15000)
    })


@when('I save the Objekt')
def step_impl(context):
    url = reverse('objekt_create', args=[context.siedlung.pk])
    context.response = context.client.post(url, data=context.form_data)
    assert_status_code(context.response, expected_status=302, message="Failed to save the Objekt")

    # get saved Objekt from DB
    context.objekt = Objekt.objects.get(internal_oid=context.form_data['internal_oid'])
    assert context.objekt is not None, "Objekt was not found in the database"
    context.target_objekt = context.objekt.internal_oid


@then('I am redirected to the homepage')
def step_impl(context):
    assert context.response.url == reverse('siedlung_home')


@then('I am redirected to the Siedlung details')
def step_impl(context):
    url = reverse('siedlung_detail', args=[context.siedlung.pk])
    assert context.response.url == url


@then("the Objekt is in the list of all Objekte on the {page}-page")
def step_impl(context, page):
    if page == 'home':
        url = reverse('siedlung_home')
    elif page == 'Siedlung-Detail':
        url = reverse('siedlung_detail', args=[context.siedlung.pk])
    else:
        raise ValueError(f"Unknown page: {page}")

    response = context.client.get(url)
    assert context.target_objekt in response.content.decode(), f"Objekt not found on the {page}-page"


@then("the Siedlung is in the list of all Siedlungen")
def step_impl(context):
    response = context.client.get(reverse('siedlung_home'))
    assert context.target_siedlung in response.content.decode()

