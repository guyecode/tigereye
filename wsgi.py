
from tigereye import create_app
from tigereye.configs.production import ProductionConfig


application = create_app(config=ProductionConfig)
