import os
from dotenv import load_dotenv

# Load environment variables of file .env
load_dotenv()


class Config(object):
    """
    Base configuration class.

    Attributes:
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): If set to False,
        it disables the modification tracking system in SQLAlchemy
                                               to save memory.

    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """
    Development configuration class that inherits from the base Config class.

    Attributes:
        DEBUG (bool): If set to True, enables debug mode for the Flask
        application.
        SQLALCHEMY_DATABASE_URI (str): The database URI that should be used
        for the connection. It reads from the environment
                                       variable 'DATABASE_URL' or defaults to
                                       'sqlite:///development.db'.
    """
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'sqlite:///development.db')
    
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '2c1br3mt2wkkcagl68aqh5iml')


class ProductionConfig(Config):
    """
    Production configuration class that inherits from the base Config class.

    Attributes:
        DEBUG (bool): If set to False, disables debug mode for the Flask
        application.
        SQLALCHEMY_DATABASE_URI (str): The database URI that should be used
        for the connection. It reads from the environment
                                       variable 'DATABASE_URL' (production)
    """

    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


def get_config():
    """
    Determines the configuration class to use based on the 'ENV' environment
    variable.

    Returns:
        Config: The appropriate configuration class (DevelopmentConfig or
        ProductionConfig).

    Notes:
        - If 'ENV' is set to 'production', it returns the ProductionConfig
        class.
        - If 'ENV' is set to any other value or is not set, it returns the
        DevelopmentConfig class.
    """
    env = os.environ.get('ENV', 'development')
    if env == 'production':
        return ProductionConfig
    else:
        return DevelopmentConfig
