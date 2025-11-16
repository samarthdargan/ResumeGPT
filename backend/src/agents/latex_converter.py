from agent_framework.azure import AzureOpenAIChatClient
from ..config import settings
import json
import re
class LaTeXConverter:
    def __init__(self):
        self.client = AzureOpenAIChatClient(
            endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME
        )

        self.agent = self.client.create_agent(
            name="LaTeX Resume Generator",
            system_prompt="""
You are an expert LaTeX resume generator.

TASK:
You will receive:
1. A LaTeX TEMPLATE (.tex code)
2. A JSON resume object

Your job:
- Merge JSON content into the LaTeX template.
- Fill ONLY the sections that exist in the template.
- If JSON contains extra sections that template doesn't have → skip them.
- If template contains sections missing in JSON → delete/skip gracefully.
- Do NOT hallucinate any content.
- Preserve the LaTeX formatting exactly as provided in the template.

STRICT OUTPUT RULE:
Return ONLY valid LaTeX code from \\documentclass to \\end{document}.
No explanations, no markdown, no comments.

MERGING RULES:
- Replace placeholders or section content with JSON fields even if formatting differs.
- Bullet points from JSON → use same LaTeX bullet style already inside the template.
- Multiple jobs, projects, skills → repeat the LaTeX item structures in template.
- Maintain template style: fonts, spacing, commands, etc.
- Escape LaTeX-sensitive characters: %, &, _, $, {, }, #, ^, ~.

Your output must be:
✔ A SINGLE, fully formatted .tex file
✔ 100% compilable
✔ Uses template structure exactly
✔ Insert JSON resume data properly
"""
        )
    
    async def strip_fenced_code(self, text):
        text = re.sub(r"^```[a-zA-Z0-9_+-]*\s*\n", "", text)
        text = re.sub(r"\n```$", "", text)
        return text

    async def convert_to_latex(self, latex_template: str, json_data: dict) -> dict:
        """
        latex_template: raw .tex template string
        json_data: resume JSON object
        """
        try:
            message = f"""
Here is the LaTeX template:

===== TEMPLATE START =====
{latex_template}
===== TEMPLATE END =====

Here is the JSON resume data:
{json.dumps(json_data, indent=2)}

REMEMBER:
Output MUST begin with \documentclass and end with \end{{document}}. 
Output MUST contain ONLY LaTeX — no markdown, no commentary.

Generate the final LaTeX resume.
```latex
"""
            response = await self.agent.run(message)
            return {"success": True, "latex": await self.strip_fenced_code(response.text)}

        except Exception as e:
            return {"success": False, "error": str(e)}
