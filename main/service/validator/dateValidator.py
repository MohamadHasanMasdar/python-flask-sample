import datetime
import bundles.messages as messages
from main.utils import jsonMaker


class DateValidate:
    def validate_date_format_is_correct(self, date):

        # giving the date format
        date_format = '%Y-%m-%d'
        try:
            datetime.datetime.strptime(date, date_format)
        except ValueError:
            raise ValueError

