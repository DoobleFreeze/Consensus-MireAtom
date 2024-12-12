from web import create_api
from configs.settings import *


app = create_api(
    flask_log=FLASK_LOG,
    logging_cgf_path=LOGGING_CFG_PATH
)

if __name__ == '__main__':
    # Запуск web-приложения
    app.run(
        host=HOST_SERVER,
        port=PORT_SERVER,
        debug=False
    )
