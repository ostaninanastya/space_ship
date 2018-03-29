from infi.clickhouse_orm.fields import Field

class BooleanField(Field):

    db_type = 'UInt8'

    class_default = False

    def to_python(self, value, timezone_in_use):
        
        if value in (1, '1', True):
            return True
        elif value in (0, '0', False):
            return False
        else:
            raise ValueError('Invalid value for BooleanField: %r' % value)

    def to_db_string(self, value, quote=True):
        return '1' if value else '0'