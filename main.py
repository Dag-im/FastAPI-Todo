from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from todos.routes import router as todo_routes
from auth.routes import router as auth_routes
from users.routes import router as user_routes
from core.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",  # React or Next.js dev server
    "http://127.0.0.1:3000",
    "https://your-frontend-domain.com",  # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # OR ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],                # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],                # Allows all headers
)

# Include all routers
app.include_router(todo_routes)  # ✅ Correct usage
app.include_router(auth_routes)  # ✅ Correct usage
app.include_router(user_routes)  # ✅ Correct usage
