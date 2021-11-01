import pandas
from sqlalchemy import create_engine, inspect
import psycopg2

HOST = "czechitaspsql.postgres.database.azure.com"
PORT = 5432
USER = "anna.ocilkova"
USERNAME = f"anna.ocilkova@czechitaspsql"
DATABASE = "postgres"
PASSWORD = "YgW4TIZNB0aMZa5U"
engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", echo=False)

# inspector = inspect(engine)
# print(inspector.get_columns('crime'))

# pandas.set_option('display.max_columns', None)
# pandas.set_option('display.max_rows', None)
# pandas.set_option('display.max_colwidth', 250)

# Tabulka crime v naší databázi obsahuje informace o kriminalitě v Chicagu. Data si můžete i interaktivně prohlédnout na mapě zde.
#
# Dataset je poměrně velký, a tak si určitě vytáhneme vždy jen nějaký výběr, se kterým budeme dále pracovat.
#
# Pomocí SQL dotazu si připrav tabulku o krádeži motorových vozidel (sloupec PRIMARY_DESCRIPTION by měl mít hodnotu "MOTOR VEHICLE THEFT").

vehicle_theft = pandas.read_sql("SELECT * from \"crime\" WHERE \"PRIMARY_DESCRIPTION\" = 'MOTOR VEHICLE THEFT'", con=engine)

# Tabulku dále pomocí pandasu vyfiltruj tak, aby obsahovala jen informace o krádeži aut (hodnota "AUTOMOBILE" ve sloupci SECONDARY_DESCRIPTION).

car_theft = vehicle_theft[vehicle_theft['SECONDARY_DESCRIPTION'] == "AUTOMOBILE"]

# Ve kterém měsíci dochází nejčastěji ke krádeži auta?

car_theft["DATE_OF_OCCURRENCE"] = pandas.to_datetime(car_theft["DATE_OF_OCCURRENCE"])
car_theft['DATE_OF_OCCURRENCE_MONTH'] = car_theft['DATE_OF_OCCURRENCE'].dt.month
car_theft_grouped = car_theft.groupby('DATE_OF_OCCURRENCE_MONTH').count()
print(car_theft_grouped.sort_values("CASE#", ascending=False))


# nakonec to funguje, ale proč mi to hlásí ty chyby při převádění na datetime? dalo by se jim nějak vyhnout? koukala jsem na ten .loc, ale moc se mi to nedaří pořešit. díky.



