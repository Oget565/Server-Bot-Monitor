from aiogram import types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.filters.owner import IsOwner
from app.settings.read_write_settings import Settings
import asyncio

sett = Settings()

keyboard_builder = InlineKeyboardBuilder()
keyboard_builder.button(text="Update Interval", callback_data="interval_call")
keyboard_builder.button(text="Timezone Region", callback_data="timezone_call")
keyboard_builder.button(text="Notification Time", callback_data="notification_call")
keyboard = keyboard_builder.as_markup(row_width=1)

class SettingsStates(StatesGroup):
    waiting_for_interval = State()
    waiting_for_timezone = State()
    waiting_for_notification = State()

def settings_commands(dp):
    @dp.message(Command("settings"), IsOwner())
    async def get_keyboard(message: types.Message):
        await message.reply("Settings are working", reply_markup=keyboard)

    @dp.callback_query(lambda call: call.data in ['interval_call', 'timezone_call', 'notification_call'])
    async def callback_handler(call: types.CallbackQuery, state: FSMContext):
        await call.answer()
        if call.data == "interval_call":
            await call.message.answer("Enter the interval value in minutes \n"
                                      f"Curret value: {sett.read_settings("update_interval")} minutes"
                                      )
            await state.set_state(SettingsStates.waiting_for_interval)

        if call.data == "timezone_call":
            await call.message.answer("Enter yout timezone location in America/New_York format \n"
                                      f"Current timezone: {sett.read_settings("timezone")}"
                                      )
            await state.set_state(SettingsStates.waiting_for_timezone)

        if call.data == "notification_call":
            await call.message.answer("Enter the time of daily notification in 24hr format \n"
                                      f"Current notification time: {sett.read_settings("notification_time")}"
                                      )
            await state.set_state(SettingsStates.waiting_for_notification)

    @dp.message(SettingsStates.waiting_for_interval, IsOwner())
    async def process_interval(message: types.Message, state: FSMContext):
        interval_val = message.text
        sett.write_settings("update_interval", interval_val)
        await message.answer("Success!")
        await state.clear()

    @dp.message(SettingsStates.waiting_for_timezone, IsOwner())
    async def process_timezone(message: types.Message, state: FSMContext):
        timezone_val = message.text
        sett.write_settings("timezone", timezone_val)
        await message.answer("Success!")
        await state.clear()

    @dp.message(SettingsStates.waiting_for_notification, IsOwner())
    async def process_notification(message: types.Message, state: FSMContext):
        notification_val = message.text
        sett.write_settings("notification_time", notification_val)
        await message.answer("Success!")
        await state.clear()