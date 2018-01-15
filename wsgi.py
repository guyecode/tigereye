
from tigereye import create_app
from tigereye.configs.production import ProductionConfig


tigereye = create_app(config=ProductionConfig())
