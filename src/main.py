from sites import *

companiess = Companies([])
all_companiess = companiess.get_companies_from_json(JSON_FILE)
all_companiess.save_companies_to_sqlite(DB_FILE)