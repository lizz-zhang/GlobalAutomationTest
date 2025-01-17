import datetime
import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://dash11.comm100.io/login")
    page.locator('input[name="email"]').click()
    page.locator('input[name="password"]').click()
    page.get_by_role("button", name="Sign in").click()


def test_clock(page: Page):
    # Initialize clock with some time before the test time and let the page load
    # naturally. `Date.now` will progress as the timers fire.
    page.clock.install(time=datetime.datetime(2024, 2, 2, 8, 0, 0))
    page.clock.set_fixed_time(datetime.datetime(2024, 2, 2, 8, 0, 0))
    page.goto("http://127.0.0.1:5500/index.html")

    # Pretend that the user closed the laptop lid and opened it again at 10am.
    # Pause the time once reached that point.
    page.clock.pause_at(datetime.datetime(2024, 2, 2, 10, 0, 0))

    # Assert the page state.
    expect(page.get_by_test_id("current-time")).to_have_text("2/2/2024, 10:00:00 AM")

    # Close the laptop lid again and open it at 10:30am.
    page.clock.fast_forward("30:00")
    expect(page.get_by_test_id("current-time")).to_have_text("2/2/2024, 10:30:00 AM")


def test_clock_inactvity_timeout(page: Page):

    # Initial time does not matter for the test, so we can pick current time.
    page.clock.install()
    page.goto("http://127.0.0.1:5500/inactivity_timeout.html")
    # Interact with the page
    page.get_by_role("button").click()

    # Fast forward time 5 minutes as if the user did not do anything.
    # Fast forward is like closing the laptop lid and opening it after 5 minutes.
    # All the timers due will fire once immediately, as in the real browser.
    page.clock.fast_forward("05:00")

    # Check that the user was logged out automatically.
    expect(
        page.get_by_text("You have been logged out due to inactivity.")
    ).to_be_visible()
