from fastapi import FastAPI

app = FastAPI(title='abacaba')

@app.route('/health')
def health():
    return {"status": "ok"}