import pytest
import datetime
import math
from event import Event
from freezegun import freeze_time
from dateutil.tz import tzutc
from dateutil import parser


@pytest.fixture(params=[30, 25, 60, 55, 15])
def event(request):
    """
    Returns a mock event starting at 2022-01-01T00:00:00Z with data pre-populated

    Duration is determined by the param to allow for variable event durrations
    """

    start = datetime.datetime(2022, 1, 1, 0, 0, tzinfo=tzutc())
    end = start + datetime.timedelta(minutes=request.param)

    data = {
        'summary': 'Test',
        'start': {'dateTime': str(start)},
        'end': {'dateTime': str(end)},
        'status': 'confirmed',
        '_duration': request.param
    }

    return Event(data)


@pytest.fixture(params=[30, 15, 10, 5, 4, 3, 2, 1])
def minutes_to_display(request):
    """
    Fixture to iterate through times intended to display
    """
    return request.param


@pytest.fixture(params=[60, 59, 55, 51, 50, 49, 45, 41,
                40, 36, 35, 32, 27, 25, 22, 20, 11, 6])
def minutes_not_to_display(request):
    """
    Fixture to iterate through times not intended to display
    """
    return request.param


def test_stores_data(event):
    """
    Test that the data is stored
    """
    assert event.data["summary"] == "Test"


def test_title(event):
    """
    Test the title is stored
    """
    assert event.title() == "Test"


def test_start(event):
    """
    Test that the start time is parsed and stored
    """
    assert event.start() == datetime.datetime(2022, 1, 1, 0, 0, tzinfo=tzutc())


def test_end(event):
    """
    Test that the end time is parsed and stored
    """

    end = event.start() + datetime.timedelta(minutes=event.data["_duration"])
    assert event.end() == end


@freeze_time("2022-01-01 00:30:00Z")
def test_time_remaining(event):
    """
    Test that the time remaining is calculated correctly
    """
    half = datetime.timedelta(minutes=event.data["_duration"] / 2)
    with freeze_time(event.start() + half):
        assert event.time_remaining() == half


def test_durration(event):
    """
    Test that the durration is calculated correctly
    """
    assert event.durration() == datetime.timedelta(
        minutes=event.data["_duration"])


def test_perceived_durration(event):
    """
    Test that the perceived_durration is calculated correctly
    """

    if event.data["_duration"] in [25, 55]:
        expected = event.data["_duration"] + 5
    elif event.data["_duration"] == 50:
        expected = event.data["_duration"] + 10
    else:
        expected = event.data["_duration"]

    assert event.perceived_durration() == datetime.timedelta(minutes=expected)


@freeze_time("2022-01-01 00:15:00Z")
def test_in_progress(event):
    """
    Test that the event determined to be in progress correctly
    """
    assert event.in_progress()


def test_percent_remaining(event):
    """
    Test that the percent remaining is calculated correctly
    """
    half = event.perceived_durration() / 2
    with freeze_time(event.end() - half):
        assert event.percent_remaining() == 0.5


@freeze_time("2021-01-01 01:00:00Z")
def test_not_in_progress(event):
    """
    Test that the event determined to not be in progress correctly
    """
    assert not event.in_progress()


@freeze_time("2022-01-01 00:30:00Z")
def test_minutes_remaining(event):
    """
    Test that the minutes remaining is calculated correctly
    """
    half = datetime.timedelta(minutes=event.data["_duration"] / 2)
    with freeze_time(event.start() + half):
        assert event.minutes_remaining() == round(half.total_seconds() / 60)


def test_should_display_time(event, minutes_to_display):
    """
    Test times when the time should be displayed
    """

    diff = datetime.timedelta(
        minutes=event.data["_duration"]) - datetime.timedelta(minutes=minutes_to_display)
    with freeze_time(event.start() + diff):
        if not event.in_progress():
            return

        assert event.should_display_time() is True


def test_should_not_display_time(event, minutes_not_to_display):
    """
    Test times when the time should not be displayed
    """

    diff = datetime.timedelta(
        minutes=event.data["_duration"]) - datetime.timedelta(minutes=minutes_not_to_display)
    with freeze_time(event.start() + diff):
        if not event.in_progress():
            return

        assert event.should_display_time() is False
