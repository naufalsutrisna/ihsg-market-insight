import json

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.clients.llm import get_llm
from app.prompts.market_prompts import CLOSING_INSIGHT_PROMPT


def format_closing_insight(report: dict) -> str:
    prompt = ChatPromptTemplate.from_template(
        CLOSING_INSIGHT_PROMPT
    )

    chain = prompt | get_llm() | StrOutputParser()

    report_data = json.dumps(
        report,
        ensure_ascii=False,
        indent=2,
    )

    return chain.invoke({
        "report_data": report_data,
    }).strip()
