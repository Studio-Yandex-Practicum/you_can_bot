import json
import logging
import os
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import sentry_sdk
from sentry_sdk.transport import Transport
from telegram.error import BadRequest
from telegram.ext import ConversationHandler

from utils.error_handler import handle_error
from utils.monitoring import configure_monitoring


class RecordingTransport(Transport):
    def __init__(self):
        super().__init__()
        self.events = []

    def capture_envelope(self, envelope):
        for item in envelope.items:
            if item.type == "event":
                self.events.append(item.payload.json)


class MonitoringTests(IsolatedAsyncioTestCase):
    def setUp(self):
        self.previous_client = sentry_sdk.get_client()
        self.scope = sentry_sdk.isolation_scope()
        self.scope.__enter__()
        with patch.dict(os.environ, {"SENTRY_DSN": "http://key@localhost/1"}):
            configure_monitoring()
        self.transport = RecordingTransport()
        sentry_sdk.get_client().transport.kill()
        sentry_sdk.get_client().transport = self.transport
        self.chat_secret = uuid4().hex
        self.user_secret = uuid4().hex

    def tearDown(self):
        sentry_sdk.get_client().close()
        sentry_sdk.get_global_scope().set_client(self.previous_client)
        self.scope.__exit__(None, None, None)

    async def test_handled_error_is_reported_once_without_conversation_data(self):
        update = MagicMock()
        update.effective_chat.send_message = AsyncMock()
        context = MagicMock()
        context.chat_data = {"private": self.chat_secret}
        context.user_data = {"private": self.user_secret}
        try:
            raise RuntimeError("Conversation failed")
        except RuntimeError as error:
            result = await handle_error(
                update, context, error, logging.getLogger(__name__)
            )

        self.assertEqual(result, ConversationHandler.END)
        update.effective_chat.send_message.assert_awaited_once()
        self.assertEqual(context.user_data, {})
        self.assertEqual(len(self.transport.events), 1)
        event = self.transport.events[0]
        self.assertEqual(event["tags"]["service"], "bot")
        self.assertEqual(event["exception"]["values"][-1]["type"], "RuntimeError")
        serialized = json.dumps(event)
        self.assertNotIn(self.chat_secret, serialized)
        self.assertNotIn(self.user_secret, serialized)
        self.assertFalse(event.get("breadcrumbs", {}).get("values"))
        for value in event["exception"]["values"]:
            for frame in value.get("stacktrace", {}).get("frames", []):
                self.assertNotIn("vars", frame)

    async def test_expected_not_modified_error_is_ignored(self):
        await handle_error(
            MagicMock(),
            MagicMock(),
            BadRequest("Message is not modified"),
            logging.getLogger(__name__),
        )
        self.assertEqual(self.transport.events, [])

    async def test_application_error_handler_reports_undecorated_errors(self):
        from bot import create_bot

        with patch("bot.TOKEN", "123456789:synthetic-test-token"):
            application = create_bot()
        await application.process_error(None, RuntimeError("Unhandled callback"))

        self.assertEqual(len(self.transport.events), 1)
        self.assertEqual(
            self.transport.events[0]["exception"]["values"][-1]["value"],
            "Unhandled callback",
        )

    def test_empty_dsn_leaves_monitoring_disabled(self):
        with patch.dict(os.environ, {"SENTRY_DSN": ""}):
            with patch("utils.monitoring.sentry_sdk.init") as initialize:
                configure_monitoring()
        initialize.assert_not_called()
