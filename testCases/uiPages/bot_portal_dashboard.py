import re
from faker import Faker
from autoUtils.optionUtil import generate_autotest_object_name
from testCases.uiPages.base_page import BasePage

fake = Faker()

class BotPortalDashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.path = "/bot/dashboard/"

        # self.refresh_button = self.page.locator("svg").locator("title", has_text="refresh")
        self.chatbot_in_livechat_button = self.page.get_by_text("Chatbot Usage in Live Chat")
        self.chatbot_in_ticket_button =  self.page.get_by_text("Chatbot Usage in Ticketing & Messaging")
        self.new_tips = self.page.get_by_text("News & Tips")
        # self.chatbot_chats = self.page.get_by_text("Chatbot Chats")
        self.last_7_days = self.page.get_by_text("Last 7 Days")
        # self.chatbot_only_chat = self.page.get_by_text("Chatbot Only Chats")