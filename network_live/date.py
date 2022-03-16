"""Work with different date formats for logs and parsers."""


from datetime import datetime, timedelta


class Date(object):
    """Date interface."""

    date_formats = {
        'tele2': '%Y%m%{d}'.format(d='d'),
        'beeline': '%{d}.%m.%Y'.format(d='d'),
        'network_live': '%{d}%m%y'.format(d='d'),
    }

    @classmethod
    def get_date(cls, format_key):
        """
        Return date for date_format.

        Args:
            format_key: string

        Returns:
            string
        """
        now = datetime.now()
        date_format = cls.date_formats[format_key]
        if format_key == 'network_live':
            return datetime.now().strftime(date_format)

        return (now - timedelta(days=1)).strftime(date_format)
