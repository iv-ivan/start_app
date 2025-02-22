# Frontend
1) `mkdir frontend && cd frontend`
2) Official React docs recommend using framework. So we start new frontend app with [React Router](https://reactrouter.com/home)
```
npx create-react-router@latest --template remix-run/react-router-templates/default
# - Where: ./app
# - Initialize git: No
#- Install dependencies: Yes
```
3) Take a look at auto-generated `README.md`, it's quite useful.
4) We are going to build SPA (SinglePageApplication), because it's much easier to deploy, only a page `index.html`:
```
# Disable ServerSideRendering in react-router.config.ts
ssr: false
```
5) I've updated `home.tsx` and `main/*.tsx` files to contain a simple input field, please check them.
6) Remove dark mode style from `app.css`, we don't need it now.
7) **CORS**: To be able to call our API from our website, we need to support CORS headers in API response. At this step we patch `main.py` for local development:
```python
from fastapi.middleware.cors import CORSMiddleware

...

origins = [
    "http://localhost:5173/",
    "http://localhost:5173",
    "localhost:5173",
    "localhost:5173/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
8) Let's test!
```
npm run dev
python3 -m fastapi dev main.py
# Now open localhost:5173 in your browser
```