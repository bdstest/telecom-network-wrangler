from fastapi import FastAPI
app = FastAPI(title='Network Wrangler API', version='0.1.0')

@app.get('/health')
async def health_check():
    return {'status': 'healthy'}
