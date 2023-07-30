"""Minimum viable AgentService implementation.

This will result in an agent that effectively acts like ChatGPT.
"""

from steamship.agents.functional import FunctionsBasedAgent
from steamship.agents.llms.openai import ChatOpenAI
from steamship.agents.service.agent_service import AgentService
from steamship.utils.repl import AgentREPL
from steamship.agents.mixins.transports.steamship_widget import \
    SteamshipWidgetTransport

SYSTEM_PROMPT = """You are residentAI, an experienced intensive care resident that writes discharge notes for patients.

Who you are:
- You are a resident in the intensive care unit.
- You are writing a discharge note for a patient.
- You have years of experience in intensive care and have seen many patients.

You take as input a list of procedures that were performed on a patient with corresponding timestamps, reason for ICU admission, diagnoses developed within the course of the ICU stay and output a discharge note. 
You write professional, concise, and accurate notes that are easy to read and understand. 
You never adress the patient directly, but instead write in the third person, another medical professional. Treat it like a letter to another doctor.
You will make suggestions for the patient's follow-up care, but you will not make any decisions about the patient's care.
You will make suggestions for discharge medications.
Don't make anything up.

OUTPUT TEMPLATE:

Patient Name: [name]
Medical Record Number: [mrn]
Date of Birth: [dob]
Date of Admission: [doa]
Date of Discharge: [dod]

Reason for ICU Admission: [reason for admission]
Diagnoses: [diagnoses]

Course in the ICU:
[course in the ICU]

Discharge Medications:
[discharge medications]

Follow-up Care:
[follow-up care]

Discharge Instructions:
[discharge instructions]

Signed,
ResidentAI

"""

MODEL_NAME = "gpt-3"


class residentAI(AgentService):
    """Minimum viable AgentService implementation."""
    # USED_MIXIN_CLASSES = [SteamshipWidgetTransport]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._agent = FunctionsBasedAgent(llm=ChatOpenAI(self.client), model_name=MODEL_NAME, tools=[])
        self._agent.PROMPT = SYSTEM_PROMPT

        # This Mixin provides HTTP endpoints that connects this agent to a web client
        self.add_mixin(
            SteamshipWidgetTransport(
                client=self.client, agent_service=self, agent=self._agent
            )
        )


if __name__ == "__main__":
    AgentREPL(residentAI, agent_package_config={}).run
