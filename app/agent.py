import asyncio
import json
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus

import httpx
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, JobContext, RunContext, function_tool
from livekit.plugins import google

from app.memory_store import JsonMemoryStore


load_dotenv(".env.local")
MEMORY_STORE = JsonMemoryStore(Path("jarvis_memory.json"))


class JarvisAssistant(Agent):
    def __init__(self) -> None:
        memory = MEMORY_STORE.load()

        super().__init__(
            instructions=f"""
            You are Jarvis, a friendly AI voice assistant.

            Speak in simple English and keep voice responses reasonably short.
            Explain technical subjects step by step when useful.

            You can:
            - remember, recall and forget information
            - open approved Windows applications
            - open websites and Google searches
            - provide the current date and time
            - check current weather
            - create Python files inside a controlled workspace

            Use tools when the user asks for one of these actions.
            Never claim an action succeeded unless the tool confirms it.

            SLEEP COMMAND RULE:
            Only call go_to_sleep when the user clearly asks Jarvis to stop
            the current conversation, for example: "go to sleep", "sleep now",
            "stop listening", "goodbye Jarvis", "close Jarvis" or
            "return to sleep". If speech is uncertain, ask the user to repeat.
            When the command is clear, call go_to_sleep immediately.

            Current saved memory:
            {json.dumps(memory, ensure_ascii=False)}
            """
        )

    @function_tool()
    async def remember_information(
        self,
        context: RunContext,
        key: str,
        value: str,
    ) -> str:
        """Save an important key/value pair for future conversations."""
        clean_key, clean_value = MEMORY_STORE.remember(key, value)
        return f"I saved {clean_key} as {clean_value}."

    @function_tool()
    async def recall_information(self, context: RunContext, key: str) -> str:
        """Recall a previously saved value by key."""
        clean_key = MEMORY_STORE.normalise_key(key)
        value = MEMORY_STORE.recall(key)
        if value is None:
            return f"I do not have anything saved under {clean_key}."
        return f"{clean_key}: {value}"

    @function_tool()
    async def show_all_memories(self, context: RunContext) -> str:
        """Return all locally saved information."""
        memory = MEMORY_STORE.load()
        if not memory:
            return "There is no saved information yet."
        return json.dumps(memory, ensure_ascii=False)

    @function_tool()
    async def forget_information(self, context: RunContext, key: str) -> str:
        """Delete one saved memory."""
        clean_key = MEMORY_STORE.normalise_key(key)
        if not MEMORY_STORE.forget(key):
            return f"I could not find a memory named {clean_key}."
        return f"I deleted the memory named {clean_key}."

    @function_tool()
    async def go_to_sleep(self, context: RunContext) -> str:
        """Close the current agent session and return to wake-word mode."""

        async def close_session() -> None:
            await asyncio.sleep(0.5)
            await context.session.aclose()

        asyncio.create_task(close_session())
        return "Going to sleep."

    @function_tool()
    async def open_application(
        self,
        context: RunContext,
        application_name: str,
    ) -> str:
        """Open a Windows application from an explicit allow-list."""
        app_name = application_name.strip().lower()
        allowed_apps = {
            "chrome": ["cmd", "/c", "start", "", "chrome"],
            "google chrome": ["cmd", "/c", "start", "", "chrome"],
            "calculator": ["calc.exe"],
            "calc": ["calc.exe"],
            "notepad": ["notepad.exe"],
            "vs code": ["cmd", "/c", "start", "", "code"],
            "visual studio code": ["cmd", "/c", "start", "", "code"],
            "file explorer": ["explorer.exe"],
            "explorer": ["explorer.exe"],
        }

        command = allowed_apps.get(app_name)
        if command is None:
            approved = ", ".join(sorted(allowed_apps))
            return (
                f"I cannot open {application_name}. "
                f"Approved applications are: {approved}."
            )

        try:
            subprocess.Popen(command)
            return f"I opened {application_name}."
        except OSError as error:
            return f"I could not open {application_name}: {error}"

    @function_tool()
    async def open_website(self, context: RunContext, website: str) -> str:
        """Open a website in the computer's default browser."""
        common_websites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "github": "https://github.com",
            "linkedin": "https://www.linkedin.com",
            "livekit": "https://livekit.io",
            "gmail": "https://mail.google.com",
        }

        website = website.strip()
        url = common_websites.get(website.lower(), website)
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"

        return f"I opened {url}." if webbrowser.open(url) else f"I was unable to open {url}."

    @function_tool()
    async def search_google(self, context: RunContext, query: str) -> str:
        """Open Google search results for a query."""
        search_url = "https://www.google.com/search?q=" + quote_plus(query.strip())
        if webbrowser.open(search_url):
            return f"I opened Google results for {query}."
        return "I could not open the Google search."

    @function_tool()
    async def get_current_date_and_time(self, context: RunContext) -> str:
        """Get the current local date and time from this computer."""
        return datetime.now().strftime(
            "Today is %A, %d %B %Y, and the time is %I:%M %p."
        )

    @function_tool()
    async def get_weather(self, context: RunContext, city: str) -> str:
        """Get current weather for a city using Open-Meteo."""
        descriptions = {
            0: "clear sky",
            1: "mainly clear",
            2: "partly cloudy",
            3: "overcast",
            45: "foggy",
            48: "foggy",
            51: "light drizzle",
            53: "drizzle",
            55: "heavy drizzle",
            61: "light rain",
            63: "rain",
            65: "heavy rain",
            71: "light snow",
            73: "snow",
            75: "heavy snow",
            80: "light rain showers",
            81: "rain showers",
            82: "heavy rain showers",
            95: "thunderstorms",
            96: "thunderstorms with hail",
            99: "heavy thunderstorms with hail",
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                location_response = await client.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={
                        "name": city,
                        "count": 1,
                        "language": "en",
                        "format": "json",
                    },
                )
                location_response.raise_for_status()
                results = location_response.json().get("results")
                if not results:
                    return f"I could not find a city named {city}."

                location = results[0]
                weather_response = await client.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": location["latitude"],
                        "longitude": location["longitude"],
                        "current": (
                            "temperature_2m,apparent_temperature,"
                            "weather_code,wind_speed_10m"
                        ),
                        "timezone": "auto",
                    },
                )
                weather_response.raise_for_status()

            current = weather_response.json()["current"]
            condition = descriptions.get(
                current["weather_code"],
                "unknown weather conditions",
            )
            return (
                f"In {location['name']}, {location.get('country', '')}, "
                f"it is {condition}. The temperature is "
                f"{current['temperature_2m']} degrees Celsius, it feels like "
                f"{current['apparent_temperature']} degrees, and the wind speed "
                f"is {current['wind_speed_10m']} kilometres per hour."
            )
        except httpx.TimeoutException:
            return "The weather request took too long. Please try again."
        except httpx.HTTPStatusError as error:
            return f"The weather service returned status {error.response.status_code}."
        except httpx.RequestError as error:
            return f"I could not connect to the weather service: {error}"
        except (KeyError, TypeError, ValueError) as error:
            return f"I could not understand the weather information: {error}"

    @function_tool()
    async def create_python_file(
        self,
        context: RunContext,
        filename: str,
        code: str,
    ) -> str:
        """Create a Python file only inside generated_projects/."""
        try:
            workspace = Path("generated_projects").resolve()
            workspace.mkdir(exist_ok=True)
            clean_filename = Path(filename).name
            if not clean_filename.endswith(".py"):
                clean_filename += ".py"

            file_path = (workspace / clean_filename).resolve()
            if file_path.parent != workspace:
                return "I cannot create files outside the generated projects folder."
            if file_path.exists():
                return (
                    f"{clean_filename} already exists. "
                    "Please ask me to use a different filename."
                )

            file_path.write_text(code.strip() + "\n", encoding="utf-8")
            subprocess.Popen(["code", str(file_path)], shell=False)
            return (
                f"I created {clean_filename} inside the generated projects "
                "folder and opened it in Visual Studio Code."
            )
        except FileNotFoundError:
            return (
                "The file was created, but I could not open Visual Studio Code. "
                "Make sure the VS Code code command is installed."
            )
        except OSError as error:
            return f"I could not create the Python file: {error}"


async def entrypoint(ctx: JobContext) -> None:
    session = AgentSession(
        llm=google.realtime.RealtimeModel(voice="Puck"),
    )
    await session.start(room=ctx.room, agent=JarvisAssistant())
    await session.generate_reply(
        instructions="Greet the user briefly as Jarvis and ask how you can help."
    )


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(entrypoint_fnc=entrypoint),
    )
