class CCSReadOnlyRouter:
    """
    Router bazy danych zapewniający, że baza 'ccs' jest wyłącznie do odczytu (read-only).
    Uniemożliwia jakiekolwiek modyfikacje, zapisy i migracje na tej bazie.
    """
    def db_for_read(self, model, **hints):
        # Kierujemy odczyt modeli CCS bezpośrednio do bazy 'ccs'
        if model._meta.db_table.startswith('django].[vv_'):
            return 'ccs'
        return None

    def db_for_write(self, model, **hints):
        # Blokujemy zapis dla modeli powiązanych z CCS lub przy próbie zapisu bezpośrednio do aliasu 'ccs'
        if model._meta.db_table.startswith('django].[vv_') or hints.get('using') == 'ccs':
            raise PermissionError("Zapis do bazy danych CCS jest zabroniony (baza tylko do odczytu)!")
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Blokujemy relacje pomiędzy bazą lokalną a zewnętrzną CCS
        if obj1._state.db == 'ccs' or obj2._state.db == 'ccs':
            return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Całkowicie wykluczamy bazę 'ccs' z jakichkolwiek migracji Django
        if db == 'ccs':
            return False
        return None
