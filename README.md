# TEACHER Tanzania - Server BURE

## Ni BURE kweli?
NDIO 100% BURE:

1. **Groq API (Llama 3 70B)**: BURE - 14,400 requests SIKU (wanafunzi 1000+ bure)
2. **Render.com Hosting**: BURE - 750 hours mwezi (server inafanya kazi masaa yote bure)
3. **Domain**: BURE - https://teacher-tanzania-ai.onrender.com

Hakuna kadi ya benki inahitajika kwa Groq na Render free tier.

## Jinsi ya Kudeploy (Dakika 5):

### Hatua 1: GitHub
1. Nenda github.com -> New repository -> teacher-tanzania-ai
2. Upload files hizi zote (main.py, requirements.txt, render.yaml)

### Hatua 2: Render.com
1. Nenda render.com -> Sign up na GitHub (bure)
2. New + -> Web Service -> Connect repository yako
3. Render itasoma render.yaml yenyewe
4. Nenda Environment -> Add Variable:
   Key: GROQ_API_KEY
   Value: gsk_yako_... (key uliyopata)
5. Bonyeza Deploy

### Hatua 3: Maliza!
Baada ya dakika 2-3, utapata link:
https://teacher-tanzania-ai.onrender.com

Test: Fungua https://teacher-tanzania-ai.onrender.com/docs -> Try /ask

### Hatua 4: Unganisha na App ya Simu
Kwenye app yako ya React Native/Expo, weka:

const API_URL = "https://teacher-tanzania-ai.onrender.com"

Wanafunzi HAWAWEKI key, wanauliza tu!

## Gharama baadaye?
- Wanafunzi 0-1000 kila siku: BURE kabisa
- Wanafunzi 1000-10,000: Bado bure (Groq inatoa sana)
- Wanafunzi 10,000+: $5-10 mwezi tu

## Msaada?
Ukikwama, tuma screenshot ya Render dashboard.
