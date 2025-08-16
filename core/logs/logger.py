import pytz
import logging
from decouple import config
from asgiref.local import Local
from django.utils import timezone
nepali_timezone = pytz.timezone(config('TIME_ZONE'))
current_time = timezone.now().astimezone(nepali_timezone)
formatted_time = current_time.strftime("%Y-%m-%d %I:%M:%S %p")


nepali_time = timezone.now()
_local = Local()

class UserFilter(logging.Filter):
    def filter(self, record):
        record.username = getattr(_local, 'username', 'Anonymous')
        record.logged_time = formatted_time
        full_path = record.pathname
        record.short_path = '/'.join(full_path.split('/')[-3:])
        return True

LOGGING_CONFIG = None

logging.basicConfig(
    format='%(levelname)s -- %(logged_time)s -- %(short_path)s:%(lineno)d -- User: %(username)s -- Message: %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bookmanagementsystem.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.addFilter(UserFilter())
