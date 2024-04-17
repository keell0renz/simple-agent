"""Entry point, main file which works with UI."""

from typing import Any, Literal, cast, List, Dict, Union

from langchain_core.messages import MessageLikeRepresentation
from langchain.schema import AIMessage, HumanMessage

import chainlit as cl

from system_prompt import _construct_system_prompt
from agent import agent_executor
from utils import image_to_base64


@cl.on_chat_start
async def init():
    chat_history: list[MessageLikeRepresentation] = []

    cl.user_session.set("chat_history", chat_history)


@cl.on_message
async def main(message: cl.Message):
    history: list[MessageLikeRepresentation] = cl.user_session.get("chat_history")  # type: ignore
    response = cl.Message(content="")

    images = [file for file in message.elements if file.mime and "image" in file.mime]

    content = [{"type": "text", "text": message.content}] + [
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_to_base64(file.path)}"
            },
        }
        for file in images
        if file.path
    ]

    content = cast(List[Union[str, Dict]], content)

    history.append(HumanMessage(content=content))

    await response.send()

    try:
        async for event in agent_executor.astream_events(
            {"messages": history, "system_prompt": _construct_system_prompt()},
            version="v1",
        ):
            kind = event["event"]

            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    await response.stream_token(content)

            # elif kind == "on_tool_start":
            #     async with cl.Step(name=event["name"]) as step:
            #         step.input = event["data"].get("input")  # type: ignore

            # elif kind == "on_tool_end":
            #     async with cl.Step(name=event["name"]) as step:
            #         step.output = event["data"].get("output")  # type: ignore

    except Exception as e:
        print(e)

    history.append(AIMessage(content=response.content))
