import os
from typing import List, Dict

SYSTEM = """You are Ada, an encouraging programming tutor for BCA beginners.
Teach in simple English. Never overwhelm the learner. Prefer:
1) a short explanation,
2) a tiny analogy,
3) a small code example,
4) one practice step.
When reviewing code, explain the error and give a hint before giving a full solution.
Use Markdown. Avoid pretending code was executed. Keep most answers under 220 words.
The learner is studying {language}. Their current topic is {topic}.
Performance context: {context}
"""

def provider():
    if os.getenv("OPENAI_API_KEY"): return "openai"
    if os.getenv("ANTHROPIC_API_KEY"): return "anthropic"
    return None

def enabled():
    return provider() is not None

def ask(language, topic, question, history=None, context=""):
    p=provider()
    if not p:
        return offline_answer(language,topic,question)
    system=SYSTEM.format(language=language,topic=topic,context=context or "No performance data yet.")
    msgs=list(history or [])[-8:]+[{"role":"user","content":question}]
    try:
        if p=="openai":
            from openai import OpenAI
            client=OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            r=client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),
                messages=[{"role":"system","content":system}]+msgs,
                temperature=0.4,max_tokens=500)
            return r.choices[0].message.content
        from anthropic import Anthropic
        client=Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        r=client.messages.create(model=os.getenv("ANTHROPIC_MODEL","claude-3-5-haiku-latest"),
            max_tokens=500,system=system,messages=msgs)
        return r.content[0].text
    except Exception as e:
        return f"⚠️ The AI service could not respond right now.\\n\\n**Fallback:** {offline_answer(language,topic,question)}\\n\\n`{type(e).__name__}`"

def offline_answer(language,topic,question):
    q=question.lower()
    if "hint" in q:
        return f"💡 **Hint for {topic}:** Break the problem into one tiny step first. Write the smallest piece of {language} syntax you know for this topic, then build from there."
    if "error" in q or "wrong" in q:
        return "🛠️ **Debugging approach:** read the error message, find the line it points to, check brackets/quotes/types, then test the smallest change. Paste the exact error and code here for a more specific review."
    if "example" in q:
        return f"📘 **Tiny example:** Start with the simplest {language} example for **{topic}**, then change one value and observe what happens. Small experiments make the concept stick."
    return f"👋 I'm Ada. You're learning **{topic} in {language}**. The live LLM is not configured yet, but I can still guide you: read the lesson, study the example, then complete the practice challenge. Add an OpenAI or Anthropic API key to unlock full AI explanations."

def lesson(language,topic,status):
    return ask(language,topic,
        f"Start a short lesson on {topic}. The learner status is {status}. Adapt the difficulty and finish with one mini challenge.")
