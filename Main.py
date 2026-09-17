import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Knowledge base simple
knowledge = [
    {"subject": "Biology", "topic": "Cell", "notes": "Seli ni kitengo cha msingi"},
    {"subject": "History", "topic": "Maji Maji", "notes": "Vita ya Maji Maji 1905-07 Kinjekitile"},
    {"subject": "Mathematics", "topic": "Quadratic", "notes": "ax2+bx+c=0 formula x=(-b±√D)/2a"},
]

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except:
    GROQ_AVAILABLE = False

groq_key = os.getenv("GROQ_API_KEY", "")
client = None
if GROQ_AVAILABLE and groq_key:
    try:
        client = Groq(api_key=groq_key)
    except:
        client = None

class AskRequest(BaseModel):
    question: str
    subject: str = "General"
    level: str = "O-Level"

@app.get("/")
def home():
    return {
        "message": "TEACHER Tanzania - TIE 2025 - BURE",
        "status": "Live" if client else "Add GROQ_API_KEY in Environment",
        "free": True,
        "topics": len(knowledge),
        "groq_ready": client is not None
    }

@app.post("/ask")
async def ask(req: AskRequest):
    if not client:
        # Fallback bila Groq - ili deploy isifanane
        return {
            "answer": f"Swali: {req.question}\n\nJibu la TIE 2025 (bila AI): Hii ni mfano. Weka GROQ_API_KEY kwenye Render Environment Variables ili upate majibu ya Llama 3 70B halisi. Knowledge: {[k['topic'] for k in knowledge][:3]}",
            "sources": ["TIE 2025 - Fallback"],
            "model": "fallback",
            "free": True,
            "note": "Weka GROQ_API_KEY ili AI halisi ianze"
        }
    
    # Real AI
    context = "\n".join([f"{k['subject']}-{k['topic']}: {k['notes']}" for k in knowledge])
    prompt = f"Wewe ni mwalimu wa Tanzania TIE 2025. Mtaala: {context}. Jibu kwa Kiswahili, mifano ya Tanzania. Swali: {req.question}"
    
    try:
        res = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": req.question}
            ],
            temperature=0.3,
            max_tokens=800
        )
        return {"answer": res.choices[0].message.content, "free": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
