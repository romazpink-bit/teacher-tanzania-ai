# TEACHER Server - Production - Wanafunzi HAWAHITAJI key
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json, os
from groq import Groq

app = FastAPI(title="TEACHER Tanzania - TIE 2025")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Knowledge base - 21 topics muhimu
knowledge_base = [
    {"subject": "Biology", "topic": "Cell Structure", "level": "O-Level", "notes": "Seli ni kitengo cha msingi cha uhai. Prokaryotic (bacteria bila nucleus) na Eukaryotic (mimea/wanyama na nucleus). Organelles: membrane, nucleus DNA, mitochondria powerhouse ATP, chloroplast photosynthesis, ribosome protein, vacuole. Tofauti seli ya mnyama na mmea."},
    {"subject": "Biology", "topic": "Photosynthesis", "level": "O-Level", "notes": "6CO2+6H2O+mwanga->C6H12O6+6O2 kwenye chloroplast na chlorophyll. Factors: mwanga, CO2, maji, joto. Importance kwa food chain."},
    {"subject": "Biology", "topic": "Blood Circulation", "level": "O-Level", "notes": "Moyo: atria 2 ventricles 2. Artery damu safi kutoka moyoni, Vein damu chafu, Capillary kubadilishana. Damu: RBC hemoglobin O2, WBC kinga, Platelets kuganda, Plasma. Mzunguko mara mbili."},
    {"subject": "Chemistry", "topic": "Atomic Structure", "level": "O-Level", "notes": "Atomu: nucleus proton+neutron na electrons shells. Atomic number=protons. Isotopes kama C-12 C-14. Configuration 2,8,8. Periodic: Groups vertical same valence, Periods horizontal. Alkali metals, Halogens, Noble gases."},
    {"subject": "Chemistry", "topic": "Acids Bases", "level": "O-Level", "notes": "Acids sour pH<7 H+, Bases bitter pH>7 OH-, Salts. Neutralization, titration, pH scale."},
    {"subject": "Physics", "topic": "Forces", "level": "O-Level", "notes": "Newton: 1st inertia, 2nd F=ma, 3rd action-reaction. Forces: gravity, friction, upthrust, tension. Motion equations v=u+at, s=ut+1/2at^2, v2=u2+2as."},
    {"subject": "Physics", "topic": "Electricity", "level": "O-Level", "notes": "Ohm V=IR. Series R=R1+R2 I same V splits. Parallel 1/R=1/R1+1/R2 V same I splits. Power P=VI. Safety fuse earthing."},
    {"subject": "Mathematics", "topic": "Quadratic Equations", "level": "O-Level", "notes": "ax^2+bx+c=0. Factorization, completing square, formula x=(-b±√(b²-4ac))/2a. Discriminant D=b²-4ac: D>0 mbili, D=0 moja, D<0 hakuna real. Graph parabola."},
    {"subject": "Mathematics", "topic": "Trigonometry", "level": "O-Level", "notes": "SOH CAH TOA sin=opp/hyp cos=adj/hyp tan=opp/adj. Pythagoras a2+b2=c2. Elevation depression bearing."},
    {"subject": "History", "topic": "Colonialism and Maji Maji", "level": "O-Level", "notes": "Berlin 1884-85. Sababu za ukoloni: malighafi masoko capital. Direct Indirect rule. Maji Maji 1905-07 Kinjekitile Ngwale maji ya uvundo, sababu: kodi kibarua mkonge, athari vifo 250k+ mwanzo wa utaifa."},
    {"subject": "History", "topic": "Nationalism", "level": "O-Level", "notes": "Misingi: elimu vita kuu UN Pan-Africanism. TANU 1954 Nyerere Uhuru 1961. Ghana 1957 Nkrumah Kenya Mau Mau. Neocolonialism."},
    {"subject": "Geography", "topic": "Climate Tanzania", "level": "O-Level", "notes": "Solar rotation siku revolution mwaka. Miamba igneous sedimentary metamorphic. Climate: equatorial tropical semi-arid. Vegetation equatorial forest savanna desert. Tanzania: kilimo kahawa Moshi, dhahabu Geita, Serengeti."},
    {"subject": "Civics", "topic": "Constitution", "level": "O-Level", "notes": "Katiba 1977, haki za binadamu UDHR, utawala bora transparency accountability rule of law, democracy multi-party, Muungano 1964, serikali za mitaa, life skills."},
    {"subject": "Kiswahili", "topic": "Sarufi", "level": "O-Level", "notes": "Ngeli 9: A-WA KI-VI LI-YA JI-MA U-ZI U-YA I-ZI YU KU. Vitenzi mizizi viambishi, vivumishi vielezi. Fasihi: Takadini Rosa Mistika tamthilia ushairi vina mizani methali vitendawili."},
]

# Groq client - key inatoka Render Environment Variable (wanafunzi hawaioni)
groq_key = os.getenv("GROQ_API_KEY", "")
client = Groq(api_key=groq_key) if groq_key else None
MODEL = "llama3-70b-8192"

class AskRequest(BaseModel):
    question: str
    subject: str = "General"
    level: str = "O-Level"

def search_context(q, subj, top_k=3):
    ql = q.lower()
    scored = []
    for item in knowledge_base:
        score = 0
        text = (item["topic"] + " " + item["notes"]).lower()
        for w in ql.split():
            if len(w)>2 and w in text:
                score+=1
        if subj.lower() in item["subject"].lower():
            score+=2
        if score>0:
            scored.append((score,item))
    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored:
        return [k for k in knowledge_base if subj.lower() in k["subject"].lower()][:top_k] or knowledge_base[:2]
    return [i for _,i in scored[:top_k]]

@app.get("/")
def home():
    return {"message": "TEACHER Tanzania API - TIE 2025", "topics": len(knowledge_base), "status": "Bure - Wanafunzi hawahitaji API key", "free": True}

@app.post("/ask")
async def ask(req: AskRequest):
    if not client:
        raise HTTPException(500, "GROQ_API_KEY haijawekwa kwenye server")
    
    contexts = search_context(req.question, req.subject)
    context_text = "\n\n".join([f"{c['subject']} - {c['topic']}: {c['notes']}" for c in contexts])
    
    system_prompt = f"""Wewe ni TEACHER, mwalimu wa Tanzania TIE 2025.
Mtaala: {context_text}
Jibu kwa Kiswahili sanifu, mifano ya Tanzania (Moshi, Geita, Serengeti). Toa pointi, hatua kwa hesabu, malizia swali la kujipima. Usiseme umetafuta PDF."""
    
    try:
        res = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Somo: {req.subject} {req.level} Swali: {req.question}"}
            ],
            temperature=0.3,
            max_tokens=900
        )
        return {
            "answer": res.choices[0].message.content,
            "sources": [f"{c['subject']} - {c['topic']}" for c in contexts],
            "model": MODEL,
            "free": True
        }
    except Exception as e:
        raise HTTPException(500, str(e))

# Kwa local: uvicorn main:app --reload
