from src.scripts.settings import Settings


def test_embedding_dim():
   settings = Settings()

   assert settings.embedding_dim == 128