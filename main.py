from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.wardrobe_controller import wardrobe_router
from controllers.edit_controller import edit_router
from controllers.review_controller import review_router
from controllers.tryon_controller import try_on_router

def create_app() -> FastAPI:
    app = FastAPI(title="Outfit Python API")

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    # Router’ları ekle
    app.include_router(wardrobe_router)
    app.include_router(edit_router)
    app.include_router(review_router)
    app.include_router(try_on_router)

    return app

app = create_app()
