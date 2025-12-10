from fastapi import FastAPI

app = FastAPI(title='abacaba')

@app.get('/health')
def health():
    return {"status": "ok"}