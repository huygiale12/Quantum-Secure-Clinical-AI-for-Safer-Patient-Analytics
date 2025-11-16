# Team Setup Guide

## Prerequisites
- Python 3.11+
- Git

## Setup Steps

### 1. Clone & Install
```bash
git clone [REPO_URL]
cd Quantum-Secure-Clinical-AI-for-Safer-Patient-Analytics
pip install -r requirements.txt
```

### 2. Get API Keys

#### Supabase (SHARED)
Ask Tin for the Supabase credentials via private message.

#### Gemini API (INDIVIDUAL - FREE)
1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your keys
```

### 4. Test
```bash
python test_gemini.py
```

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt --upgrade
```

### Gemini 404 error
Make sure you're using `gemini-2.5-flash` not `gemini-1.5-flash`

### Supabase connection failed
Double-check the credentials Tin sent you.

## Questions?
Contact Tin on [Discord/Slack/etc]
