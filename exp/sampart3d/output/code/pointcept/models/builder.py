from pointcept.utils.registry import Registry

MODELS = Registry("models")
MODULES = Registry("modules")


def build_model(cfg):
    """Build models."""
    return MODELS.build(cfg)
